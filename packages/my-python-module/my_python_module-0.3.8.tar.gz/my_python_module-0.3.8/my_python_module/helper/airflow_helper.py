#!/usr/bin/env python
# -*-coding:utf-8-*-


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RunningTaskProgress(Base):
    """
    airflow 正在运行的任务 进度记录，已经运行完了记录将会被删除

    airflow那边正在运行的任务唯一性标识 {dag_id}_{task_id}_{running_id}

    每个任务启动时建立这样一条记录，内部有任务进度计数，积极捕捉异常，异常发生后，

    status 字段里面根据需要保存一些必要的信息，后面的任务运行根据这些必要的信息来决定跳过某些任务处理步骤


    每个任务正常跑完之后，删除本记录
    每个任务启动前，检查时候有目标记录，如果有，则根据 记录跳过一些运算任务。
    """
    __tablename__ = 'running_task_progress'

    id = Column(Integer, primary_key=True)

    airflow_unique_string = Column(String(511), unique=True, nullable=False)

    status = Column(JSON)


def get_airflow_unique_string(kwargs):
    task_instance = kwargs['task_instance']
    run_id = kwargs['run_id']

    unique_string = '{0}_{1}_{2}'.format(task_instance.dag_id,
                                         task_instance.task_id, run_id)
    return unique_string


class StatusRecordHandler(object):
    def __init__(self, airflow_kwargs, session_workflow):
        self.session_workflow = session_workflow

        self.airflow_unique_string = get_airflow_unique_string(airflow_kwargs)
        self.status_record = session_workflow.query(
            RunningTaskProgress).filter_by(
            airflow_unique_string=self.airflow_unique_string).first()

        if self.status_record:
            self.task_status = self.status_record.status
        else:
            self.status_record = RunningTaskProgress(
                airflow_unique_string=self.airflow_unique_string, status={})
            session_workflow.add(self.status_record)
            session_workflow.commit()
            self.task_status = self.status_record.status

    def delete(self):
        self.session_workflow.delete(self.status_record)
        self.session_workflow.commit()

    def update_status(self, status):
        self.status_record.status = status
        self.session_workflow.commit()
