from typing import List

from mp3monitoring.core.job import Job, JobConfig


class Manager:
    """
    :ivar jobs: We could use a dictionary here, but it is easier to use a List and find a specific Job in it.
                    Also it is not expected to have a lot of _jobs.
    """

    def __init__(self):
        self.jobs: List[Job] = []

    def __len__(self):
        return len(self.jobs)

    def add(self, job: Job):
        self.jobs.append(job)

    def get_configurations(self) -> List[JobConfig]:
        return [job.config for job in self.jobs]

    def remove_by_index(self, index: int):
        job = self.jobs.pop(index)
        job.stop()

    def start(self):
        for job in self.jobs:
            if job.config.run_at_startup:
                job.start()

    def stop(self, join=True):
        for job in self.jobs:
            job.stop(join)

    def join(self):
        for job in self.jobs:
            job.join()
