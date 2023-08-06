import os
from models.operator import Operator
import inspect
import zipfile

class PythonOperator(Operator):

    def __init__(self, *, dag, task_id, description, python_callable, op_kwargs, requirements: []):
        super().__init__()

        self.dag = dag
        self.task_id = task_id
        self.description = description
        self.python_callable = python_callable
        self.op_kwargs = op_kwargs
        self.requirements = requirements

    def _write_cloud_function_code(self):

        code = inspect.getsource(self.python_callable)

        code += "\ndef cloudfunction_execution(event, context):\n"\
                f"    outputs = {self.python_callable.__name__}({self.op_kwargs})\n"\
                f"\n    if outputs is None:\n"\
                f"        outputs = ['done']\n"\
                f"\n    topic_name = 'task_{self.dag.dag_id}_{self.task_id}'\n"\


        pubsub_code = inspect.getsourcelines(self._write_to_pub_sub_code)
        code += "\n    def call_pub_sub(message, topic_name):\n"
        code += "".join(pubsub_code[0][1:])

        code += "\n    for output in outputs:\n"
        code += "        call_pub_sub(output, topic_name)\n"

        main = f"output/{self.dag.dag_id}/{self.task_id}/main.py"
        os.makedirs(os.path.dirname(main), exist_ok=True)

        with open(main, "w") as file:
            file.write(code)

        requirements = f"output/{self.dag.dag_id}/{self.task_id}/requirements.txt"

        self.requirements.extend(["google-cloud","google-cloud-pubsub"])

        with open(requirements,"w") as file:
            file.write("\n".join(self.requirements))

    def _write_to_pub_sub_code(self, message, topic_name):
        from google.cloud import pubsub_v1
        import json

        PROJECT_ID = 'serverless-etl-test'
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, topic_name)
        message_json = json.dumps({'data': {'message': message},})
        message_bytes = message_json.encode('utf-8')
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()

    def get_terraform_json(self) -> {}:

        self._write_cloud_function_code()

        source_dir = f"{self.dag.dag_id}/{self.task_id}"
        file_path = f"{self.dag.dag_id}/{self.task_id}.zip"

        if len(self.upstream_tasks) > 0:
            trigger_resource = f"task_{self.dag.dag_id}_{self.upstream_tasks[0]}"
        else:
            trigger_resource = f"dag_{self.dag.dag_id}"

        configuration = {
            "data": {
                "archive_file": [{
                    f"task_{self.task_id}": {
                        "type": "zip",
                        "source_dir": source_dir,
                        "output_path": file_path
                    }
                }]
            },
            "resource": {
                "google_storage_bucket_object": [{
                    f"task_{self.task_id}": {
                        "name": file_path+"#${data.archive_file.task_"+self.task_id+".output_md5}",
                        "bucket": "${google_storage_bucket.bucket.name}",
                        "source": file_path
                    }
                }],
                "google_cloudfunctions_function": [{
                    f"function_{self.task_id}": {
                        "name": f"{self.dag.dag_id}-{self.task_id}",
                        "description": self.description,
                        "runtime": "python38",
                        "available_memory_mb": 256,
                        "service_account_email": os.environ["SERVICE_ACCOUNT_EMAIL"],
                        "source_archive_bucket": "${google_storage_bucket.bucket.name}",
                        "source_archive_object": "${google_storage_bucket_object.task_"+self.task_id+".name}",
                        "event_trigger": {
                            "event_type": "providers/cloud.pubsub/eventTypes/topic.publish",
                            "resource": trigger_resource
                        },
                        "entry_point": "cloudfunction_execution"
                    }
                }],
                "google_pubsub_topic": [{
                    f"task_{self.dag.dag_id}_{self.task_id}": {
                        "name": f"task_{self.dag.dag_id}_{self.task_id}"
                    }
                }]
            }
        }

        return configuration