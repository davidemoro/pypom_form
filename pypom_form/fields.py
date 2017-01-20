"""
From https://github.com/Kotti/Kotti/blob/master/kotti/views/form.py
"""
import colander


class ObjectType(colander.SchemaType):
    """ A type leaving the value untouched.
    """

    @staticmethod
    def serialize(node, value):
        return value

    @staticmethod
    def deserialize(node, value):
        return value
