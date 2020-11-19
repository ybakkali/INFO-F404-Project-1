import random
import sys
import getopt


def parse(argv):
    """
    Parse the list of arguments obtained from the command line and check if it meets the criteria

    :param argv: the list of the arguments
    """
    if len(argv) == 12:
        output_filename, tasks_number, utilization, limit, offset_type, deadline_type = None, None, None, None, None, None
        try:
            opts, args = getopt.getopt(argv, "t:u:l:o:k:d:")
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-t':
                if not arg.isdigit():
                    print("The -t option can take only integer values")
                    sys.exit(2)
                else:
                    tasks_number = int(arg)
            elif opt == '-u':
                if not arg.isdigit():
                    print("The -u option can take only integer values")
                    sys.exit(2)
                elif not 0 < int(arg) <= 100:
                    print("The -u option value should be in the range ]0,100]")
                    sys.exit(2)
                else:
                    utilization = int(arg)
            elif opt == '-l':
                if not arg.isdigit():
                    print("The -p option can take only integer values")
                    sys.exit(2)
                else:
                    limit = int(arg)
            elif opt == '-k':
                if arg not in ["sync", "async"]:
                    print("The -k option can take only one of these values synchronous or asynchronous")
                    sys.exit(2)
                else:
                    offset_type = arg
            elif opt == '-d':
                if arg not in ["implicit", "constrained", "arbitrary"]:
                    print("The -d option can take only one of these values implicit, constrained or arbitrary")
                    sys.exit(2)
                else:
                    deadline_type = arg
            elif opt == '-o':
                output_filename = arg
        return output_filename, tasks_number, utilization, limit, offset_type, deadline_type
    else:
        print("The command line is incorrect")
        sys.exit(2)


def generate(output_filename, tasks_number, utilization, limit, offset_type, deadline_type):
    """
    Generate a task set file depending on the combination of options

    :param output_filename: the output filename to write in the the task set
    :param tasks_number: the tasks number to generate
    :param utilization: the utilization factor for all the tasks
    :param limit: the maximum value that an offset, a period and a deadline can take
    :param offset_type: the offset type of the tasks
    :param deadline_type: the deadline type of the tasks
    """
    res = ""
    for i in range(tasks_number):
        offset = random.randrange(0, limit, 5) if offset_type == "async" else 0
        period = random.randrange(10, limit, 5)

        if deadline_type == "implicit":
            deadline = period
        elif deadline_type == "constrained":
            deadline = random.randrange(5, period, 5)
        elif deadline_type == "arbitrary":
            deadline = random.randrange(5, limit, 5)

        wcet = int(utilization * period / 100)
        res += "{} {} {} {}\n".format(offset, wcet, deadline, period)

    f = open(output_filename, "w")
    f.write(res[:-1])
    f.close()


if __name__ == '__main__':
    generate(*parse(sys.argv[1:]))
