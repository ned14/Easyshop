# ZODB imports
from persistent.dict import PersistentDict

# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class ProductPrices(object):
    """Provides IPrices for product content object.
    """
    implements(IPrices)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        pvm  = IProductVariantsManagement(context)
        shop = IShopManagement(context).getShop()
        
        self.context = context
        if not hasattr(context, "cache"):
            self.context.cache = PersistentDict()

        self.gross_prices = shop.getGrossPrices()
        self.has_variants = pvm.hasVariants()
        self.taxes = ITaxes(context)

        if self.has_variants:
            self.product_variant = \
                pvm.getSelectedVariant() or pvm.getDefaultVariant()
        else:
            self.product_variant = self.context
                                   
    def getPriceForCustomer(self, effective=True, variant_price=True):
        """
        """
        import pdb; pdb.set_trace()
        cache_key = "price-for-customer-%s-%s-%s" % (effective, variant_price, self.product_variant.UID())
        price = self.context.cache.get(cache_key)
        if price is not None:
            return price
            
        if self.has_variants and variant_price and \
           self.product_variant.getPrice() != 0:
            price = IPrices(self.product_variant).getPriceForCustomer(effective)
        else:
            if effective == True:
                price = self._getEffectivePriceForCustomer()
            else:
                price = self._getStandardPriceForCustomer()
        
        self.context.cache[cache_key] = price
        return price
            
    def getPriceNet(self, effective=True, variant_price=True):
        """
        """
        cache_key = "price-net-%s-%s-%s" % (effective, variant_price, self.product_variant.UID())
        price = self.context.cache.get(cache_key)
        if price is not None:
            return price
        
        if self.has_variants and variant_price and \
           self.product_variant.getPrice() != 0:
            price = IPrices(self.product_variant).getPriceNet(effective)
        else:
            if effective == True:
                return self._getEffectivePriceNet()
            else:
                return self._getStandardPriceNet()

        self.context.cache[cache_key] = price
        return price

    def getPriceGross(self, effective=True, variant_price=True):
        """
        """
        cache_key = "price-for-gross-%s-%s-%s" % (effective, variant_price, self.product_variant.UID())
        price = self.context.cache.get(cache_key)
        if price is not None:
            return price
        
        if self.has_variants and variant_price and \
           self.product_variant.getPrice() != 0:
            price = IPrices(self.product_variant).getPriceGross(effective)
        else:
            if effective == True:
                price = self._getEffectivePriceGross()
            else:
                price = self._getStandardPriceGross()

        self.context.cache[cache_key] = price
        return price

    # Effective Price
    def _getEffectivePriceForCustomer(self):
        """Returns the effective price for customer, dependend of the product 
        is for sale or not.
        """
        tax_abs_customer = self.taxes.getTaxForCustomer()
        return self._getEffectivePriceNet() + tax_abs_customer

    def _getEffectivePriceNet(self):
        """Returns the effective price for customer, dependend of the product 
        is for sale or not.
        """
        if self.context.getForSale() == True:
            price = self.context.getSalePrice()
        else:
            price = self.context.getPrice()
        
        if self.gross_prices == True:
            return price - self.taxes.getTax()
        else:
            return price

    def _getEffectivePriceGross(self):
        """Returns the effective price for customer, dependend of the product 
        is for sale or not.
        """
        if self.context.getForSale() == True:
            price = self.context.getSalePrice()
        else:
            price = self.context.getPrice()
            
        if self.gross_prices == True:
            return price
        else:
            return price + self.taxes.getTax()

    # Standard Price
    def _getStandardPriceForCustomer(self):
        """Returns always the standard price, independent of the product is for 
        sale or not. We need this in any case to display the standard price 
        (e.g. stroked).
        """
        tax_abs_customer = self.taxes.getTaxForCustomer(False)
        return self._getStandardPriceNet() + tax_abs_customer

    def _getStandardPriceNet(self):
        """Returns always the standard price, independent of the product is for 
        sale or not. We need this in any case to display the standard price 
        (e.g. stroked).
        """
        if self.gross_prices == True:
            return self.context.getPrice() - self.taxes.getTax(False)
        else:
            return self.context.getPrice()

    def _getStandardPriceGross(self):
        """Returns always the standard price, independent of the product is for 
        sale or not. We need this in any case to display the standard price 
        (e.g. stroked).
        """
        if self.gross_prices == True:
            return self.context.getPrice()
        else:
            return self.context.getPrice() + self.taxes.getTax(False)
            
class ProductVariantPrices(ProductPrices):
    """Provides IPrices for product variant content object.
    """
    implements(IPrices)
    adapts(IProductVariant)

    def __init__(self, context):
        """
        """
        super(ProductVariantPrices, self).__init__(context)
        self.parent = self.context.aq_inner.aq_parent

    def getPriceForCustomer(self, effective=True):
        """
        """
        if self.context.getPrice() != 0:
            base = super(ProductVariantPrices, self)
            price = base.getPriceForCustomer(effective)
        else:
            price = IPrices(self.parent).getPriceForCustomer(variant_price=False)

        return price
            
    def getPriceNet(self, effective=True):
        """
        """
        if self.context.getPrice() != 0:
            base = super(ProductVariantPrices, self)
            price = base.getPriceNet(effective)
        else:
            price = IPrices(self.parent).getPriceNet(variant_price=False)

        return price

    def getPriceGross(self, effective=True):
        """
        """
        if self.context.getPrice() != 0:
            base = super(ProductVariantPrices, self)
            price = base.getPriceGross(effective)
        else:
            price = IPrices(self.parent).getPriceGross(variant_price=False)
            
        return price
            