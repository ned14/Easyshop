## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters= firstname, lastname, email
##title=

from Products.CMFPlone import PloneMessageFactory as _

member=context.portal_membership.getAuthenticatedMember()
member.setProperties(context.REQUEST)

return state.set(portal_status_message=_(u'User informations has been changed.'))

