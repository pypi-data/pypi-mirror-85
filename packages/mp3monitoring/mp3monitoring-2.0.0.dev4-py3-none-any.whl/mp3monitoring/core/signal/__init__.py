Signal = None


def choose_signal(use_qt: bool):
    global Signal
    if use_qt:
        from mp3monitoring.core.signal._signal_qt import Signal as SignalQt
        Signal = SignalQt
    else:
        from mp3monitoring.core.signal._signal_no_qt import Signal as SignalNQt
        Signal = SignalNQt
