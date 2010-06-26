from easyshop.core.config import _

def FORM_HEADER(form_id):
    return """
        <form id="%s">
            <table>
    """ % form_id
    
def FORM_TEXT_FIELD(label, name, required=False, value=""):
    """
    """
    result = """
        <tr>
            <td>
                <label>
                    %s
                </label>    
    """ % label
    
    if required == True:
        result += """
                <span class="fieldRequired"
                      title="Required">
                    (Required)
                </span>
        """
    result += """                        
            </td>
            <td>
                <input name="%s"
                       value="%s"
                       type="text" />                
            </td>
        </tr>
    """ % (name, value)
    
    return result

def FORM_BUTTON(id, value="Save", klass="context"):
    return """
        <input class="%s" 
               value="%s"
               id="%s" 
               type="submit" />
    """ % (klass, _(value), id)

def FORM_FOOTER():
    return """
            </table>    
        </form>
    """