# Python imports
import random
import os 

# Zope imports
from Globals import package_home

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import *

LETTERS = [chr(i) for i in range(65, 91)]

class TestEnvironmentView(BrowserView):
    """
    """
    def createProducts1(self):
        """
        """                            
        shop = self.context

        categories = []
        for i in range(1, 21):
            id = "category-%s" % i
            shop.categories.manage_addProduct["easyshop.shop"].addCategory(id, title="Category %s" %i)
            
            category = shop.categories.get(id)
            categories.append(category)
            
            wftool = getToolByName(self.context, "portal_workflow")
            wftool.doActionFor(category, "publish")

        for i in range(1, 101):
            title = self.createTitle()
            id = title.lower()
            shop.products.manage_addProduct["easyshop.shop"].addProduct(id, title=title)
            product = shop.products.get(id)            

            # add category
            category = random.choice(categories)
            category.addReference(product, "categories_products")
            
            wftool.doActionFor(product, "publish")
            
        self.context.portal_catalog.manage_catalogRebuild()
        
    def createProducts2(self):
        """Add all products to one category.
        """                            
        shop = self.context
                
        id = "category"
        shop.categories.manage_addProduct["easyshop.shop"].addCategory(id, title="Category")        
        category = shop.categories.get(id)
        
        wftool = getToolByName(self.context, "portal_workflow")
        wftool.doActionFor(category, "publish")

        for i in range(1, 21):
            title = self.createTitle()
            id = title.lower()
            shop.products.manage_addProduct["easyshop.shop"].addProduct(id, title=title)
            product = shop.products.get(id)

            img = os.path.join(package_home(globals()), '../../tests/test_2.jpg')
            img = open(img)
        
            product.setImage(img)

            category.addReference(product, "categories_products")            
            wftool.doActionFor(product, "publish")
            
        self.context.portal_catalog.manage_catalogRebuild()
        
    def createTitle(self):
        """
        """
        return "".join([random.choice(LETTERS) for i in range(1, 10)])
        

    def testMail(self):
        # Python imports
        from email.MIMENonMultipart import MIMENonMultipart
        from email.Utils import COMMASPACE

        from easyshop.shop.utilities.misc import sendMultipartMail
        
        text = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<style type="text/css">

.HeadGrossGrauLinks {
font-family: Arial, Helvetica, sans-serif;
font-size: 18px;
font-weight: bold;
text-align: left;
color: #666666;

}
.HeadGrossGrauMitte {
font-family: Arial, Helvetica, sans-serif;
font-size: 18px;
font-weight: bold;
text-align: center;
color: #666666;


}
.TextGrossGrauLinks {
font-family: Arial, Helvetica, sans-serif;
font-size: 14px;
font-weight: normal;
text-align: left;
color: #666666;
line-height: 22px;

}
.TextGrossGrauMitte {
font-family: Arial, Helvetica, sans-serif;
font-size: 14px;
font-weight: normal;
text-align: center;
color: #666666;
}

.TextKleinGrauLinks {
font-family: Arial, Helvetica, sans-serif;
font-size: 10px;
font-weight: normal;
text-align: left;
color: #666666;
}

.HeadHintergrundLinks {
font-family: Arial, Helvetica, sans-serif;
font-size: 16px;
font-weight: bold;
text-align: left;
color: #666666;
background-color: #F2F2F2;
padding-left: 10px;
vertical-align: middle;
}
.HeadHintergrundMitte {
font-family: Arial, Helvetica, sans-serif;
font-size: 18px;
font-weight: bold;
text-align: center;
color: #666666;
background-color: #F2F2F2;
vertical-align: middle;
}
.HeadHintergrundLinksGross {
font-family: Arial, Helvetica, sans-serif;
font-size: 18px;
font-weight: bold;
text-align: left;
color: #666666;
background-color: #F2F2F2;
font-variant: small-caps;
padding-left: 10px;
vertical-align: middle;

}
.HeadHintergrundMitteGross {
font-family: Arial, Helvetica, sans-serif;
font-size: 18px;
font-weight: bold;
text-align: center;
color: #666666;
background-color: #F2F2F2;
font-variant: small-caps;
vertical-align: middle;
}
.RahmenGrossGrau {
font-family: Arial, Helvetica, sans-serif;
font-size: 16px;
font-weight: bold;
text-align: center;
border: thin solid #CCCCCC;
color: #666666;
text-indent: 0pt;
padding-top: 8px;
}
.TextGrossGrauLinksFett {

font-family: Arial, Helvetica, sans-serif;
font-size: 14px;
font-weight: bold;
text-align: left;
color: #666666;
}

a{font-size:14px;:text-decoration:underline;font-weight;}
a:link { text-decoration:underline; color:#666666; }
a:visited { text-decoration:underline; color:#cccccc; }
a:hover { text-decoration:underline; color:#cccccc;}
a:active { text-decoration:underline; color:#666666;} 

-->
</style>
</head>

<body>
<div align="right"><img src="http://www.demmelhuber.net/logo.jpg" width="327" height="60" alt="Demmelhuber" longdesc="http://www.demmelhuber.net/laden" />
</div>
<p class="TextGrossGrauLinks">Sehr geehrte/r Dirk Kommol,<br />
<br />
vielen Dank für Ihre Bestellung bei www.demmelhuber.net. Hiermit erhalten Sie Ihre Bestellbestätigung:</p>
<table width="100%" border="0" cellpadding="5" cellspacing="0" bordercolor="#000000">
<tr>
<td colspan="4" class="HeadHintergrundMitteGross">BESTELLUNG 1211793802901</td>
</tr>
<tr>
<td width="15%" class="TextGrossGrauLinksFett">Name:</td>
<td width="35%" bordercolor="#000000" class="TextGrossGrauLinks">Dirk Kommol</td>
<td width="15%" class="TextGrossGrauLinksFett">Datum</td>
<td width="35%" class="TextGrossGrauLinks">26.05.2008; 11:23 Uhr</td>
</tr>
<tr>
<td width="15%" class="TextGrossGrauLinksFett">E-Mail</td>
<td width="35%" class="TextGrossGrauLinks">d.kommol@demmelhuber.net</td>;
<td width="15%" class="TextGrossGrauLinksFett">Status:</td>
<td width="35%" class="TextGrossGrauLinks">in Bearbeitung</td>
</tr>
<tr>
<td width="15%" class="TextGrossGrauLinksFett">Telefon: </td>
<td width="35%" class="TextGrossGrauLinks">037207/683-40</td>
<td width="15%" class="TextGrossGrauLinksFett">Betrag:</td>
<td width="35%" class="TextGrossGrauLinks">€ 646,95</td>
</tr>
<tr>
<td colspan="4" class="TextGrossGrauLinksFett">&nbsp;</td>
</tr>
</table>
<table width="100%" border="0" cellspacing="0" cellpadding="5">
<tr>
<td class="HeadHintergrundLinks">Rechnungsadresse</td>
<td class="HeadHintergrundLinks">Lieferadresse</td>
<td class="HeadHintergrundLinks">Zahlungsweise</td>
<td class="HeadHintergrundLinks"><div align="center">
<input type="submit" name="1" id="1" value="Zahlungsweise ändern" />
</div></td>
</tr>
<tr>
<td class="TextGrossGrauLinks">Dirk Kommol</td>
<td class="TextGrossGrauLinks">Dirk Kommol</td>
<td colspan="2" class="TextGrossGrauLinksFett">Baneinzug</td>
</tr>
<tr>
<td class="TextGrossGrauLinks">Schulstraße 3</td>
<td class="TextGrossGrauLinks">Am Gewerbegbiet 3</td>
<td colspan="2" class="TextGrossGrauLinks">Konto: 4103461 / Inhaber: Dirk Kommol</td>
</tr>
<tr>
<td class="TextGrossGrauLinks">09661 Tiefenbach</td>
<td class="TextGrossGrauLinks">09661 Schegel</td>
<td colspan="2" class="TextGrossGrauLinks">BLZ: 860 400 400 / Commerzbank Leipzig</td>
</tr>
<tr>
<td class="TextGrossGrauLinks">Deutschland</td>
<td class="TextGrossGrauLinks">Deutschland</td>
<td colspan="2" class="TextGrossGrauLinks"> </td>
</tr>
<tr>
<td colspan="4" class="TextGrossGrauLinks">&nbsp;</td>
</tr>
</table>
<table width="100%" border="0" cellspacing="0" cellpadding="5">
<tr>
<td class="HeadHintergrundLinks">Produkt</td>
<td class="HeadHintergrundLinks">Eingenschaften</td>
<td class="HeadHintergrundMitte">E - Preis</td>
<td class="HeadHintergrundMitte">Menge</td>
<td class="HeadHintergrundMitte">G - Preis</td>
</tr>
<tr>
<td class="TextGrossGrauLinks">Spielturm Jungle Gym FARM - Kletterturm mit Rutsche</td>
<td class="TextGrossGrauLinks">Rutschen 3,00 m : blau</td>
<td class="TextGrossGrauLinks"><div align="right">€ 629,00</div></td>
<td class="TextGrossGrauLinks"><div align="right">1,0</div></td>
<td class="TextGrossGrauLinks"><div align="right">€ 629,00</div></td>
</tr>
<tr>
<td class="TextGrossGrauLinks">Nachnahmebehühr</td>
<td class="TextGrossGrauLinks">&nbsp;</td>
<td class="TextGrossGrauLinks"><div align="right">€ 17,95</div></td>
<td class="TextGrossGrauLinks"><div align="right">1,0</div></td>
<td class="TextGrossGrauLinks"><div align="right">€ 17,95</div></td>
</tr>
<tr>
<td class="TextGrossGrauLinks">Versandkosten</td>
<td class="TextGrossGrauLinks">&nbsp;</td>
<td class="TextGrossGrauLinks"><div align="right">€ 0,00</div></td>
<td class="TextGrossGrauLinks"><div align="right">1,0</div></td>
<td class="TextGrossGrauLinks"><div align="right">€ 0,00</div></td>
</tr>
<tr>
<td colspan="4" class="HeadHintergrundLinks"><div align="right">Gesamtwert Ihrer Bestellung inkl. 19% MwSt.:</div></td>
<td class="HeadHintergrundLinks"><div align="right">€ 646,95</div></td>
</tr>
<tr>
<td colspan="5">&nbsp;</td>
</tr>
</table>
<table width="100%" border="0" cellspacing="0" cellpadding="5">
<tr>
<td class="HeadHintergrundLinks">Hinweis zur Bestellung</td>
</tr>
<tr>
<td class="TextGrossGrauLinks">Bla balladfgjasdklgsadlfjkshdfsdagfadskghasdlkfsmhcvlasdkhnxksavasfhlxasdcgacdgascdfgcdsfcgsdf</td>
</tr>
</table>
<p class="RahmenGrossGrau">Sie haben es Zahlunsweise Bankeinzug gewählt, Der Betrag wird in den nächsten Tagen von Ihrem Konto.....<br />
fdasdfsdafasdfasdfsadfsdafs<br />
</p>
<p class="TextGrossGrauLinks">Für Fragen erreichen Sie uns unter unserer Kunden-Hotline +49(0)37207.683-66 oder per email an <a href="maiulto:info@demmelhuber.net">info@demmelhuber.net</a>. 
Bei Rückfragen geben Sie bitte immer Ihre Bestellnummer 1211793802901 an. Vielen Dank!</p>
<p class="TextGrossGrauLinks">Mit freundlichen Grüßen<br />
DEMMELHUBER Holz &amp; Raum GmbH<br />
<img src="http://www.demmelhuber.net/logo.jpg" alt="Demmelhuber" width="327" height="60" longdesc="http://www.demmelhuber.net/laden" /></p>
<table width="100%" border="0" cellspacing="0" cellpadding="5">
<tr>
<td width="33%"><span class="TextGrossGrauLinks">Am Gewerbegebiet 3<br />
09661 Hainichen/ OT Schlegel</span></td>
<td width="33%"><span class="TextGrossGrauLinks">Telefon: +49(0)37207.683-66<br />
Telefax: +49(0)37207.683-50</span></td>
<td width="33%"><span class="TextGrossGrauLinks"><a href="www.demmelhuber.net">Homepage: www.demmelhuber.net</a><a href="http://www.demmelhuber.net/laden"><br />
Online Shop: www.demmelhuber.net/laden</a></span></td>;
</tr>
</table>
<p class="TextGrossGrauLinks"><span class="TextKleinGrauBlock"> Sitz der Gesellschaft: Demmelhuber Holz &amp; Raum GmbH, Am Gewerbegebiet 3, 09661 Hainichen/ OT Schlegel<br />
Geschäftsführer: Rüdiger Schmidt, Erfüllungsort und Gerichtsstand Hainichen, Registergericht: AG Chemnitz HRB 16407, Ust-ID: DE 812638837 </span></p>
<p class="TextGrossGrauLinks"><br />
</p>
<p>&nbsp;</p>
</body>
</html>        """
        # msg = MIMENonMultipart("text", "html")
        # 
        # msg["from"] = "usenet@diefenba.ch"
        # msg["to"] = COMMASPACE.join(("usenet@diefenba.ch", "d.Kommol@demmelhuber.net"))
        # msg["subject"] = "Order Test Mail 2"
        # msg.set_payload(text)
        # 
        # mailhost = self.context.MailHost
        # mailhost.send(msg.as_string())

        from email.MIMEText import MIMEText
        from email.MIMEMultipart import MIMEMultipart

        mail = MIMEMultipart("alternative")
    
        mail['From']    = "usenet@diefenba.ch"
        mail['To']      = COMMASPACE.join(("usenet@diefenba.ch", "d.Kommol@demmelhuber.net"))
        mail['Subject'] = "Order Test Mail 3"
        mail.epilogue   = ''

        # create & attach text part 
        text_part = MIMEText(text, "plain", "utf-8")
        mail.attach(text_part)

        # create & attach html part with images            
        html_part = MIMEMultipart("related")
        html_code = MIMEText(text, "html", "utf-8")
        html_part.attach(html_code)       
        mail.attach(html_part)

        self.context.MailHost.send(mail.as_string())
