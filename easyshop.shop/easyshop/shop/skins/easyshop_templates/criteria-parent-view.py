url = context.aq_inner.aq_parent.absolute_url()
context.REQUEST.RESPONSE.redirect(url)