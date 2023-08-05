import shutil
import threading
import time
import traceback
from pathlib import Path
from threading import Thread
from typing import List

from mp3monitoring import tools
from mp3monitoring.core import signal


class JobConfig:
    """

    :param source_dir: source directory
    :param target_dir: target directory
    :param run_at_startup: run at startup
    :param sleep_time: pause in seconds between the scans
    :param last_check: last modification time
    """

    def __init__(self, source_dir: Path, target_dir: Path, run_at_startup: bool = False, sleep_time: int = 10, recursive: bool = True, last_check: float = 0):
        self.source_dir: Path = source_dir
        self.target_dir: Path = target_dir
        self.run_at_startup: bool = run_at_startup
        self.sleep_time: int = sleep_time
        self.recursive: bool = recursive
        self.last_check: float = last_check

    @classmethod
    def from_dict(cls, j_dict: dict):
        return cls(Path(j_dict['source_dir']), Path(j_dict['target_dir']), run_at_startup=j_dict['run_at_startup'], sleep_time=j_dict['sleep_time'],
                   recursive=j_dict['recursive'], last_check=j_dict['last_check'])

    def to_dict(self) -> dict:
        return {
            'source_dir': str(self.source_dir.resolve()),
            'target_dir': str(self.target_dir.resolve()),
            'run_at_startup': self.run_at_startup,
            'sleep_time': self.sleep_time,
            'recursive': self.recursive,
            'last_check': self.last_check
        }


class Job:
    def __init__(self, config: JobConfig):
        self.config: JobConfig = config

        self._sleep_event: threading.Event = threading.Event()
        self._thread: Thread = None
        self._active: bool = False
        self._status: str = 'stopped'
        self._err_msg: str = ""

        self.status_changed: signal.Signal = signal.Signal()

    def __del__(self):
        self.stop()
        self.status_changed.s_disconnect()

    def __run(self):
        self._active = True
        while True:
            self.status = 'search'
            cur_check: float = time.time()
            mp3_files: List[Path] = []
            if self.config.recursive:
                files = self.config.source_dir.glob('**/*')
            else:
                files = self.config.source_dir.glob('*')
            for file in files:
                # check for ctime and mtime, as it can happen that the ctime is newer than the mtime. (At least on Windows)
                if file.is_file() and (max(file.stat().st_mtime, file.stat().st_ctime) > self.config.last_check) and tools.is_mp3(file):
                    mp3_files.append(file)

            for file in mp3_files:
                try:
                    new_file = self.config.target_dir.joinpath(file.name)
                    new_file = new_file.with_suffix('.mp3')

                    while new_file.exists():
                        new_file = new_file.with_name(new_file.stem + '_d.mp3')

                    shutil.copyfile(file, new_file)
                except Exception:
                    # TODO: call as error
                    traceback.print_exc()

            self.config.last_check = cur_check
            if not self._sleep_event.is_set():
                self.status = 'ok'
            if self._sleep_event.wait(self.config.sleep_time):
                self._sleep_event.clear()
                time.sleep(10)
                self._active = False
                self.status = 'stopped'
                return

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: str):
        self._status = new_status
        self.status_changed.s_emit(-1)

    def start(self):
        if not self.config.source_dir.exists():
            self._err_msg = "Source directory does not exist."
            self.status = 'error'
            return
        elif not self.config.source_dir.is_dir():
            self._err_msg = "Source directory is not a directory."
            self.status = 'error'
            return
        if not self.config.target_dir.exists():
            try:
                Path.mkdir(self.config.target_dir, parents=True)
            except PermissionError:
                self._err_msg = "Cant create target directory. Do you have write permissions?"
                self.status = 'error'
                return
        elif not self.config.target_dir.is_dir():
            self._err_msg = "Target directory is not a directory."
            self.status = 'error'
            return

        source_dir = self.config.source_dir.resolve()
        if self.config.target_dir.resolve() in (source_dir, *source_dir.parents):
            self._err_msg = "Target directory cannot be a sub directory of the source directory."
            self.status = 'error'
            return

        if not self.is_stopping() and not self.is_active():
            self._thread: Thread = Thread(target=self.__run)
            self._thread.start()

    def stop(self, join: bool = True):
        """
        Stop and join the thread.
        :return:
        """
        if self._thread is not None and self._thread.is_alive() and not self.is_stopping():
            self._sleep_event.set()
            self.status = 'stopping'
            if join:
                self._thread.join()

    def join(self):
        if self._thread is not None and self._thread.is_alive():
            self._thread.join()

    def is_stopping(self):
        return self._sleep_event.is_set()

    def is_active(self):
        return self._active

    def tooltip(self):
        if self.status == 'error':
            return "error: " + self._err_msg
        return self.status
