import json
from pathlib import Path
from typing import List

from mp3monitoring.core.job import JobConfig

SETTINGS_VERSION = "1"


class Settings:
    def __init__(self):
        self.file: Path = Path.home().joinpath(".mp3monitoring/config.json")

        self.ignore_config: bool = False

        self.start_minimized: bool = False
        self.start_with_system: bool = False

    @classmethod
    def from_dict(cls, file: Path, j_dict: dict):
        settings = cls()
        settings.file = file
        settings.start_minimized = j_dict.get('start_minimized', settings.start_minimized)
        settings.start_with_system = j_dict.get('start_with_system', settings.start_with_system)
        return settings

    def to_dict(self):
        return {
            'start_minimized': self.start_minimized,
            'start_with_system': self.start_with_system,
        }


def load_old_config(file: Path) -> List[JobConfig]:
    if not file.is_file():
        return []
    jobs: List[JobConfig] = []
    with file.open(encoding='utf-8') as reader:
        j_dict: dict = json.load(reader)
    for job in j_dict['jobs']:
        jobs.append(JobConfig(job['source_dir'], job['target_dir'], run_at_startup=job['startup'], sleep_time=job['pause'], last_check=job['last_mod_time']))
    file.unlink()
    return jobs


def load_config(file: Path = Path.home().joinpath(".mp3monitoring/config.json")) -> (Settings, List[JobConfig]):
    load_old_config(file.parent.joinpath('data.sav'))

    if not file.exists():
        file.parent.mkdir(exist_ok=True, parents=True)
        return Settings(), []

    with file.open(encoding='utf-8') as reader:
        j_dict: dict = json.load(reader)

    if 'meta' not in j_dict:
        raise ValueError("Missing 'meta'.")
    elif 'version' not in j_dict['meta']:
        raise ValueError("Missing 'meta.version'.")

    if j_dict['meta']['version'] == "1":
        settings = Settings.from_dict(file, j_dict['settings'])
        jobs = [JobConfig.from_dict(cur_conf) for cur_conf in j_dict['jobs']]
        return settings, jobs
    else:
        raise ValueError(f"Cannot handle 'meta.version' value '{j_dict['meta']['version']}'")


def save_config(settings: Settings, jobs: List[JobConfig]):
    if not settings.file.exists():
        settings.file.parent.mkdir(exist_ok=True, parents=True)

    json_dict = {
        'meta': {'version': SETTINGS_VERSION},
        'jobs': [job.to_dict() for job in jobs],
        'settings': settings.to_dict(),
    }

    with settings.file.open('w', encoding='utf-8') as writer:
        json.dump(json_dict, writer, indent=4)
