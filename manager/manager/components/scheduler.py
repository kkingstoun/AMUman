import logging
import threading
import time

from schedule import Scheduler

log = logging.getLogger("rich")


class RepeatTimer(threading.Timer):
    running: bool = False

    def __init__(self, *args, **kwargs):
        threading.Timer.__init__(self, *args, **kwargs)

    def start(self) -> None:
        """Protect from running start method multiple times"""
        if not self.running:
            super().start()
            self.running = True
        else:
            log.debug("Timer is already running, cannot be started again.")

    def cancel(self) -> None:
        """Protect from running stop method multiple times"""
        if self.running:
            super().cancel()
            self.running = False
        else:
            log.debug("Timer is already canceled, cannot be canceled again.")

    def run(self):
        """Replace run method of timer to run continuously"""
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class ThreadedScheduler(Scheduler):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *_args, **_kwargs):
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
        self._stop_event = threading.Event()
        self.thread = None

    def run_continuously(self):
        while not self._stop_event.is_set():
            self.run_pending()
            log.debug("Scheduler is running")
            time.sleep(self.interval)

    def initiate_thread(self):
        if self.thread is None or not self.thread.is_alive():
            self._stop_event.clear()  # Upewnij się, że flaga stopu jest wyczyszczona
            self.thread = threading.Thread(target=self.run_continuously, daemon=True)
            self.thread.start()

    def start(self):
        self.initiate_thread()

    def stop(self):
        self._stop_event.set()
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)
