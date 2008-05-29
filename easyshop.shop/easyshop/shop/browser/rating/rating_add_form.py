# Five imports
from Products.Five.browser import pagetemplatefile

# iqpp.plone.rating imports
from iqpp.plone.rating.browser.rating_forms import RatingAddForm as Base

class RatingAddForm(Base):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile("rating_add_form.pt")