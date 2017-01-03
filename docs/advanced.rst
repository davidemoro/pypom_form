Advanced
********

Here you can see how to create a custom widget or create your own
colander types with validators.

Encoded values widget
=====================

Let's pretend we have to manage a simple key-value widget:
a sort of dictionary like structure where both keys and values are string types like shown
in the following picture.

  .. image:: images/encoded-values.png


Final interaction with the widget
---------------------------------

For example you might have a ``I set the encoded values field with:`` BDD statement like the
following one::

    @UI @edit @CANBusFamily @encoded
    Scenario: Add a CAN bus family encoded
      Given I am logged in as Administrator
      And I am on the CANBusFamiliesPage page
      When I click on the Add button
      And I fill in the name of the form
      And I set the encoded values field with:
          {"0": "zero", "1": "one"}
      And I submit the form
      Then a success popup message appears

implemented just with::

    @pytest_bdd.when(pytest_bdd.parsers.cfparse(
        'I set the encoded values field with:\n{encoded_values:json}',
        extra_types=dict(json=json.loads)))
    def set_encoded_values(navigation, encoded_values):
        """ Set encoded values """
        navigation.page.encoded_values = encoded_values

On the page instance you can simply set the values you want to apply in one shot::

    page.encoded_values = {'company1': 'Company ONE', 'company2': 'Company TWO'}
    ...

or interact step by step thanks to the widget region::

    page.getWidgetRegion('encoded_values').click_add()
    ...

Final page form setup configuration
-----------------------------------

You can add a new row, delete a row, add a key and a value for each row. If you want you
can also create some validators and contraints to your values.

On the page side we need a schema and a page or region object inheriting from the base classes
provided by ``pypom_form`` with a dictionary like colander type (``Mapping``) and a custom
widget ``EncodedValuesWidget``::

    class MyEditPageSchema(BaseEditSchema):
    
        encoded_values = colander.SchemaNode(
            colander.Mapping(unknown='preserve'),
            selector=('css', '#metric-tabs-2'),
            pypom_widget=EncodedValuesWidget(),
            )
        )
    
    
    class MyEditPage(BaseEditPage):
    
        schema_factory = MyEditPageSchema


Widget implementation
---------------------

And now let's see our pretend custom widget implementation. The widget itself is based on:

* a widget ``EncodedValuesWidget``, it will let you interact with the input elements if you want
  to set a value or read the actual value on the browser (eg: ``{'company1': 'Company 1'}``).
  The widget is internally based on a widget region called ``EncodedValuesWidgetRegion``

* a widget region ``EncodedValuesWidgetRegion``, providing the main logics used by the
  widget itself and available on the page if you want to interact step by step instead of
  assign a whole dictionary like. For example you can add a new row, delete it, change a single
  value or key and so on.
  So you can interact with the ``EncodedValuesWidgetRegion`` like a dictionary: set or get values,
  iterate on them, etc.
  The widget region inner logics are demanded to subregions ``EncodedValueRegion`` (dynamic
  regions) for each row. The subregions controls how to set a key, a value, delete the item row.

* the inner element is the region ``EncodedValueRegion``. They are instanciated dynamically by
  the widget region and they provides a schema_factory containing a ``key`` and a ``value``
  string properties you can interact with

Each key-value pair Here you can see how to create a custom widget, for example a dictionary
like widget with a key and a value (encoded values widget) or create your own

Let's see the resulting code::

    import colander
    from pypom_form.form import BaseFormRegion
    from pypom_form.widgets import (
        BaseWidget,
        BaseWidgetRegion,
    )
    
    
    class EncodedValueRegionSchema(colander.MappingSchema):
        """ EncodedValueRegion schema for encoded values """
    
        key = colander.SchemaNode(
            colander.String(),
            selector=('css', 'input[type="number"]'),
        )
    
        value = colander.SchemaNode(
            colander.String(),
            selector=('css', 'input[type="text"]'),
        )
    
    
    class EncodedValueRegion(BaseFormRegion):
        """ Single encoded value region with key, value and delete button.
    
            This is a subregion returned dynamically by
            the EncodedValuesWidgetRegion for each key-value pair.
    
            Each subregion exposes a key and a value.
    
    
            You can delete subregion instance through the ``delete`` method,
        """
    
        schema_factory = EncodedValueRegionSchema
    
        DELETE_SELECTOR = ('css', '.administration_list_delete')
    
        def delete(self):
            """ Delete region """
            self.find_element(*self.DELETE_SELECTOR).click()
    
    
    class EncodedValuesWidgetRegion(BaseWidgetRegion):
        """ Encoded values widget region
            You can interact with your page using dictionary-like
            operations.
    
            >>> region = page.getWidgetRegion('encoded_values')
            >>> region['0'] = 'ZERO'
            >>> region['0']
    
            You can also iterate on subregions for each key-value pair:
    
            >>> region.encoded_value_regions[0].key = '1'
            >>> region.encoded_value_regions[0].value = 'one'
    
            Or add a new key-value pair without interact:
    
            >>> subregion = region.click_add()
            >>> subregion.key = '1'
            >>> subregion.value = 'ONE'
    
            Access to one key-value pair and interact with it:
    
            >>> region.encoded_value_regions[0].value = 'one'
    
            Or delete a mapping:
    
            >>> del region['0']
        """
    
        REGIONS_ROW_SELECTOR = ('css', 'tbody > tr')
        ADD_BUTTON_SELECTOR = ('css', '.add_button')
    
        def click_add(self):
            """ Click add and returns a subregion """
            previous_len = len(self)
            self.find_element(*self.ADD_BUTTON_SELECTOR).click()
            self.wait.until(lambda s: len(self) == previous_len+1)
            return self.encoded_value_regions[0]
    
        @property
        def encoded_value_regions(self):
            """ Encoded values regions"""
            return [EncodedValueRegion(self, root=root) for root in
                    self.find_elements(*self.REGIONS_ROW_SELECTOR)]
    
        def clear(self):
            """ clear all values """
            for region in self.encoded_value_regions:
                region.delete()
    
        def copy(self):
            values = {}
            for key, value in self.items():
                values[key] = value
            return values
    
        def items(self):
            return [(key, self[key]) for key in self]
    
        def update(self, **values):
            for key, value in values.items():
                self[key] = value
    
        def __getitem__(self, key):
            for region in self.encoded_value_regions:
                if region.key == key:
                    return region.value
            raise KeyError
    
        def __setitem__(self, key, value):
            regions = [item for item in self.encoded_value_regions
                       if item.key == key]
            if not regions:
                regions = [self.click_add()]
            region = regions[0]
            region.value = value
            if region.key != key:
                region.key = key
    
        def __delitem__(self, key):
            self[key].delete()
    
        def __contains__(self, key):
            for key_item in self:
                if key_item == key:
                    return True
            return False
    
        def __len__(self):
            return len(self.encoded_value_regions)
    
        def __iter__(self):
            for region in self.encoded_value_regions:
                yield region.key
    
        def __repr__(self):
            return "%r(%r)" % (self.__class__, self.copy())
    
    
    class EncodedValuesWidget(BaseWidget):
        """ This is the EncodedValuesWidget """
        region_class = EncodedValuesWidgetRegion
    
        def getter_factory(self):
            def _getter(page):
                reg = self.getWidgetRegion(page)
                value = reg.copy()
                return self.field.deserialize(value)
            return _getter
    
        def setter_factory(self):
            def _setter(page, value):
                reg = self.getWidgetRegion(page)
                reg.clear()
                value = self.field.serialize(value)
                reg.update(**value)
            return _setter


Final considerations
--------------------

Now you have a dictionary like edit widget reusable across different page objects sharing
the same data structures powered by regions and subregions. The widget interaction on page
objects empowered by ``pypom_form`` widgets is as easy as dealing with a Python dictionary but
you can also perform custom interactions using the widget region API.

So thanks to ``pypom_form`` widgets you can deal with rich UI widgets hiding the complexity
making things easy for a great development and testing experience.

Extending Colander
==================

We won't cover how to add your own custom colander types or validators, instead
we'll address you to the Colander documentation online:

* http://docs.pylonsproject.org/projects/colander/en/latest/extending.html
