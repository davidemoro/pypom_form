

def test_meta_form_page(browser):
    """ test metaclass with pypom form page"""
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)
    import mock

    with mock.patch(
            'pypom_form.widgets.StringWidget.get_input_element') \
            as get_input_element:
        get_input_element.configure_mock(**{'return_value.value': 'the title'})
        assert subform.title == 'the title'

    with mock.patch(
            'pypom_form.widgets.StringWidget.get_input_element') \
            as get_input_element:
        get_input_element.configure_mock(**{'return_value.value': 'the name'})
        assert subform.name == 'the name'


def test_meta_form_region(browser):
    """ test metaclass with pypom form region"""
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    import pypom
    from pypom_form.form import BaseFormRegion

    class SubFormRegion(BaseFormRegion):
        schema_factory = SubFormSchema

    subform = SubFormRegion(pypom.Page(browser))
    import mock

    with mock.patch(
            'pypom_form.widgets.StringWidget.get_input_element') \
            as get_input_element:
        get_input_element.configure_mock(**{'return_value.value': 'the title'})
        assert subform.title == 'the title'

    with mock.patch(
            'pypom_form.widgets.StringWidget.get_input_element') \
            as get_input_element:
        get_input_element.configure_mock(**{'return_value.value': 'the name'})
        assert subform.name == 'the name'


def test_pypom_inner_attribute_form_page(browser):
    """ test pypom inner attribute """
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)

    assert subform.__pypom__
    assert 'title' in subform.__pypom__
    assert 'name' in subform.__pypom__
    assert list(subform.__pypom__.keys()) == ['title', 'name']
    assert isinstance(subform.__pypom__['title'], colander.SchemaNode)
    assert isinstance(subform.__pypom__['name'], colander.SchemaNode)


def test_pypom_inner_attribute_form_region(browser):
    """ test pypom inner attribute """
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)

    assert subform.__pypom__
    assert 'title' in subform.__pypom__
    assert 'name' in subform.__pypom__
    assert list(subform.__pypom__.keys()) == ['title', 'name']
    assert isinstance(subform.__pypom__['title'], colander.SchemaNode)
    assert isinstance(subform.__pypom__['name'], colander.SchemaNode)


def test_meta_form_page_widget_region(browser):
    """ test metaclass with pypom form page"""
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)

    import mock

    with mock.patch(
            'pypom_form.widgets.BaseWidgetRegion.wait_for_region_to_load') \
            as wait_for_region_to_load:
        wait_for_region_to_load.configure_mock(**{'return_value': None})

        title_region = subform.getWidgetRegion('title')
        name_region = subform.getWidgetRegion('name')

        from pypom_form.widgets import BaseWidgetRegion
        assert isinstance(title_region, BaseWidgetRegion)
        assert isinstance(name_region, BaseWidgetRegion)


def test_meta_form_region_widget_region(browser):
    """ test metaclass with pypom form page"""
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    import pypom
    from pypom_form.form import BaseFormRegion

    class SubFormRegion(BaseFormRegion):
        schema_factory = SubFormSchema

    subform = SubFormRegion(pypom.Page(browser))
    title_region = subform.getWidgetRegion('title')
    name_region = subform.getWidgetRegion('name')

    from pypom_form.widgets import BaseWidgetRegion
    assert isinstance(title_region, BaseWidgetRegion)
    assert isinstance(name_region, BaseWidgetRegion)


def test_mixed_page_region(browser):
    """ Test mixed/nested page and region """
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    from pypom_form.form import BaseFormRegion

    class SubFormRegion(BaseFormRegion):
        schema_factory = SubFormSchema

    region = SubFormRegion(SubFormPage(browser))

    assert region.getWidgetRegion('title') != \
        region.page.getWidgetRegion('title')
    assert region.getWidgetRegion('name') != \
        region.page.getWidgetRegion('name')


def test_mixed_page_region_page_reference(browser):
    """ Test mixed/nested page and region """
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
                                   pypom_widget=MyStringWidget(
                                       kwargs={'test': 1}))

    from pypom_form.form import BaseFormPage

    class SubFormPage(BaseFormPage):
        schema_factory = SubFormSchema

    from pypom_form.form import BaseFormRegion

    class SubFormRegion(BaseFormRegion):
        schema_factory = SubFormSchema

    page = SubFormPage(browser)
    region = SubFormRegion(page)

    assert region.page == page
    assert region.getWidgetRegion('title').page == \
        region
    assert page.getWidgetRegion('title').page == \
        page
