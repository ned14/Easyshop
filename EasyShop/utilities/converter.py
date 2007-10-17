# Python imports
import re

# zope imports
from zope.interface import implements

# EasyShop imports
from Products.EasyShop.interfaces import IAddressConverter
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import INumberConverter
from Products.EasyShop.interfaces import IPhotoManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IPropertyManagement

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


class AddressConverter:
    """
    """
    implements(IAddressConverter)
    
    def addressToDict(self, address):
        """
        """
        return {
            "name" : address.getName(),
            "company_name" : address.getCompanyName(),
            "address1" : address.getAddress1(),
            "address2" : address.getAddress2(),
            "zipcode" : address.getZipCode(),
            "city": address.getCity(),
            "country" : address.getCountry(),
            "phone" : address.getPhone()            
        }