import pytest
import mock


def test_base_widget_1():
    """ Assert widget is None """
    from pypom_form.widgets import BaseWidget

    widget = BaseWidget()
    assert widget.field is None


def test_base_widget_2():
    """ Assert kwargs are stored """
    from pypom_form.widgets import BaseWidget

    widget = BaseWidget(kwargs={'test': 1})
    assert widget.kwargs['test'] == 1


def test_base_widget_3():
    """ Assert getter method is required """
    from pypom_form.widgets import BaseWidget

    widget = BaseWidget()
    assert callable(widget.getter_factory)
    with pytest.raises(NotImplementedError):
        widget.getter_factory()


def test_base_widget_4():
    """ Assert setter method is required """
    from pypom_form.widgets import BaseWidget

    widget = BaseWidget()
    assert callable(widget.setter_factory)
    with pytest.raises(NotImplementedError):
        widget.setter_factory()


def test_string_widget_1():
    """ Assert getter is implemented """
    from pypom_form.widgets import StringWidget
    import colander

    widget_class = StringWidget

    mock_field = colander.SchemaNode(
        colander.String(),
        selector=('id', 'id1'),
    )

    widget = widget_class(field=mock_field)
    get_input_element_mock = mock.MagicMock()
    get_input_element_mock.configure_mock(**{
        'return_value.value': 'test ok'})
    widget.get_input_element = get_input_element_mock
    getter = widget.getter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.getter = property(fget=getter)
    assert page_mock.getter == 'test ok'


def test_string_widget_2():
    """ Assert setter is implemented """
    from pypom_form.widgets import StringWidget
    import colander

    widget_class = StringWidget

    mock_field = colander.SchemaNode(
        colander.String(),
        selector=('id', 'id1'),
    )

    widget = widget_class(field=mock_field)
    get_input_element_mock = mock.MagicMock()
    widget.get_input_element = get_input_element_mock
    setter = widget.setter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.setter = property(fset=setter)
    page_mock.setter = 'test ok'
    assert get_input_element_mock. \
        return_value.fill.assert_called_once_with('test ok') is None


def test_checkbox_widget_1():
    """ Assert getter is implemented """
    from pypom_form.widgets import CheckboxWidget
    import colander

    widget_class = CheckboxWidget

    mock_field = colander.SchemaNode(
        colander.Bool(),
        selector=('id', 'id1'),
    )

    widget = widget_class(field=mock_field)
    get_input_element_mock = mock.MagicMock()
    get_input_element_mock.configure_mock(**{
        'return_value.checked': True})
    widget.get_input_element = get_input_element_mock
    getter = widget.getter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.getter = property(fget=getter)

    assert page_mock.getter is True


def test_checkbox_widget_2():
    """ Assert setter is implemented. Set True, True """
    from pypom_form.widgets import CheckboxWidget
    import colander

    widget_class = CheckboxWidget

    mock_field = colander.SchemaNode(
        colander.Bool(),
        selector=('id', 'id1'),
    )

    widget = widget_class(field=mock_field)
    get_input_element_mock = mock.MagicMock()
    widget.get_input_element = get_input_element_mock
    setter = widget.setter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.setter = property(fset=setter)

    page_mock.setter = True
    # let's set True twice
    page_mock.setter = True

    assert get_input_element_mock. \
        return_value.check.call_count == 2
    assert get_input_element_mock. \
        return_value.uncheck.call_count == 0


def test_checkbox_widget_3():
    """ Assert setter is implemented. Set True, False """
    from pypom_form.widgets import CheckboxWidget
    import colander

    widget_class = CheckboxWidget

    mock_field = colander.SchemaNode(
        colander.Bool(),
        selector=('id', 'id1'),
    )

    widget = widget_class(field=mock_field)
    get_input_element_mock = mock.MagicMock()
    widget.get_input_element = get_input_element_mock
    setter = widget.setter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.setter = property(fset=setter)

    page_mock.setter = True
    # let's set False now
    page_mock.setter = False

    assert get_input_element_mock. \
        return_value.check.call_count == 1
    assert get_input_element_mock. \
        return_value.uncheck.call_count == 1


def test_integer_widget_1():
    """ Assert getter is implemented """
    from pypom_form.widgets import StringWidget
    import colander

    widget_class = StringWidget

    mock_field = colander.SchemaNode(
        colander.Int(),
        selector=('id', 'id1'),
    )
    widget = widget_class(field=mock_field)
    get_input_element_mock = mock.MagicMock()
    get_input_element_mock.configure_mock(**{
        'return_value.value': '1'})
    widget.get_input_element = get_input_element_mock
    getter = widget.getter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.getter = property(fget=getter)
    assert page_mock.getter == 1


def test_integer_widget_2():
    """ Assert setter is implemented """
    from pypom_form.widgets import StringWidget
    import colander

    widget_class = StringWidget

    mock_field = colander.SchemaNode(
        colander.Int(),
        selector=('id', 'id1'),
    )
    get_input_element_mock = mock.MagicMock()
    widget = widget_class(field=mock_field)
    widget.get_input_element = get_input_element_mock
    setter = widget.setter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.setter = property(fset=setter)
    page_mock.setter = 1
    assert get_input_element_mock. \
        return_value.fill.assert_called_once_with('1') is None


def test_float_widget_1():
    """ Assert getter is implemented """
    from pypom_form.widgets import StringWidget
    import colander

    widget_class = StringWidget

    mock_field = colander.SchemaNode(
        colander.Float(),
        selector=('id', 'id1'),
    )
    widget = widget_class(field=mock_field)
    get_input_element_mock = mock.MagicMock()
    get_input_element_mock.configure_mock(**{
        'return_value.value': '-1.1'})
    widget.get_input_element = get_input_element_mock
    getter = widget.getter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.getter = property(fget=getter)
    assert page_mock.getter == -1.1


def test_float_widget_2():
    """ Assert setter is implemented """
    from pypom_form.widgets import StringWidget
    import colander

    widget_class = StringWidget

    mock_field = colander.SchemaNode(
        colander.Float(),
        selector=('id', 'id1'),
    )
    get_input_element_mock = mock.MagicMock()
    widget = widget_class(field=mock_field)
    widget.get_input_element = get_input_element_mock
    setter = widget.setter_factory()
    page_mock = mock.MagicMock()
    page_mock.__class__.setter = property(fset=setter)
    page_mock.setter = -1.1
    assert get_input_element_mock. \
        return_value.fill.assert_called_once_with('-1.1') is None


def test_region_widget_not_implemented(browser):
    """ Region widget """
    import colander

    from pypom_form.widgets import StringWidget

    class MyStringWidget(StringWidget):
        pass

    class BaseFormSchema(colander.MappingSchema):
        title = colander.SchemaNode(colander.String(),
                                    selector=('id', 'id1'))

    class SubFormSchema(BaseFormSchema):
        name = colander.SchemaNode(colander.String(),
                                   selector=('id', 'id2'),
                                   pwidget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)

    from pypom_form.widgets import BaseWidgetRegion
    widget_region = BaseWidgetRegion(subform)

    with pytest.raises(NotImplementedError):
        widget_region.get_help()
    with pytest.raises(NotImplementedError):
        widget_region.get_validation_errors()


def test_region_widget_get_label(browser):
    """ Region widget """
    import colander

    from pypom_form.widgets import StringWidget

    class MyStringWidget(StringWidget):
        pass

    class BaseFormSchema(colander.MappingSchema):
        title = colander.SchemaNode(colander.String(),
                                    selector=('id', 'id1'))

    class SubFormSchema(BaseFormSchema):
        name = colander.SchemaNode(colander.String(),
                                   selector=('id', 'id2'),
                                   pwidget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)

    from pypom_form.widgets import BaseWidgetRegion
    widget_region = BaseWidgetRegion(subform)

    widget_region.find_element = mock.MagicMock(**{
        'return_value.value': 'title'})
    assert widget_region.get_label() == 'title'
