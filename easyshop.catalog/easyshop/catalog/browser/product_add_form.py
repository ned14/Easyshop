# z3c imports
from z3c.form import form
from z3c.form import field

# plone imports
from plone.z3cform import base

# easyshop imports
from easyshop.core.interfaces import IProduct

class ProductAddForm(form.Form):

    fields = field.Fields(IProduct)
    ignoreContext=True
    
    def create(self, data):
        """
        """
        pass

    def add(self, object):
        pass

    def nextURL(self):
        pass

class ProductAddFormView(base.FormWrapper):
    """
    """
    form = ProductAddForm


from zope import interface, schema
from z3c.form import form, field, button
from plone.z3cform import base

class MySchema(interface.Interface):
    age = schema.Int(title=u"Age")

class MyForm(form.AddForm):
    fields = field.Fields(MySchema)

    @button.buttonAndHandler(u'Apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        print data['age'] # ... or do stuff

class MyView(base.FormWrapper):
    form = MyForm
    label = u"Please enter your age"