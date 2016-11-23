==========
pypom_form
==========

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



``pypom_form`` is a PyPOM based package that provides declarative schema based form interaction for page objects.

pypom_form aims to improve the developer experience for UI, E2E test automation when you
have to interact with page object containing forms thanks to declarative schema models.

If you come from past experience with frameworks like SQLAlchemy, Dexterity (Plone) or the old Archetypes (Plone)
you should be already familiar with this pattern: you simply define a model with a schema and you will be able to
interact with your model saving or retrieving data.
Same happens with pypom_form where the model is the page.

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

* separation of concerns for page and widget logics
* declarative schema approach
* reusable schema and widgets, no code repetition
* widgets can be shared with other projects using pypom_form
* simple API based on auto generated getter and setters
* interact with advanced widget logics thanks to PyPOM based region widgets
* widget isolation. All element queries run against the root region, not the page root
* schema forms improves how you document page containing forms (attributes names, type, widgets,
  allowed vocabularies, etc). All you need to know is defined at schema level with the whole picture
  available at a glance
* reuse of existing schemas if you are going to test a colander/deform based application (probably
  you are testing a Pylons/Pyramid Python based web application)
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
* don't reinvent the wheel. It is based on existing and widely used components like the plain PyPOM or
  Colander libraries
* same user experience if you are already familiar with schema declarative models like ``SQLAlchemy``,
  ``Archetypes`` (Plone), ``Dexterity`` (Plone) or form libraries like ``deform``
* since widget implementation is based on regions, you can simply perform a ``page.name = "the name"``
  on page load instead of having to call a wait method: the widget is able to wait for the widget load
  before getting or setting data (not yet implemented)
* page objects classes more simple, with less code, more standard even if different test engineers will
  implement page form logics: there is a structural pattern

In addition:

* 100% test coverage
* both Python 2 and 3 support
* supports both Selenium (not yet implemented) or Splinter drivers
* pytest setup ready thanks to ``pytest.selenium`` or ``pytest.splinter``


It is internally based on:

* `PyPOM`_
* `colander`_


.. _PyPOM: http://pypom.readthedocs.io
.. _colander: http://docs.pylonsproject.org/projects/colander/en/latest/
