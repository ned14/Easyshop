# Python imports
import re

# zope imports
from zope.interface import implements

# easyshop imports
from easyshop.core.interfaces import INumberConverter

class NumberConverter:
    """
    """
    implements(INumberConverter)
    
    def floatToString(self, myfloat):
        """
        """
        myfloat = "%.2f" % myfloat
        myfloat = myfloat.replace(".", ",")
        return myfloat

    def floatToTaxString(self, myfloat, unit=" %"):
        """
        """
        myfloat = "%.2f" % myfloat
        
        # replace zeros if appropriate
        myfloat = re.sub("\.?0+$", "", myfloat)
                
        myfloat = myfloat.replace(".", ",")
        myfloat = myfloat + unit
        
        return myfloat

    def formatString(self, mystring):
        """
        """
        try:
            myfloat = float(mystring)
        except ValueError:
            return ""
            
        myfloat = "%.2f" % myfloat
        myfloat = myfloat.replace(".", ",")
        return myfloat
        
    def stringToFloat(self, mystring):
        """
        """
        mystring = mystring.replace(",", ".")
        try:
            myfloat = float(mystring)
        except ValueError:
            return 0.0

        return myfloat