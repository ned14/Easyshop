from zope.interface import Interface

class ICompleteness(Interface):
    """Provides methods to check completeness.
    """

    def isComplete():
        """Checks whether the data of an object is complete.
        """        
        
class IType(Interface):
    """Provides methods to get type informations.
    """
    def getType():
        """Returns the type of the object.
        """
        
class IValidity(Interface):
    """Provides methods to check validity.
    """

    def isValid(**kwargs):
        """Returns true if the object fullfills criteria of validity.
        """
        
class IMailAddresses(Interface):
    """Provides methods to retrieve mail addresses.
    """
    def getSender():
        """Returns the sender of shop e-mails based on the entered data.
        """
        
    def getReceivers():
        """Returns receivers of shop e-mails based on entered data.
        """