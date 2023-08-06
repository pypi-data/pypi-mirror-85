__version__ = '0.2.4'


class DarthMailError(Exception):
    def __init__(self, inner, *args):
        self.inner = inner
        super(DarthMailError, self).__init__(inner, *args)

    def __str__(self):
        try:
            return "%s: %s" % (super(DarthMailError, self).__str__(), self.inner.response.content)
        except AttributeError:
            return super(DarthMailError, self).__str__()


class DarthMailDuplicateError(DarthMailError):
    pass
