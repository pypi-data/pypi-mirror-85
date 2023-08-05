from importlib import resources
from pathlib import Path

with resources.path('mp3monitoring.gui.pkg_data', 'icon.svg') as p:
    LOGO_ICON = Path(p)

with resources.path('mp3monitoring.gui.pkg_data.symbols', 'error.svg') as p:
    ERROR_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'ok.svg') as p:
    OK_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'search.svg') as p:
    SEARCH_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'stopped.svg') as p:
    STOPPED_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'wait.svg') as p:
    WAIT_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'wait_animated.svg') as p:
    WAIT_ANIMATED_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'warning.svg') as p:
    WARNING_SYMBOL = Path(p)

with resources.path('mp3monitoring.gui.pkg_data.symbols', 'add.svg') as p:
    ADD_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'remove.svg') as p:
    REMOVE_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'start.svg') as p:
    START_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'stop.svg') as p:
    STOP_SYMBOL = Path(p)

with resources.path('mp3monitoring.gui.pkg_data.symbols', 'info.svg') as p:
    INFO_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'settings.svg') as p:
    SETTINGS_SYMBOL = Path(p)
with resources.path('mp3monitoring.gui.pkg_data.symbols', 'power.svg') as p:
    POWER_SYMBOL = Path(p)
