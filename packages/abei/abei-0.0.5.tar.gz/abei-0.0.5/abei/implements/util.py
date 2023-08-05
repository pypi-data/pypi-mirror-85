class FileLikeWrapper(object):
    def __init__(self, file_or_filename):
        if isinstance(file_or_filename, str):
            self.file = open(file_or_filename)
            self.hold = True
        elif hasattr(file_or_filename, 'read'):
            self.file = file_or_filename
            self.hold = False
        else:
            raise TypeError('invalid file type')

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.hold and hasattr(self.file, 'close'):
            self.file.close()


class LazyProperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        value = self.func(instance)
        setattr(instance, self.func.__name__, value)
        return value
