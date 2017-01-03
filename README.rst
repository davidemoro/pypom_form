pypom_form
**********

.. image:: https://travis-ci.org/tierratelematics/pypom_form.svg?branch=master
       :target: https://travis-ci.org/tierratelematics/pypom_form

.. image:: https://requires.io/github/tierratelematics/pypom_form/requirements.svg?branch=master
       :target: https://requires.io/github/tierratelematics/pypom_form/requirements/?branch=master

.. image:: https://readthedocs.org/projects/pypom_form/badge/?version=latest
       :target: http://pypom_form.readthedocs.io

.. image:: https://codecov.io/gh/tierratelematics/pypom_form/branch/master/graph/badge.svg
       :target: https://codecov.io/gh/tierratelematics/pypom_form

.. image:: https://api.codacy.com/project/badge/Grade/0698c7aa2e164ee996518737aad7d6f4
       :target: https://www.codacy.com/app/davide-moro/pypom_form?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tierratelematics/pypom_form&amp;utm_campaign=Badge_Grade
       
.. image:: https://pyup.io/repos/github/tierratelematics/pypom_form/python-3-shield.svg
     :target: https://pyup.io/repos/github/tierratelematics/pypom_form/
     :alt: Python 3


``pypom_form`` is a PyPOM based package that provides declarative schema based form interaction for page objects.

pypom_form aims to improve the developer experience for UI, E2E test automation when you
have to interact with page object containing forms thanks to declarative schema models.

If you come from past experience with frameworks like `SQLAlchemy`_, Dexterity (`Plone`_) or the old Archetypes (`Plone`_)
you should be already familiar with this pattern: you simply define a model with a schema and you will be able to
interact with your model saving or retrieving data.
Same happens with pypom_form where the model is the page.

pypom_form it is internally based on:

* `PyPOM`_
* `colander`_
* `Splinter`_

How does it work?
=================

Whith pypom_form you have just to:

* instanciate a page object instance whose class inherits from BaseFormPage provided by pypom_form
* declare the schema model

And you will be ready for interacting with your page driving the browser with your form just typing::

    page.title = 'the title'
    page.title

assuming that you have a ``title`` field in your form.

Main concepts
-------------

You might think about the ``schema`` concept as a set of named attributes (``fields``) that will be
available on the ``model`` as regular properties.

Each ``field`` on the schema is defined with a ``type`` (eg: string, int, float, datetime, date, bool, etc)
that defines the data type for the given field on the application domain level.

Fields has a reference to a ``widget`` defined imperatively or assigned by default depending on the field
type.
The inner implementation of widgets provided by pypom_form is based on PyPOM's Regions, so ``widget regions``
wraps and manage a DOM containing the widget.

Basically the widget translates data from the applicative domain to the browser domain and vice versa
through serialization and deserialization.

You might thing about a widget as how you have to driver your browser when you set ``True`` to a boolean
property or get the actual value on the form: basically it depends on the widget implementation. For example
you might have a checkbox, yes/no radio buttons or combo select, etc and if you want to set ``True`` the
way you drive the browser changes. Same for date widgets and so on.

You might have to deal with complex widgets too like:

* reference widgets (eg: hierarchical content navigation with search, filtering, etc)
* advanced multi selection widgets
* dictionary widgets (key value mapping)
* etc

For example, assuming you are dealing with a pretend advanced single selection choice field you can
access to advanced logics provided by the ``widget region``::

    page.getWidgetRegion('state').filter('virg').select('Virginia')

or access to validation error messages, label text, etc.

Why pypom_form
--------------

Obviously you can drive your browser in automated tests with plain selenium/splinter or with a traditional
plain page object model pattern but with pypom_form you have the following advantages:

* write once and reusable approach, very useful if you are testing CMS framework
* separation of concerns for page and widget logics
* declarative schema approach
* reusable schema and widgets, no code repetition
* widgets can be shared with other projects using pypom_form
* simple API based on auto generated getter and setters
* interact with advanced widget logics thanks to PyPOM based region widgets
* widget isolation. All element queries run against the root region, not the page root
* simpler input elements selectors, they are relative to the region widget root
* schema forms improves how you document page containing forms (attributes names, type, widgets,
  allowed vocabularies, etc). All you need to know is defined at schema level with the whole picture
  available at a glance
* reuse of existing schemas if you are going to test a colander/deform based application (probably
  you are testing a Pylons `Pyramid`_ Python based web application)
* page and schema inheritance supported as well
* easy test multi skin web applications with same data model, same or different selectors or widget
  types. So you can reuse all your page object classes as they are defined, it changes only the schema
  widget selector adn widget types
* widget regions are PyPOM regions, so if you want to access inner elements inside the widget container
  the resulting selectors will be simpler because they are relative to the widget region root.
  Also sub/nested regions or dynamic regions are supperted as well
* interact with your model with applicative domain data instead of browser domain data. It is more
  simple and easy to manage Python data (for example you set 12.9 instead of '12.9', same for datetimes
  values like ``datetime.now()``)
* supports chained calls like ``page.set('title', 'the title')``
* supports bulk field updates considering the order defined at schema level via ``page.update(**values)``
* don't reinvent the wheel. It is based on existing and widely used components like the plain PyPOM or
  Colander libraries
* same user experience if you are already familiar with schema declarative models like ``SQLAlchemy``,
  ``Archetypes`` (Plone), ``Dexterity`` (Plone) or form libraries like ``deform``
* since widget implementation is based on regions, you can simply perform a ``page.name = "the name"``
  on page load instead of having to call a wait method before setting the value:
  the widget is able to wait for the widget load before getting or setting data
* page objects classes more simple, with less code, more standard even if different test engineers will
  implement page form logics: there is a structural pattern

In addition:

* 100% test coverage
* both Python 2 and 3 support
* supports Splinter drivers (Selenium support not yet available)
* pytest setup ready thanks to ``pytest-splinter``

Code samples
============

The following code samples assumes that there is a navigation fixture providing the page instance
built with a Splinter driver but you can build by yourself a page instance following
the PyPOM documentation:

* http://pypom.readthedocs.io/en/latest/

Schema definition::

    import colander
    
    from pypom_form.form import BaseFormPage
    
    
    class BaseEditSchema(colander.MappingSchema):
        """ This is the base edit mapping common for all pages """
    
        name = colander.SchemaNode(
            colander.String(),
            selector=('id', 'name-widget'),
        )
    
    
    class BaseEditPage(BaseFormPage):
        """ This is the base edit class """
    
        schema_factory = BaseEditSchema

And assuming you have a page instance you can interact with the above page
just setting an attribute::

    @pytest_bdd.when(pytest_bdd.parsers.parse(
        'I set {name} as name field'))
    def fill_name(navigation, name):
        page = navigation.page
        page.name = name

You can also define other pages with extended schema, for example an integer
type::

    class AnotherPageEditSchema(BaseEditSchema):
    
        duration = colander.SchemaNode(
            colander.Int(),
            missing=0,
            selector=('id',
                      'duration-widget'),
            validator=colander.Range(0, 9999))

but you can create also field types like ``colander.Bool`` or any other colander
supported types.

And the test::

    @pytest_bdd.when(pytest_bdd.parsers.cfparse(
        'I set {duration:Number} as Alarm duration',
        extra_types=dict(Number=int)))
    def fill_alarm_duration(navigation, duration):
        page = navigation.page
        page.duration = duration

You might notice that in the above example you are setting an integer duration
and not a string. So you can perform ``page.duration += 10`` for example. 

You can also define custom widgets on fields if the default implementation does
not match the one available on your application (for example a non standard
checkbox for a boolean widget), for example a pretend ``MyBooleanWidget``::

    mybool = colander.SchemaNode(
        colander.Bool(),
        missing=False,
        selector=(
            'id',
            'mybool-widget'
        ),
        pypom_widget=MyBoolWidget()
    )

Also chained calls are supported (eg: set the title, perform the pretend submit method
and then set a boolean)::

    page.set('title', 'the title'). \
        .submit(). \
        .set('mybool', False)

or bulk updates. All changes occurs following the fields order at schema level::

    page.update(**{'title': 'the title', 'mybool': True})

The ``update`` or ``raw_update`` can be used in test preconditions creation.
Assuming you have a generic given step with parametrized with a complex configuration
you can pass the raw json data and the ``raw_update`` will take care about the
data conversion from browser model (eg: string) to the page model (strings, integers,
datetimes, etc)::

    @pytest_bdd.given(pytest_bdd.parsers.cfparse(
        'I have a CAN bus protocol configured with:\n{raw_conf:json}',
        extra_types=dict(json=json.loads)))
    def create_can_protocol(navigation, base_url, raw_conf):
        """ create a can protocol
        """

        navigation. \
            visit_page('CANBusProtocolsPage'). \
            wait_for_full_spinner(). \
            click_add(). \
            raw_update(**raw_conf). \
            save(). \
            wait_for_success_pop_up_appears(). \
            click_on_ok_pop_up()

assuming that the ``raw_conf`` is specified in json format in
the ``.feature`` file, for example::

    @UI @edit @CANBusParameter
    Scenario: Add a CAN bus parameter
      Given I am logged in as Administrator
      And I have a CAN bus protocol configured with:
          {"name": "The name",
           "baudrate": "250",
           ...
          }
      And ...

As you can see in the above code examples there is no need to perform wait calls before
interacting with a form on page load because each widget is able to wait until its
controlled input element is ready. Wait logics are already defined on widget level and
you can override them.


.. _PyPOM: http://pypom.readthedocs.io
.. _colander: http://docs.pylonsproject.org/projects/colander/en/latest/
.. _Splinter: https://splinter.readthedocs.io/en/latest/
.. _Plone: https://plone.org/
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _Pyramid: https://trypyramid.com/
