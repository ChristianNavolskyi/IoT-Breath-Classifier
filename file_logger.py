from logging import Logger, INFO, Formatter, FileHandler


class FileLogger(Logger):
    def __init__(self, name, file):
        Logger.__init__(self, name=name, level=INFO)
        formatter = Formatter("%(asctime)s [{0}] %(message)s".format(name))
        handler = FileHandler(file)
        handler.setFormatter(formatter)
        self.addHandler(handler)
