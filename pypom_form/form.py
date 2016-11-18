from pypom import (
    Page,
    Region,
)

from .meta import PyPOMFormMetaclass


BaseFormPage = PyPOMFormMetaclass(
    str('BaseFormPage'),
    (Page,),
    {
        '__doc__': 'This is the base page form class'
                   'for schema based page objects.'
    }
)


BaseFormRegion = PyPOMFormMetaclass(
    str('BaseFormRegion'),
    (Region,),
    {
        '__doc__': 'This is the base region form class'
                   'for schema based page objects.'
    }
)
