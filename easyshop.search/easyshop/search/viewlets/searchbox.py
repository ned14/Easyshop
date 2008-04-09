from plone.app.layout.viewlets.common import SearchBoxViewlet as Base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SearchBoxViewlet(Base):
    """
    """
    render = ViewPageTemplateFile('searchbox.pt')
