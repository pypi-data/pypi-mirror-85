class DummyClass:
    def __init__(self, x):
        """This is a dummy class which can store and manipulate a number"""
        self._x = x

    def add_to_x(self, number=1):
        """
        Adds ``number`` to the stored number.

        Args:
            number (int): The number to add.
        """
        self._x += number

    def get_x(self):
        """
        Returns the stored number.

        Returns:
            int: The stored number.
        """
        return self._x


def dummy_function(x):
    """
    This function adds 1 to a number and returns it.

    This function makes use of :class:`~.DummyClass`.

    Args:
        x (int): The input number.

    Returns:
        int: One plus the input number.
    """
    dc = DummyClass(x)
    dc.add_to_x()
    return dc.get_x()
