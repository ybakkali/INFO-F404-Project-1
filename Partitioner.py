from Scheduler import EDFScheduler


class Partition:
    def __init__(self, id):
        """

        :param id:
        """
        self.id = id
        self.tasks = []
        self.utilization = 0

    def __str__(self):
        res = ""
        for task in self.tasks:
            res += "Task {},".format(task.id)
        return "Partition {} : ".format(self.id) + res[:-1]

    def add_task(self, task):
        """

        :param task:
        """
        self.tasks.append(task)
        self.utilization += task.get_utilization()

    def remove_task(self):
        """

        """
        task = self.tasks.pop()
        self.utilization -= task.get_utilization()

    def get_utilization(self):
        """

        :return:
        """
        return self.utilization

    def get_tasks(self):
        """

        :return:
        """
        return self.tasks


class Partitioner:
    def __init__(self, tasks, cores):
        """

        :param tasks:
        :param cores:
        """
        self.tasks = tasks
        self.cores = cores
        self.partitions = [Partition(i + 1) for i in range(cores)]
        self.last_core_used = 0
        self.can_be_partitioned = False

    def run(self, sort, heuristic, limit):
        """

        :param sort:
        :param heuristic:
        :param limit:
        """
        self.sort_tasks(sort)

        if heuristic == "ff":
            self.first_fit(limit)
        elif heuristic == "wf":
            self.worst_fit(limit)
        elif heuristic == "bf":
            self.best_fit(limit)
        elif heuristic == "nf":
            self.next_fit(limit)

        if self.can_be_partitioned:
            for partition in self.partitions:
                if partition.get_utilization() > 0:
                    print(partition)
                    scheduler = EDFScheduler(partition.get_tasks())
                    scheduler.run(limit)
                    print()
        else:
            print("Cannot be partitioned")

    def sort_tasks(self, sort):
        """

        :param sort:
        """
        if sort == "du":
            self.tasks.sort(key=lambda task: task.utilization, reverse=True)
        else:
            self.tasks.sort(key=lambda task: task.utilization)

    def sort_cores(self, sort):
        """

        :param sort:
        """
        if sort == "bf":
            self.partitions.sort(key=lambda partition: partition.utilization, reverse=True)
        else:
            self.partitions.sort(key=lambda partition: partition.utilization)

    def can_be_placed(self, task, limit):
        """

        :param task:
        :param limit:
        :return:
        """
        for it in range(self.cores):
            self.last_core_used = it
            self.partitions[it].add_task(task)
            scheduler = EDFScheduler(self.partitions[it].get_tasks())
            is_accepted = scheduler.is_scheduling(limit)
            task.reset()
            if not is_accepted:
                self.partitions[it].remove_task()
                it += 1
            else:
                return True
        return False

    def first_fit(self, limit):
        """

        :param limit:
        """
        for task in self.tasks:
            self.can_be_partitioned = self.can_be_placed(task, limit)

    def worst_fit(self, limit):
        """

        :param limit:
        """
        for task in self.tasks:
            self.can_be_partitioned = self.can_be_placed(task, limit)
            self.sort_cores("wf")

    def best_fit(self, limit):
        """

        :param limit:
        """
        for task in self.tasks:
            self.can_be_partitioned = self.can_be_placed(task, limit)
            self.sort_cores("bf")

    def next_fit(self, limit):
        """

        :param limit:
        """
        for task in self.tasks:
            self.can_be_partitioned = self.can_be_placed(task, limit)
