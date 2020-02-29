class Status(object):
    SHUTTING_DOWN = 'Shutting Down'
    RUNNING = 'Running'


class __State(object):
    def __init__(self):
        self._shutting_down = False

    def set_to_shutting_down(self):
        self._shutting_down = True

    def is_shutting_down(self):
        return self._shutting_down

    @property
    def status(self):
        return Status.SHUTTING_DOWN if self.is_shutting_down() else Status.RUNNING


runtime_state = __State()
