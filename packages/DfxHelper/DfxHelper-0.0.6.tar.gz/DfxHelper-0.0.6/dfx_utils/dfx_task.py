from threading import Timer, Event, Lock


class DfxTimer(Timer):

    def __init__(self, interval, function, callback=None, args=None, kwargs=None):
        self.callback = callback
        super(DfxTimer, self).__init__(interval, function, args=args, kwargs=kwargs)

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            result = self.function(*self.args, **self.kwargs)
            self.callback(result)
        self.finished.set()


class DfxExecutor:

    def __init__(self, name, interval, function, callback=None, args=None, kwargs=None):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.interval = interval
        self.function = function
        self.callback = callback
        self.finished = Event()

    def __start(self, _callback):
        DfxTimer(self.interval, self.function, _callback, self.args, self.kwargs).start()

    def run(self):
        def inline_callback(result):
            if self.callback:
                self.callback(result)
            DfxExecutorManager.cancel(self.name)

        if not self.finished.is_set():
            self.__start(inline_callback)

    def run_cycle(self):
        def inline_callback(result):
            if self.callback:
                self.callback(result)
            if not self.finished.is_set():
                self.__start(inline_callback)
            else:
                DfxExecutorManager.cancel(self.name)

        if not self.finished.is_set():
            self.__start(inline_callback)

    def cancel(self):
        self.finished.set()

    def is_finished(self):
        return self.finished.is_set()


class DfxExecutorManager:
    Executors = dict()
    ManagerLock = Lock()

    @classmethod
    def get_executor(cls, name, interval, function, callback=None, args=None, kwages=None):
        executor = DfxExecutor(name, interval, function, callback, args, kwages)
        cls.Executors[name] = executor
        return executor

    @classmethod
    def cancel(cls, name):
        with cls.ManagerLock:
            if name in cls.Executors:
                cls.Executors[name].cancel()
                del cls.Executors[name]

    @classmethod
    def check_state(cls, name):
        with cls.ManagerLock:
            if name in cls.Executors:
                return cls.Executors[name].is_finished()