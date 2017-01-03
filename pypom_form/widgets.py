from .form import BaseFormRegion


class BaseWidgetRegion(BaseFormRegion):
    """
        This is the base widget region associated to a widget.

        You can lookup the base widget region from a page or region
        form with ``page.getWidgetRegion('field_name')`` in order
        to enable advanced widget interactions.

        For example you can get the field label, the help text,
        validation errors or if you have a complex widget you can
        expose the widget API. For example a multi selection widget
        with a filter feature or a reference field with a navigation
        popup with all the portal contents.

        This way you are not only able to set or get field values but
        you can incapsulate complex logics in the widget region and
        expose them on the page or region form ready to be used
    """
    label_selector = ('tag', 'label')

    def get_label(self):
        """ Return the widget label """
        element = self.find_element(*self.label_selector)
        return element and element.value or ''

    def get_help(self):
        """ Return the widget text help """
        raise NotImplementedError

    def get_validation_errors(self):
        """ Return the widget validation error """
        raise NotImplementedError

    def wait_for_region_to_load(self):
        """Wait for the page region to load."""
        if self.root is not None:
            self.wait.until(lambda s: self.root.visible)


class BaseWidget(object):
    """ This is the base widget. It is not intended to be used itself
        but you can use it as base class for your own widgets.

        You can associate widgets on schema level or the form metaclass
        will associate a fallback depending on the schema type if
        ``pypom_widget`` is missing.

        You can provide your own ``region_class`` on the schema definition
        of overriding the ``region_class`` class attribute in your own widget
        implementations.
    """

    region_class = BaseWidgetRegion

    def __init__(self, field=None, region_class=None, options={}):
        self.field = field
        if region_class is not None:
            self.region_class = region_class
        self.options = options

    @property
    def input_selector(self):
        """ Returns the input selector inside the field container.

            Most or times is a tuple with ``('tag', 'input')`` but
            it might change depending on the widget type.

            It's up to you providing the input selector that matches
            your input type.
        """
        raise NotImplementedError

    def get_input_element(self, page):
        """ Return the input element.

            If you provide a selector for the container of the input
            element, it will return the input element itself
            (preferred way if you want to use advanced widget
            features).

            Otherwise the region root will be returned
        """
        region = self.getWidgetRegion(page)
        element = region.find_element(*self.input_selector)
        element = element or element or region.root
        return element

    def getWidgetRegion(self, page):
        """ Returns a dynamic widget region containing the
            root selector.

            This is an internal method used by the page or
            region metaclass in order to be able to expose
            the widget region simply calling
            ``page.getWidgetRegion()``.

            It also sets a reference to the widget itself containing
            the widget options on the widget region.
        """
        region = self.region_class(page)
        region._root_locator = self.field.selector
        region.__pypom_widget__ = self
        return region

    def getter_factory(self):
        """ Returns a generated method to be attached on the
            PyPOM page or region.

            This is an internal method used by the page or
            region metaclass in order to be able to generate
            the getter method for the field.
        """
        raise NotImplementedError

    def setter_factory(self):
        """ Returns a generated method to be attached on the
            PyPOM page or region.

            This is an internal method used by the page or
            region metaclass in order to be able to generate
            the getter method for the field.
        """
        raise NotImplementedError


class StringWidget(BaseWidget):
    """ String widget """

    input_selector = ('tag', 'input')

    def getter_factory(self):
        def _getter(page):
            element = self.get_input_element(page)
            value = element.value
            return self.field.deserialize(value)
        return _getter

    def setter_factory(self):
        def _setter(page, value):
            value = self.field.serialize(value)
            element = self.get_input_element(page)
            element.fill(value)
        return _setter


class TextAreaWidget(StringWidget):
    """ TextArea widget """

    input_selector = ('tag', 'textarea')


class CheckboxWidget(BaseWidget):
    """ Checkbox widget """

    input_selector = ('css', 'input[type="checkbox"]')

    def getter_factory(self):
        def _getter(page):
            element = self.get_input_element(page)
            value = element.checked
            return self.field.deserialize(value)
        return _getter

    def setter_factory(self):
        def _setter(page, value):
            element = self.get_input_element(page)
            if value:
                element.check()
            else:
                element.uncheck()
        return _setter
