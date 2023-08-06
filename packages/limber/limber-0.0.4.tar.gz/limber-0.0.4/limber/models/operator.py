

class Operator:

    def __init__(self):
        self.downstream_tasks = []
        self.upstream_tasks = []

    def __lshift__(self, task2):
        """Implements Task << Task"""
        self.set_upstream(task2)

    def __rshift__(self, task2):
        """Implements Task >> Task"""
        self.set_downstream(task2)

    def set_upstream(self, task):

        self.set_relative(task=task, upstream=True)
        task.set_relative(task=self, upstream=False)

    def set_downstream(self, task):

        self.set_relative(task=task, upstream=False)
        task.set_relative(task=self, upstream=True)

    def set_relative(self, *, task, upstream):

        if upstream:
            self.upstream_tasks.append(task.task_id)
        else:
            self.downstream_tasks.append(task.task_id)