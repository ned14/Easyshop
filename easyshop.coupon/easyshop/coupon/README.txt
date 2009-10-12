Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Create a EasyShop instance

    >>> browser.getLink('Add new').click()
    >>> browser.getControl('EasyShop').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'EasyShop' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'EasyShop sample'
    >>> browser.getControl(name='shopOwner').value = 'Portal Testowner'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Create a test product

    >>> browser.getLink('Add new').click()
    >>> import pdb; pdb.set_trace()
    >>> browser.getControl('Product', index=0).click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Product' in browser.contents
    True

fill in product data

    >>> browser.getControl(name='title').value = 'Test Product'
    >>> browser.getControl(name='price').value = '100'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

add the product to a test category so that we can buy it later on

    >>> browser.getLink('Products').click()
    >>> browser.getControl('Go!').click()
    >>> 'Test Product' in browser contents
    True

    >>> browser.getControl(name='selected_uids').click()
    >>> browser.getControl(name='action').value = 'change_category'
    >>> browser.getForm(action='manage-products').submit()
    >>> 'New category' in browser.contents
    True

    >>> browser.getControl(name='new_target_category').value = 'Test Category'
    >>> browser.getControl('Add to category').click()
    >>> 'Test Category' in browser.contents
    True

-*- extra stuff goes here -*-
The Coupon content type
===============================

In this section we are tesing the Coupon content type by performing
basic operations like adding, updadating and deleting Coupon content
items.

Adding a new Coupon content item
--------------------------------

We add a easyshop discount

    >>> browser.getLink('Discounts').click()
    >>> browser.getLink('Add Discount').click()
    >>> browser.getControl(name='title').value = '50% dicount'
    >>> browser.getControl(name='value').value = '50'
    >>> browser getControl(name='type').value = 'percentage'
    >>> browser.getControl(name='base').value = 'cart_item'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

add a coupon as criteria to the discount

    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Coupon Criteria').click()
    >>> browser.getControl(name='form.button.Add').click()

save coupon id for later usage

    >>> couponId = browser.getControl(name='couponId').value
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents and couponId in browser.contents
    True

log out and buy the test product as anonymous user

    >>> browser.getLink('Logout').click()
