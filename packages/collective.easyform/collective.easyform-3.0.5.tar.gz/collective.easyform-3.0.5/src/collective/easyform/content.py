# -*- coding: utf-8 -*-
from collective.easyform.interfaces import IEasyForm
from plone.dexterity.content import Item
from zope.interface import implementer


@implementer(IEasyForm)
class EasyForm(Item):
    """An easy form content base
    """
