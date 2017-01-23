"""
From https://github.com/Kotti/Kotti/blob/master/kotti/views/form.py
"""
import colander


def is_readonly(field):
    """
        Returns True if the given field is readonly, otherwise False.

        Field readonly (True)
        ---------------------

        >>> from mock import MagicMock
        >>> field = MagicMock()
        >>> field.readonly = True
        >>> assert field.readonly is True

        >>> is_readonly(field) is True
        True

        Field readonly (False)
        ----------------------

        >>> field.readonly = False
        >>> assert field.readonly is False

        >>> is_readonly(field) is False
        True

        Field readonly (default: False)
        -------------------------------

        >>> field = object()
        >>> from pytest import raises
        >>> with raises(AttributeError):
        ...     field.readonly

        >>> is_readonly(field) is False
        True
    """
    return getattr(field, 'readonly', False)


class ObjectType(colander.SchemaType):
    """ A type leaving the value untouched.
    """

    @staticmethod
    def serialize(node, value):
        return value

    @staticmethod
    def deserialize(node, value):
        return value
