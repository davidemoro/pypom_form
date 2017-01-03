import pytest
import mock


def test_base_widget_1():
    """ Assert widget is None """
    from pypom_form.widgets import BaseWidget

    widget = BaseWidget()
    assert widget.field is None


def test_base_widget_2():
    """ Assert options are stored """
    from pypom_form.widgets import BaseWidget

    widget = BaseWidget(options={'test': 1})
    assert widget.options['test'] == 1


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


def test_textarea_widget_1():
    """ Assert getter is implemented """
    from pypom_form.widgets import TextAreaWidget
    import colander

    widget_class = TextAreaWidget

    mock_field = colander.SchemaNode(
        colander.String(),
        selector=('id', 'id1'),
        pypom_widget=TextAreaWidget(),
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


def test_textarea_widget_2():
    """ Assert setter is implemented """
    from pypom_form.widgets import TextAreaWidget
    import colander

    widget_class = TextAreaWidget

    mock_field = colander.SchemaNode(
        colander.String(),
        selector=('id', 'id1'),
        pypom_widget=TextAreaWidget(),
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
                                       options={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)

    from pypom_form.widgets import BaseWidgetRegion

    with mock.patch(
            'pypom_form.widgets.BaseWidgetRegion.wait_for_region_to_load') \
            as wait_for_region_to_load:
        wait_for_region_to_load.configure_mock(**{'return_value': None})

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
                                       options={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)

    from pypom_form.widgets import BaseWidgetRegion

    with mock.patch(
            'pypom_form.widgets.BaseWidgetRegion.wait_for_region_to_load') \
            as wait_for_region_to_load:
        wait_for_region_to_load.configure_mock(**{'return_value': None})

        widget_region = BaseWidgetRegion(subform)

    widget_region.find_element = mock.MagicMock(**{
        'return_value.value': 'title'})
    assert widget_region.get_label() == 'title'


def test_widget_base_region_class():
    from pypom_form.widgets import BaseWidget
    from pypom_form.widgets import BaseWidgetRegion

    assert BaseWidget.region_class == BaseWidgetRegion

    widget = BaseWidget()

    assert widget.region_class == BaseWidgetRegion


def test_widget_base_region_class_custom():
    from pypom_form.widgets import BaseWidget
    import pypom

    widget = BaseWidget(region_class=pypom.Region)

    assert widget.region_class == pypom.Region


def test_widget_base_input_selector_raises():
    from pypom_form.widgets import BaseWidget

    widget = BaseWidget()

    with pytest.raises(NotImplementedError):
        widget.input_selector


def test_widget_string_input_selector():
    from pypom_form.widgets import StringWidget

    widget = StringWidget()

    assert widget.input_selector == ('tag', 'input')


def test_widget_checkbox_input_selector():
    from pypom_form.widgets import CheckboxWidget

    widget = CheckboxWidget()

    assert widget.input_selector == ('css', 'input[type="checkbox"]')


def test_widget_region_root_selector(browser):
    from pypom_form.widgets import BaseWidget
    from pypom_form.widgets import BaseWidgetRegion

    assert BaseWidget.region_class == BaseWidgetRegion

    field = mock.MagicMock(**{'selector': ('id', 'xyz')})
    widget = BaseWidget(field=field)
    import pypom
    page = pypom.Page(browser)

    with mock.patch(
            'pypom_form.widgets.BaseWidgetRegion.wait_for_region_to_load') \
            as wait_for_region_to_load:
        wait_for_region_to_load.configure_mock(**{'return_value': None})

        assert widget.getWidgetRegion(page)._root_locator == ('id', 'xyz')


def test_widget_region_widget_reference(browser):
    from pypom_form.widgets import BaseWidget
    from pypom_form.widgets import BaseWidgetRegion

    assert BaseWidget.region_class == BaseWidgetRegion

    field = mock.MagicMock(**{'selector': ('id', 'xyz')})
    widget = BaseWidget(field=field)
    import pypom
    page = pypom.Page(browser)

    with mock.patch(
            'pypom_form.widgets.BaseWidgetRegion.wait_for_region_to_load') \
            as wait_for_region_to_load:
        wait_for_region_to_load.configure_mock(**{'return_value': None})

        assert widget.getWidgetRegion(page).__pypom_widget__ == widget


def test_get_input_element(browser):
    from pypom_form.widgets import StringWidget

    widget = StringWidget()
    widget.getWidgetRegion = mock.MagicMock(
        **{'return_value.find_element.return_value': 'element'})
    import pypom
    page = pypom.Page(browser)
    widget.get_input_element(page) == 'element'


def test_get_input_element_no_container(browser):
    from pypom_form.widgets import StringWidget

    widget = StringWidget()
    widget.getWidgetRegion = mock.MagicMock(
        **{'return_value.find_element.return_value': None,
           'return_value.root': 'root'})
    import pypom
    page = pypom.Page(browser)
    widget.get_input_element(page) == 'root'


def test_widget_region_wait_timeout(browser):
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
                                       options={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)
    subform.timeout = 0

    from pypom_form.widgets import BaseWidgetRegion

    with mock.patch(
            'pypom_form.widgets.BaseWidgetRegion.root') \
            as root:
        root.configure_mock(**{'visible': False})

        from selenium.common.exceptions import TimeoutException
        with pytest.raises(TimeoutException):
            BaseWidgetRegion(subform)


def test_widget_region_wait_not_timeout(browser):
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
                                       options={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)
    subform.timeout = 0

    from pypom_form.widgets import BaseWidgetRegion

    with mock.patch(
            'pypom_form.widgets.BaseWidgetRegion.root') \
            as root:
        root.configure_mock(**{'visible': True})

        BaseWidgetRegion(subform)
