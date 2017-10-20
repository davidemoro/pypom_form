from collections import OrderedDict

import colander

from .fields import is_readonly


def _widgets_mapping():
    """ circular import issues """
    from .widgets import (
        StringWidget,
        CheckboxWidget,
    )

    # typ -> default widget mapping
    WIDGETS_MAPPING = {
        colander.String: StringWidget,
        colander.Bool: CheckboxWidget,
        colander.Int: StringWidget,
        colander.Float: StringWidget,
    }
    return WIDGETS_MAPPING


class PyPOMFormMixin(object):

    def getWidgetRegion(self, name):
        """ Return the widget region for the given name"""
        return self.__pypom__[name].pypom_widget.getWidgetRegion(self)

    def set(self, name, value):
        """ Set value for the given name with chained calls support """
        field = self.__pypom__[name]
        if is_readonly(field) is not True:
            setattr(self, name, value)
        return self

    def update(self, **values):
        """ Bulk page update with chained calls support.
            Updates fields considering the PyPOM fields order in order
            to support edit forms with fields that depends on other
            fields.
        """
        value_keys = values.keys()
        pypom_values = self.__pypom__.items()
        pypom_keys = map(lambda item: item[0], pypom_values)

        if not set(value_keys) <= set(pypom_keys):
            raise KeyError

        # values must be a subset of the available declared fields
        for key, node in pypom_values:
            # set values with the specific order matching with the
            # schema definition
            if key in value_keys and is_readonly(node) is not True:
                self.set(key, values[key])

        return self

    def dump(self):
        """ Dumps all fields. """
        return {key: getattr(self, key) for key in self.__pypom__.keys()}

    def raw_update(self, **raw_values):
        """ Bulk page update with chained calls support.
            Updates fields with raw values (not deserialized)
            considering the PyPOM fields order in order
            to support edit forms with fields that depends on other
            fields.
        """
        schema = self.schema_factory()
        values = schema.deserialize(raw_values)
        return self.update(**values)

    def raw_dump(self):
        """ Dumps all fields in raw serialized format. """
        schema = self.schema_factory()
        values = self.dump()
        return schema.serialize(values)


class PyPOMFormMetaclass(type):
    """ This is the metaclass that empower the page or region
        form with dynamically generated getter and setter
        attributes depending on the declarative schema.

        Thanks to this metaclass you are able to set or access
        values driving your browser with ``page.title = 'title'``
        or ``page.title``.

        It add a ``getWidgetRegion`` method if you want to
        look up a region widget for advanced widget interactions
        accessing to region widget methods.
    """

    def __new__(cls, clsname, bases, dct):
        schema_factory = dct.get('schema_factory', None)

        if schema_factory:
            dct['__pypom__'] = OrderedDict()

            schema = schema_factory()
            WIDGETS_MAPPING = _widgets_mapping()

            for child in schema.children:
                widget = getattr(child, 'pypom_widget', None)
                if widget is None:
                    typ = child.typ
                    widget_factory = WIDGETS_MAPPING[typ.__class__]
                    child.pypom_widget = widget_factory(field=child)
                else:
                    # set the field reference
                    child.pypom_widget.field = child

                dct[child.name] = property(
                    fget=child.pypom_widget.getter_factory(),
                    fset=child.pypom_widget.setter_factory())

                dct['__pypom__'][child.name] = child

        # avoid TypeError: Cannot create a consistent method resolution
        # order (MRO) for bases ... since we have to support
        # multiple inheritance.
        # Otherwise with (PyPOMFormMixin,) + bases we get a MRO error
        new_base = type(
            PyPOMFormMixin.__name__,
            (PyPOMFormMixin,),
            {})

        return type.__new__(cls, clsname, (new_base,) + bases, dct)
