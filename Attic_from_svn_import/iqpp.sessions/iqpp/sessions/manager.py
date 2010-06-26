from DateTime import DateTime

# zope imports
from zope.interface import implements

# easyshop.core imports
from easyshop.core.interfaces import ISessionManagement

class SessionManagement:
    """
    """
    implements(ISessionManagement)
    
    def getSID(self, request):
        """
        """
        # First we try to get the session id out of a cookie. If there is none, 
        # we get the session id out of the request and create a cookie.
        
        sid = request.cookies.get("easyshop-sid", None)
        if sid is None:            
            try:                
                sid = request.SESSION.getId()
                expires = (DateTime() + 10).toZone('GMT').rfc822()
                request.RESPONSE.setCookie("easyshop-sid", sid, expires=expires, path="/")
            except AttributeError:
                sid = "DUMMY_SESSION"
        
        return sid