class Job:
    def __init__(self, task, k):
        """

        :param task:
        :param k:
        """
        self.task = task
        self.id = "T{}J{}".format(task.id, k)
        self.offset = task.offset + (k - 1) * task.period
        self.wcet = task.wcet
        self.deadline = task.offset + (k - 1) * task.period + task.deadline
        self.state = "Undone"
        self.time_remaining = self.wcet
        self.finished = -1

    def __str__(self):
        return self.id + "\noffset {}\nWCET {}\ndeadline {}".format(self.offset, self.wcet, self.deadline)

    def get_task(self):
        """

        :return:
        """
        return self.task

    def get_id(self):
        """

        :return:
        """
        return self.id

    def get_offset(self):
        """
        Get the job offset

        :return: the job offset
        """
        return self.offset

    def get_deadline(self):
        """
        Get the job deadline

        :return: the job deadline
        """
        return self.deadline

    def get_state(self):
        """

        :return:
        """
        return self.state

    def get_cumulative_time(self):
        """

        :return:
        """
        return self.wcet - self.time_remaining

    def set_state(self, state):
        """

        :param state:
        """
        self.state = state

    def is_deadline_met(self):
        """

        :return:
        """
        return self.finished + 1 <= self.deadline

    def decrease(self):
        """

        """
        self.time_remaining -= 1

    def handler(self, t):
        """

        :param t:
        """
        self.task.set_oldest_active_job(self)
        if self.state == "Undone":
            self.state = "Running"
            self.task.increase_active_jobs()
        if self.time_remaining == 0:
            self.set_state("Done")
            self.finished = t
            self.task.decrease_active_jobs()
            if self.task.get_oldest_active_job().get_id() == self.id:
                self.task.set_oldest_active_job(None)
