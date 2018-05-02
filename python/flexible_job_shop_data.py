class Task():
    '''
    A task is the basic block of a jobshop.
    '''

    def __init__(self, job_id, machines, durations):
        self.job_id = job_id        # Job ID
        self.machines = machines    # Int vector
        self.durations = durations  # Int vector
        self.out = ''

    def debug_string(self):
        ''' 
        Generate debug string: 
        machines with its corresponding durations
        '''
        self.out = [(m, durations[m]) for m in machines if m > 0]


class FlexibleShopJob():
    '''
    A FlexibleJobShopData parses data files and stores all data internally for
    easy retrieval.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = ''
        self.machine_count = ''
        self.job_count = ''
        self.horizon = ''
        self.all_tasks = ''
        self.current_job_index = ''
        self.task = ''

    def load(self, file):
        '''
        Parses a file in .fjp format and loads the model. Note that the format is
        only partially checked: bad inputs might cause undefined behavior.
        '''
        self.process_new_line(file)

    def process_new_line(self, file):
        '''
        Process lines of the .fjp format
        '''
        words = []
        for line in open(file, 'r'):
            words.append(line)

        if (self.machine_count == -1 and len(words) > 1):
            self.job_count = words[0]
            self.machine_count = words[1]

        elif (len(words) > 1):
            operations_count = words[0]
            index = 1
            for operations in operations_count:
                machines = []
                durations = []
                alternatives_count = words[index]
                for a in alternatives_count:
                    # Machine id are 1 based.
                    machines.append(words[index])
                    durations.append(words[index])
                self.add_task(self.current_job_index, machines, durations)

    def add_task(self, job_id, machines, durations):
        self.all_tasks[job_id].append(Task(job_id, machines, durations))
        self.horizon = self.sum_of_durations(durations)

    def machine_count(self):
        return self.machine_count

    def job_count(self):
        return self.job_count

    def name(self):
        return self.name

    def tasks_of_job(self, job_id):
        return self.all_tasks[job_id]

    def sum_of_durations(self, durations):
        result = 0
        for d in durations:
            result += durations[d]
        return result
