from io import open
import re
from functools import cmp_to_key

pattern = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')


def run():
    direct_dependencies = {}
    names = set()
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        match = pattern.fullmatch(line)
        if match is None:
            raise ValueError(line)
        first = match[1]
        second = match[2]
        value = direct_dependencies.get(second, set())
        value.add(first)
        direct_dependencies[second] = value
        names.add(first)
        names.add(second)
    dependencies = Dependencies(names, direct_dependencies).result
    CorrectOrder(names, dependencies).report()
    ParallelProcessing(names, dependencies).report()


class Dependencies:
    def __init__(self, names, direct_dependencies):
        self._names = names
        self._direct_dependencies = direct_dependencies
        self.result = {}
        self._process_names()

    def _process_names(self):
        for name in self._names:
            self._process(name)

    def _process(self, key):
        if key in self.result:
            return self.result[key]
        else:
            all_dependencies = set()
            for value in self._direct_dependencies.get(key, []):
                all_dependencies.add(value)
                all_dependencies.union(self._process(value))
            if key in self.result:
                raise ValueError('Encountered cyclic dependency on ' + str(key))
            self.result[key] = all_dependencies
            return all_dependencies

class CorrectOrder:
    def __init__(self, names, dependencies):
        self._names = names
        self._dependencies = dependencies
        self._initalize_data()
        self._sort()

    def _initalize_data(self):
        self._ordered_names = []
        self._available_names = set(self._names)
        self._fulfilled_dependencies = set()

    def _sort(self):
        while self._available_names:
            ready_names = self._get_ready_names()
            self._ordered_names.append(ready_names[0])
            self._fulfilled_dependencies.add(ready_names[0])
            self._available_names.remove(ready_names[0])

    def _get_ready_names(self):
        result = list(
            filter(lambda x: self._dependencies[x].issubset(self._fulfilled_dependencies),
                   self._available_names))
        result.sort()
        if not result:
            raise ValueError('No ready names found after processing ' + str(self._ordered_names))
        return result

    def report(self):
        print(''.join(self._ordered_names))

class ParallelProcessing:
    def __init__(self, names, dependencies):
        self._names = names
        self._dependencies = dependencies
        self._initalize_data()
        self._jobs: [Job] = [None] * 5
        self._sort()

    def _initalize_data(self):
        self._time_passed = 0
        self._available_names = set(self._names)
        self._fulfilled_dependencies = set()

    def _sort(self):
        while self._available_names:
            ready_names = self._get_ready_names()
            next_name = ready_names[0]
            self._available_names.remove(ready_names[0])
            self._assign_job(next_name)
        longest_job = max(self._jobs, key=lambda job: 0 if job is None else job.time_left)
        if longest_job is not None:
            self._time_passed += longest_job.time_left

    def _get_ready_names(self):
        while True:
            result = list(
                filter(lambda x: self._dependencies[x].issubset(self._fulfilled_dependencies),
                       self._available_names))
            result.sort()
            if result:
                return result
            self._finish_shortest_jobs()

    def _assign_job(self, next_name):
        if self._assign_job_to_empty_slot(next_name):
            return
        self._finish_shortest_jobs()

    def _finish_shortest_jobs(self):
        shortest_job, shortest_job_index = self._shortest_job_with_index()
        self._time_passed += shortest_job.time_left
        jobs_removed = False
        for job, index in self._jobs_with_index():
            if job.time_left > shortest_job.time_left:
                job.time_left -= shortest_job.time_left
            else:
                self._fulfilled_dependencies.add(job.name)
                self._jobs[index] = None
                jobs_removed = True
        if not jobs_removed:
            raise ValueError()

    def _assign_job_to_empty_slot(self, next_name):
        for index in self._job_indexes():
            if self._jobs[index] is None:
                self._jobs[index] = self._create_job(next_name)
                return True
        return False

    def _create_job(self, name):
        return Job(name, self._time_for_job(name))

    def _time_for_job(self, name):
        return 60 + ord(name) - ord('A') + 1

    def _shortest_job_with_index(self):
        return min(self._jobs_with_index(), key=lambda job: job[0].time_left)

    def _jobs_with_index(self):
        result = filter(lambda item: item[0] is not None, zip(self._jobs, self._job_indexes()))
        if not result:
            raise ValueError('No jobs found')
        return result

    def _job_indexes(self):
        return range(0, len(self._jobs))

    def report(self):
        print('Time passed: ' + str(self._time_passed))


class Job:
    def __init__(self, name, time_left):
        self.name = name
        self.time_left = time_left

    def __repr__(self) -> str:
        return 'Job(name: ' + str(self.name) + ', time_left: ' + str(self.time_left) + ')'


run()
