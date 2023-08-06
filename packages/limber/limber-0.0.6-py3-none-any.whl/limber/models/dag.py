from typing import Optional
from datetime import timedelta


class DAG:

    def __init__(self, dag_id:str, description:Optional[str], default_args:dict, schedule_interval:[str,timedelta]):

        self.dag_id = dag_id
        self.description=description
        self.default_args=default_args
        self.schedule_interval=schedule_interval

        pass

    def get_terraform_json(self) -> {}:

        configuration = {
            "resource": {
                "google_pubsub_topic": [{
                    f"dag_{self.dag_id}": {
                        "name": f"dag_{self.dag_id}"
                    }
                }], "google_cloud_scheduler_job": [{
                    f"job_{self.dag_id}": {
                        "name": self.dag_id,
                        "description": self.description,
                        "schedule": self.schedule_interval,
                        "pubsub_target": {
                            "topic_name": "${google_pubsub_topic.dag_" + self.dag_id + ".id}",
                            "data": "dGVzdA=="
                        }
                    }
                }]
            }
        }

        return configuration