import asyncio
import signal


class JobProcess:
    def __init__(self, path: str, flags: str = None):
        self.process = None
        self.task = None
        self.path = path
        self.flags = flags
        self.task = asyncio.create_task(self.run_subprocess())

    async def run_subprocess(self):
        # Start the amumax subprocess
        self.process = await asyncio.create_subprocess_exec(
            "amumax",
            self.flags,
            self.path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        print(f"Started amumax (PID: {self.process.pid})")

        # Wait for the process to finish
        stdout, stderr = await self.process.communicate()

        if stdout:
            print(f"[STDOUT]\n{stdout.decode()}")
        if stderr:
            print(f"[STDERR]\n{stderr.decode()}")

        print(f"amumax exited with {self.process.returncode}")

    def stop_process(self):
        if self.task and not self.task.done():
            print("Stopping amumax")
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

    print(job_process.is_running())
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
            print("The amumax task was cancelled")


if __name__ == "__main__":
    asyncio.run(main())
