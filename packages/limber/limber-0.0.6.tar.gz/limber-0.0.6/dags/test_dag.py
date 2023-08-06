from models.dag import DAG
from operators.python_operator import PythonOperator
from datetime import timedelta
import pandas


default_args = {

}

test_dag = DAG(
    dag_id="test_dag",
    description="DAG that will for now just create a Google cloud scheduler",
    default_args=default_args,
    schedule_interval="0 * * * *"
)


def test(arg):
    import pandas as pd
    from datetime import datetime

    df = pd.DataFrame([[datetime.now(), arg]], columns=["current_timestamp", "message"])
    df.to_gbq("test_dataset.test_table", if_exists="append")


test_task = PythonOperator(
    dag=test_dag,
    task_id="test_task",
    description="Test task",
    python_callable=test,
    op_kwargs={'arg': 'great test'},
    requirements=["pandas==1.0.0", "pandas_gbq==0.14.0"]
)


# Use an array as output to call task 3 two times
def test_multiple_outputs(arg):
    return ["test1", "test2"]


test_task2 = PythonOperator(
    dag=test_dag,
    task_id="test_task2",
    description="Test task2",
    python_callable=test_multiple_outputs,
    op_kwargs={'arg': 'great test2'},
    requirements=["pandas==1.0.0", "pandas_gbq==0.14.0"]
)

test_task3 = PythonOperator(
    dag=test_dag,
    task_id="test_task3",
    description="Test task3",
    python_callable=test,
    op_kwargs={'arg': 'great test3'},
    requirements=["pandas==1.0.0", "pandas_gbq==0.14.0"]
)

test_task >> test_task2

test_task2 >> test_task3
