from zope.component import getMultiAdapter
from easyshop.core.interfaces import IShopManagement
from easyshop.coupon import couponMessageFactory as _

def install_container(gs_context):
    site = gs_context.getSite()
    es = site.portal_catalog(object_provides='easyshop.core.interfaces.shop.IShop')
    
    for shop_brain in es:
        shop = shop_brain.getObject()
        if not hasattr(shop,'coupon-manager'):
            shop.manage_addProduct["easyshop.coupon"].addCouponContainer(
                id="coupon-manager", 
                title=_('Coupon Manager')
            )
