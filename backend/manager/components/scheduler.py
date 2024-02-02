from schedule import Scheduler
import threading
import warnings
import time


class RepeatTimer(threading.Timer):
    running: bool = False

    def __init__(self, *args, **kwargs):
        threading.Timer.__init__(self, *args, **kwargs)

    def start(self) -> None:
        """Protect from running start method multiple times"""
        if not self.running:
            super(RepeatTimer, self).start()
            self.running = True
        else:
            warnings.warn('Timer is already running, cannot be started again.')

    def cancel(self) -> None:
        """Protect from running stop method multiple times"""
        if self.running:
            super(RepeatTimer, self).cancel()
            self.running = False
        else:
            warnings.warn('Timer is already canceled, cannot be canceled again.')

    def run(self):
        """Replace run method of timer to run continuously"""
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class ThreadedScheduler(Scheduler):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__initialized = False
        return cls._instance

    def __init__(self, run_pending_interval=1.0):
        if self.__initialized:
            return
        self.__initialized = True
        super().__init__()
        self.interval = run_pending_interval
        self._stop_event = threading.Event()  # Flaga do kontrolowania działania wątku
        self.thread = None

    def run_continuously(self):
        """Metoda wykonująca 'run_pending' w pętli, z możliwością zatrzymania."""
        while not self._stop_event.is_set():
            self.run_pending()
            time.sleep(self.interval)

    def start(self):
        try:
            if not self.thread.is_alive():
                self.thread = threading.Thread(target=self.run_continuously, daemon=True)
                self.thread.start()
        except AttributeError:
            self.thread = threading.Thread(target=self.run_continuously, daemon=True)
            self.thread.start()

    def stop(self):
        """Zatrzymaj scheduler, sygnalizując wątkowi, by zakończył działanie."""
        self._stop_event.set()  # Ustawienie flagi zatrzymania
        if self.thread is not None:
            self.thread.join()  # Oczekiwanie na zakończenie wątku

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """Zwróć instancję singletona ThreadedScheduler."""
        return cls(*args, **kwargs)

            
            


# if __name__ == '__main__':
#     my_schedule = ThreadedScheduler(run_pending_interval=1)
#     job1 = my_schedule.every(1).seconds.do(print_work, what_to_say='Did_job1')
#     job2 = my_schedule.every(2).seconds.do(print_work, what_to_say='Did_job2')
#     my_schedule.cancel()
#     my_schedule.start()
#     time.sleep(7)
#     my_schedule.cancel_job(job1)
#     my_schedule.start()
#     time.sleep(7)
#     my_schedule.cancel()