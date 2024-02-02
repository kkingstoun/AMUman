import asyncio
import logging
import signal

from .task import Task

log = logging.getLogger("rich")


class JobProcess:
    def __init__(self, task: Task):
        self.process = None
        self.task = task
        log.debug(f"Starting {task.id=}")
        # asyncio.create_task(self.run_subprocess())

    async def run_subprocess(self):
        log.debug(f"Starting subprocess for {self.task.id=}")
        try:
            self.process = await asyncio.create_subprocess_exec(
                "amumax",
                self.task.path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except Exception as e:
            log.exception(e)

        log.info(f"Started amumax (PID: {self.process.pid})")

        # Wait for the process to finish
        stdout, stderr = await self.process.communicate()

        if stdout:
            log.debug(f"[STDOUT]\n{stdout.decode()}")
        if stderr:
            log.debug(f"[STDERR]\n{stderr.decode()}")

        log.debug(f"amumax exited with {self.process.returncode}")

    def stop_process(self):
        if self.task and not self.task.done():
            log.debug("Stopping amumax")
            self.task.cancel()
            if self.process:
                self.process.send_signal(
                    signal.SIGTERM
                )  # SIGKILL can be used if SIGTERM doesn't work

    def is_running(self):
        return self.task and not self.task.done()


async def main():
    path = "/"
    job_process = JobProcess(path=path)

    log.debug(job_process.is_running())
    # Wait for a few seconds before terminating the process
    await asyncio.sleep(5)

    # Check if the job is running and then stop it
    if job_process.is_job_running():
        job_process.stop_job()

    # Optionally, wait for the task to be cancelled
    if job_process.task:
        try:
            await job_process.task
        except asyncio.CancelledError:
            log.exception("The amumax task was cancelled")
