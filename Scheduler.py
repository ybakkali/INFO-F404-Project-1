from math import lcm
from operator import attrgetter


class EDFScheduler:
    def __init__(self, tasks):
        """

        :param tasks:
        """
        self.tasks = tasks
        self.O_max = 0
        self.P = None

        self.get_o_max()
        self.get_p()

    def sort_all_jobs(self, limit):
        """

        :param limit:
        :return:
        """
        jobs = []
        for task in self.tasks:
            task.init_jobs(limit)
            jobs += task.get_jobs()
        return sorted(jobs, key=attrgetter('deadline', 'offset'))

    def get_o_max(self):
        """

        """
        for task in self.tasks:
            if self.O_max < task.get_offset():
                self.O_max = task.get_offset()

    def get_p(self):
        """

        """
        period_list = []
        for task in self.tasks:
            period_list.append(task.get_period())
        self.P = lcm(*period_list)

    def are_deadlines_valid(self):
        """

        :return:
        """
        for task in self.tasks:
            for job in task.get_jobs():
                if not job.is_deadline_met(): # job.get_deadline() not in range(0, self.O_max + 2 * self.P + 1)
                    return False
        return True

    def configuration(self, t, task):
        """

        :param t:
        :param task:
        :return:
        """
        if t >= task.get_offset():
            gamma = (t - task.get_offset()) % task.get_period()
        else:
            gamma = t - task.get_offset()

        alpha = task.get_active_jobs()

        beta = 0 if alpha == 0 else task.get_oldest_active_job().get_cumulative_time()

        return gamma, alpha, beta

    def get_configurations(self, t):
        """

        :param t:
        :return:
        """
        return [self.configuration(t, task) for task in self.tasks]

    def is_scheduling(self, limit):
        """

        :param limit:
        :return:
        """
        t1 = self.O_max + self.P
        t2 = self.O_max + self.P * 2
        jobs = self.sort_all_jobs(limit)
        for t in range(0, limit + 1):
            if t == t1:
                conf1 = self.get_configurations(t1)
            elif t == t2:
                conf2 = self.get_configurations(t2)
                if conf1 != conf2:
                    return False

            is_selected = False
            it = 0
            while not is_selected and jobs and it < len(jobs):
                job = jobs[it]
                if job.get_offset() <= t and job.get_offset() < limit and job.get_state() != "Done":
                    job.decrease()
                    job.handler(t)
                    if job.get_state() == "Done":
                        jobs.pop(it)
                    is_selected = True

                it += 1
        return self.are_deadlines_valid()

    def run(self, limit):
        """

        :param limit:
        """
        jobs = self.sort_all_jobs(limit)
        for t in range(0, limit + 1):
            is_selected = False
            it = 0
            while not is_selected and jobs and it < len(jobs):
                job = jobs[it]
                if job.get_offset() <= t and job.get_offset() < limit and job.get_state() != "Done":
                    print("Time unit {} : ".format(t) + job.get_id())
                    job.decrease()
                    job.handler(t)
                    if job.get_state() == "Done":
                        jobs.pop(it)
                    is_selected = True

                it += 1
            if not is_selected:
                print("Time unit {} : ".format(t))
