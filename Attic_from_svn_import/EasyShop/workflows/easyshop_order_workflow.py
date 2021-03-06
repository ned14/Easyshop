# 
#
# Generated by dumpDCWorkflow.py written by Sebastien Bigaret
# Original workflow id/title: easyshop_order_workflow/EasyShop Order Workflow
# Date: 2006/10/28 15:09:36.492 GMT+2
#
# WARNING: this dumps does NOT contain any scripts you might have added to
# the workflow, IT IS YOUR RESPONSABILITY TO MAKE BACKUPS FOR THESE SCRIPTS.
#
# No script detected in this workflow
# 
"""
Programmatically creates a workflow type
"""
__version__ = "$Revision: 1.1.1.1 $"[11:-2]

from Products.CMFCore.WorkflowTool import addWorkflowFactory

from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

def setupEasyshop_order_workflow(wf):
    "..."
    wf.setProperties(title='EasyShop Order Workflow')

    for s in ['canceled', 'pending', 'sent (not payed)', 'closed', 'payed (not sent)']:
        wf.states.addState(s)
    for t in ['cancel', 'pay', 'send_not_payed', 'pay_not_sent', 'send']:
        wf.transitions.addTransition(t)
    for v in ['action', 'time', 'comments', 'actor', 'review_history']:
        wf.variables.addVariable(v)
    for l in ['reviewer_queue']:
        wf.worklists.addWorklist(l)
    for p in ('Access contents information', 'Change portal events', 'Modify portal content', 'View', 'Copy or Move'):
        wf.addManagedPermission(p)
        

    ## Initial State
    wf.states.setInitialState('pending')

    ## States initialization
    sdef = wf.states['canceled']
    sdef.setProperties(title="""""",
                       transitions=())
    sdef.setPermission('Access contents information', 0, ['Manager', 'Owner'])
    sdef.setPermission('Change portal events', 0, ['Manager'])
    sdef.setPermission('Modify portal content', 0, ['Manager'])
    sdef.setPermission('View', 0, ['Manager', 'Owner'])
    sdef.setPermission('Copy or Move', 1, [])

    sdef = wf.states['pending']
    sdef.setProperties(title="""""",
                       transitions=('cancel', 'pay', 'send'))
    sdef.setPermission('Access contents information', 0, ['Manager', 'Owner'])
    sdef.setPermission('Change portal events', 0, ['Manager'])
    sdef.setPermission('Modify portal content', 0, ['Manager'])
    sdef.setPermission('View', 0, ['Manager', 'Owner'])
    sdef.setPermission('Copy or Move', 0, ['Manager'])

    sdef = wf.states['sent (not payed)']
    sdef.setProperties(title="""""",
                       transitions=('cancel', 'pay'))
    sdef.setPermission('Access contents information', 0, ['Manager', 'Owner'])
    sdef.setPermission('Change portal events', 0, ['Manager'])
    sdef.setPermission('Modify portal content', 0, ['Manager'])
    sdef.setPermission('View', 0, ['Manager', 'Owner'])
    sdef.setPermission('Copy or Move', 1, [])

    sdef = wf.states['closed']
    sdef.setProperties(title="""""",
                       transitions=())
    sdef.setPermission('Access contents information', 0, ['Manager', 'Owner'])
    sdef.setPermission('Change portal events', 0, ['Manager'])
    sdef.setPermission('Modify portal content', 0, ['Manager'])
    sdef.setPermission('View', 0, ['Manager', 'Owner'])
    sdef.setPermission('Copy or Move', 1, [])

    sdef = wf.states['payed (not sent)']
    sdef.setProperties(title="""""",
                       transitions=('cancel', 'send'))
    sdef.setPermission('Access contents information', 1, ['Manager', 'Owner'])
    sdef.setPermission('Change portal events', 1, ['Manager'])
    sdef.setPermission('Modify portal content', 1, ['Manager'])
    sdef.setPermission('View', 1, ['Manager', 'Owner'])
    sdef.setPermission('Copy or Move', 1, [])


    ## Transitions initialization
    tdef = wf.transitions['cancel']
    tdef.setProperties(title="""""",
                       new_state_id="""canceled""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Cancel""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props={'guard_permissions': 'Manage portal'},
                       )

    tdef = wf.transitions['pay']
    tdef.setProperties(title="""""",
                       new_state_id="""closed""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Pay""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props={'guard_permissions': 'Manage portal'},
                       )

    tdef = wf.transitions['send_not_payed']
    tdef.setProperties(title="""""",
                       new_state_id="""sent (not payed)""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Send""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props={'guard_permissions': 'Manage portal'},
                       )

    tdef = wf.transitions['pay_not_sent']
    tdef.setProperties(title="""""",
                       new_state_id="""payed (not sent)""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Pay""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props={'guard_permissions': 'Manage portal'},
                       )

    tdef = wf.transitions['send']
    tdef.setProperties(title="""""",
                       new_state_id="""sent (not payed)""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Send""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props={'guard_permissions': 'Manage portal'},
                       )

    ## State Variable
    wf.variables.setStateVar('review_state')

    ## Variables initialization
    vdef = wf.variables['action']
    vdef.setProperties(description="""The last transition""",
                       default_value="""""",
                       default_expr="""transition/getId|nothing""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['time']
    vdef.setProperties(description="""Time of the last transition""",
                       default_value="""""",
                       default_expr="""state_change/getDateTime""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['comments']
    vdef.setProperties(description="""Comments about the last transition""",
                       default_value="""""",
                       default_expr="""python:state_change.kwargs.get('comment', '')""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['actor']
    vdef.setProperties(description="""The ID of the user who performed the last transition""",
                       default_value="""""",
                       default_expr="""user/getId""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['review_history']
    vdef.setProperties(description="""Provides access to workflow history""",
                       default_value="""""",
                       default_expr="""state_change/getHistory""",
                       for_catalog=0,
                       for_status=0,
                       update_always=0,
                       props={'guard_permissions': 'Request review; Review portal content'})

    ## Worklists Initialization
    ldef = wf.worklists['reviewer_queue']
    ldef.setProperties(description="""Reviewer tasks""",
                       actbox_name="""Pending (%(count)d)""",
                       actbox_url="""%(portal_url)s/search?review_state=pending""",
                       actbox_category="""global""",
                       props={'guard_permissions': 'Review portal content', 'var_match_review_state': 'pending'})


def createEasyshop_order_workflow(id):
    "..."
    ob = DCWorkflowDefinition(id)
    setupEasyshop_order_workflow(ob)
    return ob

addWorkflowFactory(createEasyshop_order_workflow,
                   id='easyshop_order_workflow',
                   title='EasyShop Order Workflow')