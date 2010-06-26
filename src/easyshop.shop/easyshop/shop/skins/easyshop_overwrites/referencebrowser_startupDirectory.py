## Script (Python) "referencebrowser_startupDirectory"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=directory=''
##title=
##

from Products.CMFCore.utils import getToolByName

# Mapping works as follows:
#
#  directory == ''                  => Current object
#  directory == '/absolute/url'     => Portal root + absolute url
#  directory == '../relative/url'   => Current object + relative url
#
# If the object is in the portal_factory, remove the factory from the equation.
# This creates an inconsistency with the case when directory is not set,
# because the current object is in the factory and thus not generally useful
# as a starting point for browsing (it won't contain any sub-objects, and the
# parent object is the factory's temporary folder). Hence, in this case, the
# startup directory is the parent folder.
#
# Similarly, if directory is a relative path starting with '../' and the object
# is in the factory, let the first '../' part of the relative URL refer to the
# destination parent folder, not the factory.

def filterPortalFactory (url):
    """Return context's url + the relative url given, but remove any
    reference to portal_factory.
    """

    portal_factory = getToolByName (context, 'portal_factory')

    # Prepend / to ensure proper path separation, and ensure url is a string
    if url:
        url = '/' + url
    else:
        url = ''
    basePath = ''

    if portal_factory.isTemporary (context):
        pathParts = context.getPhysicalPath ()

        # Remove the factory from the path
        pathParts = pathParts[:-3]

        # If the object is in the portal factory, we'll be relative to the
        # parent folder, not the temporary object which does not yet exist,
        # so remove any explicit ../ from the relative path
        if url.startswith ('/..'):
            url = url[3:]

        basePath = '/'.join (pathParts)
    else:
        basePath = context.absolute_url (relative = 1)


    # Resolve the URL
    try:
        targetPath = basePath + url
        object = context.restrictedTraverse (targetPath)
        return object.absolute_url ()
    except:
        return context.absolute_url ()

# checks if path starts with / - if, then
# path is relative to portal root
def checkPath(path):
    if path.startswith('/'):
        portal_url = getToolByName (context, 'portal_url')
        return portal_url () + path
    else:
        return path

#
# Main execution
#

# Default case - if no directory is given, search for a property
# refwidget_startupdirectories in portal_properties/site_properties
# that is a lines field having the following
# form:
#    path1:path2
# path1 is the path where all widgets being under it set startup_directory
# to path2 if no startup_directory is set.
try:
    directory = getattr(context, directory)()
except (KeyError, AttributeError):
    pass
    
if directory.strip() == '':

    props = getToolByName(context, 'portal_properties').site_properties
    if hasattr(props, 'refwidget_startupdirectories'):
        startups = props.refwidget_startupdirectories
        ownpath = '/'.join(context.getPhysicalPath())

        # remove portal path - / is always portal_root
        purl = '/'.join(getToolByName(context, 'portal_url').getPortalObject().getPhysicalPath())
        ownpath = ownpath.replace(purl, '')
        
        for pathdef in startups:
            psplit = pathdef.split(':')
            if ownpath[0:len(psplit[0])] == psplit[0]:
                dopath = psplit[1].strip()
                if checkPath(dopath) == dopath:
                    return filterPortalFactory(dopath)
                else: return checkPath(dopath)
    
    return filterPortalFactory (None)

# If we have an absolute URL, return it relative to the portal root
if checkPath(directory) != directory:
    return checkPath(directory)
    
# Else, if we have a relative URL, get it relative to the context.
return filterPortalFactory (directory)
