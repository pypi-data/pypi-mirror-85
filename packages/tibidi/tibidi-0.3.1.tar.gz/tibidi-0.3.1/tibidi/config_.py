
class config:
    """Settings of *tibidi* module.
    """

    debug = False
    """Don't suppress exceptions raised by tibidi."""

    islegal = lambda obj: True
    """Check if given object is picklable."""

    def __init__(self):
        raise NotImplementedError
