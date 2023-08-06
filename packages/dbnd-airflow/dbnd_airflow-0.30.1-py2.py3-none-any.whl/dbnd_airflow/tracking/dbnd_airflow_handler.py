import logging
import os
from contextlib import contextmanager

from uuid import UUID

import attr

from airflow.operators.subdag_operator import SubDagOperator
from airflow.utils.log.file_task_handler import FileTaskHandler
from more_itertools import first_true

from dbnd import config, get_dbnd_project_config
from dbnd._core.configuration.environ_config import ENV_DBND_CURRENT_ATTEMPT_UID
from dbnd._core.context.databand_context import new_dbnd_context
from dbnd._core.inplace_run.airflow_dag_inplace_tracking import calc_attempt_key_from_af_ti
from dbnd._core.inplace_run.context_handler import ContextHandler
from dbnd._core.task_run.task_run_logging import safe_short_read_lines
from dbnd._core.utils.uid_utils import get_uuid


def get_or_create_attempt_uid(key):
    env_attempt_uid = os.environ.get(key)
    if env_attempt_uid:
        uid = UUID(env_attempt_uid)
    else:
        task_run_attempt_uid = get_uuid()
        uid = task_run_attempt_uid
        os.environ[key] = str(task_run_attempt_uid)
    return uid


def save_task_log(dbnd_context, task_run, log_file):
    max_size = dbnd_context.settings.log.send_body_to_server_max_size
    max_size = None if max_size == -1 else max_size
    log_body = "\n".join(safe_short_read_lines(log_file, max_size))
    dbnd_context.tracking_store.save_task_run_log(
        task_run=task_run, log_body=log_body, local_log_path=log_file
    )


@contextmanager
def manage_attempt_id(ti):
    task_key = calc_attempt_key_from_af_ti(ti)
    # this can have a side effect of adding the UID to the environ
    uid = get_or_create_attempt_uid(task_key)
    yield uid
    os.environ[task_key] = ""


class DbndAirflowHandler(logging.Handler, ContextHandler):
    """
    This is a logger handler that is used as an Entry Point to airflow run.
    It's injected to the Logger(name="airflow.task"), and used by entering the context on the beginning of the task
    instance run, and getting close when the task instance is done.
    """

    def __init__(self, logger, local_base, log_file_name_factory):
        ContextHandler.__init__(self)
        logging.Handler.__init__(self)

        self.dbnd_context = None
        self.attempt_uid = None

        self.airflow_logger = logger
        self.airflow_base_log_dir = local_base
        self.log_file_name_factory = log_file_name_factory

        self.log_file = ""

    def set_context(self, ti):
        # we are not tracking SubDagOperator
        if ti.operator == SubDagOperator.__name__:
            return

        log_relative_path = self.log_file_name_factory(ti, ti.try_number)
        self.log_file = os.path.join(self.airflow_base_log_dir, log_relative_path)

        self.attempt_uid = self.enter_cm(manage_attempt_id(ti))

        get_dbnd_project_config().quiet_mode = True
        if config.getboolean("mlflow_tracking", "databand_tracking"):
            self.airflow_logger(
                "dbnd can't track mlflow and airflow together please disable dbnd config "
                "`databand_tracking` in section `mlflow_tracking`"
            )
        else:
            self.dbnd_context = self.enter_cm(
                # context with disabled logs
                new_dbnd_context(conf={"log": {"disabled": True}})
            )

    def close(self):
        if self.dbnd_context:
            try:
                fake_task_run = FakeTaskRun(task_run_attempt_uid=self.attempt_uid)
                save_task_log(self.dbnd_context, fake_task_run, self.log_file)
            except Exception:
                self.airflow_logger.exception("Exception occurred when saving task log")

        self.dbnd_context = None
        self.close_all_context_managers()

    def emit(self, record):
        pass


@attr.s
class FakeTaskRun:
    task_run_attempt_uid = attr.ib()


def set_dbnd_handler():
    airflow_logger = logging.getLogger("airflow.task")
    base_file_handler = first_true(
        airflow_logger.handlers,
        pred=lambda handler: handler.__class__.__name__ == "FileTaskHandler",
        default=None,
    )

    if base_file_handler:
        dbnd_handler = create_dbnd_handler(airflow_logger, base_file_handler)
        airflow_logger.addHandler(dbnd_handler)


def create_dbnd_handler(airflow_logger, airflow_file_handler):
    return DbndAirflowHandler(
        logger=airflow_logger,
        local_base=airflow_file_handler.local_base,
        log_file_name_factory=airflow_file_handler._render_filename,
    )
