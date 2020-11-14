import sys
import getopt
from Task import *


class Parser:
    def __init__(self):
        """
        An parser class that allows you to obtain the tasks from the task file and the options chosen to run the
        simulator.
        """
        self.filename = None
        self.heuristic = None
        self.sort = None
        self.limit = None
        self.cores = 1

    def get_options(self):
        """
        Get the options to be used for the simulation

        :return: the options tuple
        """
        return self.heuristic, self.sort, self.limit, self.cores

    def get_tasks(self):
        """
        Get the tasks that have to be scheduled from the task set file

        :return: the list of the tasks
        """
        tasks = []
        f = open(self.filename)
        i = 0
        for line in f:
            value = line.strip().split()
            task = Task(i, int(value[0]), int(value[1]), int(value[2]), int(value[3]))
            tasks.append(task)
            i += 1
        f.close()

        return tasks

    def parse(self, argv):
        """
        Parse the list of arguments obtained from the command line and check if it meets the criteria

        :param argv: the list of the arguments
        """
        self.filename = argv[0]
        try:
            opts, args = getopt.getopt(argv[1:], "h:s:l:m:")
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                if arg not in ["ff", "wf", "bf", "nf"]:
                    print("The -h option can take only one of these values ff|wf|bf|nf")
                    sys.exit()
                else:
                    self.heuristic = arg
            elif opt == '-s':
                if arg not in ["du", "iu"]:
                    print("The -s option can take only one of these values du|iu")
                    sys.exit()
                else:
                    self.sort = arg
            elif opt == '-l':
                if not arg.isdigit():
                    print("The -l option can take only integer values")
                    sys.exit()
                else:
                    self.limit = int(arg)
            elif opt == '-m':
                if not arg.isdigit():
                    print("The -m option can take only integer values")
                    sys.exit()
                else:
                    self.cores = int(arg)
