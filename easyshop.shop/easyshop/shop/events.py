# zope imports
from zope.app.event.interfaces import IObjectCreatedEvent
from zope.app.event.objectevent import ObjectCreatedEvent
from zope.interface import implements

class IShopCreatedEvent(IObjectCreatedEvent):
    """Marker interface for event: shop has been created.
    """

class ShopCreatedEvent(ObjectCreatedEvent):
    """An event, which is fired up when a shop has been created.
    """
    implements(IShopCreatedEvent)