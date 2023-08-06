import os
import glob
import importlib
import sys
import hashlib
from models.dag import DAG
from models.operator import Operator
import json


class terraform:

    def __init__(self):

        pass

    def create_terraform_configuration(self):

        top_level_dags = self._get_objects(DAG)
        configuration = self._get_terraform_configuration_dags(top_level_dags)

        with open("output/resources.tf.json","w") as file:
            file.write(json.dumps(configuration, indent=4))

    def _get_terraform_configuration_dags(self, dags):

        configurations = []

        for dag in dags:
            configurations.append(dag.get_terraform_json())

            tasks = self._get_objects(Operator)
            dag_tasks = [task for task in tasks if task.dag.dag_id == dag.dag_id]

            for task in dag_tasks:
                configurations.append(task.get_terraform_json())

        return self._combine_configurations(configurations)

    def _get_objects(self, object_type) -> []:

        files = glob.glob("dags/*.py")

        mods = []

        for filepath in files:
            org_mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])
            path_hash = hashlib.sha1(filepath.encode('utf-8')).hexdigest()
            mod_name = f'unusual_prefix_{path_hash}_{org_mod_name}'

            loader = importlib.machinery.SourceFileLoader(mod_name, filepath)
            spec = importlib.util.spec_from_loader(mod_name, loader)
            new_module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = new_module
            loader.exec_module(new_module)
            mods.append(new_module)

        top_level_dags = [
            o
            for m in mods
            for o in list(m.__dict__.values())
            if isinstance(o, object_type)
        ]

        return top_level_dags

    def _combine_configurations(self, configurations: []):

        terraform_configuration = {}

        # List of configurations
        for configuration in configurations:

            # Dict of configuration types (data or resource)
            for configuration_type in configuration:

                # If the configuration type is not yet in the config then add
                if configuration_type not in terraform_configuration:
                    terraform_configuration[configuration_type] = {}

                # List object types (pub_sub_topic, cloud_function)
                for object_type in configuration[configuration_type]:

                    # If object type not yet there then add
                    if object_type not in terraform_configuration[configuration_type]:
                        terraform_configuration[configuration_type][object_type] = {}

                    # List over objects of that type
                    for o in configuration[configuration_type][object_type]:

                        # List over keys of object (just 1 key anyway)
                        for key in o:
                            terraform_configuration[configuration_type][object_type][key] = o[key]

        return terraform_configuration