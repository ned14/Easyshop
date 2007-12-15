# Zope imports
from DateTime import DateTime

# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IDateCriteria

class DateCriteriaValidity:
    """Adapter which provides IValidity for date criteria content objects.
    """    
    implements(IValidity)
    adapts(IDateCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True if now between the selected start and end date of the
        criterion.
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