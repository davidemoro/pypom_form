from pypom import (
    Page,
    Region,
)

from .meta import PageEditMetaclass


class BaseFormPage(Page):
    """ This is the base page form class
        for schema based page objects.
    """
    __metaclass__ = PageEditMetaclass


class BaseFormRegion(Region):
    """ This is the base region form class
        for schema based page objects.
    """
    __metaclass__ = PageEditMetaclass
