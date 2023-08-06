from unittest import TestCase
from operators.python_operator import PythonOperator
from models.dag import DAG


class TestOperatorDependencies(TestCase):

    def get_dag(self):

        default_args = {}

        return DAG(
            dag_id="test_dag",
            description="Test DAG",
            default_args=default_args,
            schedule_interval="0 * * * *"
        )

    def get_task(self,*,task_id,dag):

        def test(arg):
            pass

        return PythonOperator(
            dag=dag,
            task_id=task_id,
            description="Test task",
            python_callable=test,
            op_kwargs={'arg': 'great test'},
            requirements=["pandas==1.0.0", "pandas_gbq==0.14.0"]
        )

    def test_upstream_setting(self):

        dag = self.get_dag()
        test_task = self.get_task(task_id='test_task',dag=dag)
        test_task2 = self.get_task(task_id='test_task2',dag=dag)

        test_task.set_upstream(test_task2)

        upstream_tasks = test_task.upstream_tasks
        downstream_tasks = test_task2.downstream_tasks

        self.assertEqual("test_task2", upstream_tasks[0])
        self.assertEqual("test_task", downstream_tasks[0])

    def test_upstream_lshift_setting(self):

        dag = self.get_dag()
        test_task = self.get_task(task_id='test_task',dag=dag)
        test_task2 = self.get_task(task_id='test_task2',dag=dag)

        test_task << test_task2

        upstream_tasks = test_task.upstream_tasks
        downstream_tasks = test_task2.downstream_tasks

        self.assertEqual("test_task2", upstream_tasks[0])
        self.assertEqual("test_task", downstream_tasks[0])

    def test_downstream_setting(self):

        dag = self.get_dag()
        test_task = self.get_task(task_id='test_task',dag=dag)
        test_task2 = self.get_task(task_id='test_task2',dag=dag)

        test_task.set_downstream(test_task2)

        downstream_tasks = test_task.downstream_tasks
        upstream_tasks = test_task2.upstream_tasks

        self.assertEqual("test_task2", downstream_tasks[0])
        self.assertEqual("test_task", upstream_tasks[0])

    def test_downstream_rshift_setting(self):

        dag = self.get_dag()
        test_task = self.get_task(task_id='test_task',dag=dag)
        test_task2 = self.get_task(task_id='test_task2',dag=dag)

        test_task >> test_task2

        downstream_tasks = test_task.downstream_tasks
        upstream_tasks = test_task2.upstream_tasks

        self.assertEqual("test_task2", downstream_tasks[0])
        self.assertEqual("test_task", upstream_tasks[0])

