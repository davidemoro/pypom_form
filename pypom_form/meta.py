from collections import OrderedDict

import colander


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


def _getWidgetRegion(self, name):
    """ Return the widget region for the given name"""
    return self.__pypom__[name].pypom_widget.getWidgetRegion(self)


def _set(self, name, value):
    """ Set value for the given name with chained calls support """
    setattr(self, name, value)
    return self


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
            dct['getWidgetRegion'] = _getWidgetRegion
            dct['set'] = _set

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

        return type.__new__(cls, clsname, bases, dct)
