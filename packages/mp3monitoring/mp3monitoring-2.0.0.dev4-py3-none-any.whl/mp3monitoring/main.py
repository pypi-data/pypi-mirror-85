"""
Entry into the program.
"""
import signal
import sys
import threading
import time
from argparse import ArgumentParser
from pathlib import Path

from mp3monitoring import static_data
from mp3monitoring.core.job import JobConfig, Job
from mp3monitoring.core.manager import Manager
from mp3monitoring.core.settings import load_config, Settings, save_config
from mp3monitoring.core.signal import choose_signal


def arg_parse(argv):
    parser = ArgumentParser(prog=static_data.LONG_NAME, description=static_data.DESCRIPTION)
    parser.add_argument('-v', '--version', action='version', version=f"{static_data.NAME} {static_data.VERSION}")

    parser.add_argument('-j', '--job', dest='job_list', nargs=3, action='append', metavar=('source', 'target', 'sleep'),
                        help='Will add this job to the monitor list.')
    parser.add_argument('--reset_times', dest='reset_times', default=False, action='store_true',
                        help='Reset the latest check time from configuration.')
    parser.add_argument('--ignore_config', dest='ignore_config', default=False, action='store_true',
                        help='Will not load or save the config file.')
    parser.add_argument('--gui', dest='gui', default=False, action='store_true',
                        help='Open the gui.')

    args = parser.parse_args(argv)
    if args.reset_times and args.ignore_config:
        parser.error("--reset_times and --ignore_config are mutually to each other.")

    return args


def main(argv=None):
    """
    Entry point into the program. Gets the arguments from the console and proceed them with :class:`~argparse.ArgumentParser`.
    Returns if its success successful 0 else 1.
    """
    if sys.version_info[0] < 3 or sys.version_info[1] < 8:
        sys.exit('Only Python 3.8 or greater is supported. You are using:' + sys.version)

    if argv is None:
        argv = sys.argv[1:]
    args = arg_parse(argv)
    choose_signal(args.gui)

    settings: Settings = Settings()
    settings.ignore_config = args.ignore_config
    manager: Manager = Manager()

    if not args.ignore_config:
        settings, configs = load_config()
        for config in configs:
            manager.add(Job(config))
    # add other jobs
    if args.job_list is not None:
        for job_cfg in args.job_list:
            manager.add(Job(JobConfig(Path(job_cfg[0]), Path(job_cfg[1]), True, int(job_cfg[2]))))

    if args.reset_times:
        for job in manager.jobs:
            job.config.last_check = 0

    manager.start()

    if not args.gui:
        stop_event: threading.Event = threading.Event()

        def signal_handler(sig, frame):
            stop_event.set()

        signal.signal(signal.SIGINT, signal_handler)
        while not stop_event.is_set():
            time.sleep(1)

        manager.stop()
        if not settings.ignore_config:
            save_config(settings, manager.get_configurations())
        sys.exit(0)
    else:
        from mp3monitoring.gui.window.main import MainWindow
        try:
            from PySide2.QtWidgets import QApplication
        except ImportError:
            print('PySide2 is not installed, you can not use the gui.')
            return
        app: QApplication = QApplication([])
        MainWindow(app, settings, manager)  # will call show in it's constructor
        sys.exit(app.exec_())


def main_gui(argv=None):
    if sys.version_info[0] < 3 or sys.version_info[1] < 8:
        sys.exit('Only Python 3.8 or greater is supported. You are using:' + sys.version)

    if argv is None:
        argv = sys.argv[1:]
    argv.append('--gui')
    main(argv)
