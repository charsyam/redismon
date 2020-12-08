from apscheduler.schedulers.background import BackgroundScheduler


class Poller:
    _instance = None

    @classmethod
    def _get_instance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._get_instance
        return cls._instance

    def __init__(self):
        self.sched = BackgroundScheduler(daemon=True)
        self.sched.start()

    def add(self, job, interval):
        self.sched.add_job(job,'interval',seconds=interval)
