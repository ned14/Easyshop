# Zope imports
from DateTime import DateTime

# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import IValidity
from Products.EasyShop.interfaces import IDateCriteriaContent

class DateCriteriaValidity:
    """Adapter which provides IValidity for date criteria content
    objects.
    """    
    implements(IValidity)
    adapts(IDateCriteriaContent)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """
        """
        now = DateTime()

        start = self.context.getStart()
        end   = self.context.getEnd()

        isGreaterStart = False
        isLesserEnd    = False

        if start is None:
            isGreaterStart = True
        elif now >= start:
             isGreaterStart = True

        if end is None:
            isLesserEnd = True
        elif  now <= end:
            isLesserEnd = True

        return isGreaterStart and isLesserEnd