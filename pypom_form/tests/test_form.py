def test_page_form():
    from pypom_form.form import BaseFormPage
    from pypom_form.meta import PyPOMFormMetaclass

    assert BaseFormPage.__metaclass__ == PyPOMFormMetaclass


def test_page_region():
    from pypom_form.form import BaseFormRegion
    from pypom_form.meta import PyPOMFormMetaclass

    assert BaseFormRegion.__metaclass__ == PyPOMFormMetaclass
