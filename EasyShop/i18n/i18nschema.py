#!/usr/bin/python
header = """
# --- PLEASE EDIT THE LINES BELOW CORRECTLY ---
# SOME DESCRIPTIVE TITLE.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: 2007-05-09 16:00+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI +ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=1; plural=0\\n"
"Language-Code: en\\n"
"Language-Name: English\\n"
"Preferred-Encodings: utf-8 latin1\\n"
"Domain: EasyShop\\n"

"""

import os
import re

re_label = re.compile("""label_msgid\s*=\s*["'](.*)["']""")
re_description = re.compile("""description_msgid\s*=\s*["'](.*)["']""")

msgids = {}    
result = []
for root, dirs, files in os.walk('../content'):

    if root.startswith("../content") == False:
        continue
        
    for name in files:
        if re.search("py$", name) is None:
            continue
        
        filename = os.path.join(root, name) 
        fh = open(filename)

        for line in fh.readlines():
            mo = re_label.search(line) or re_description.search(line)
            if mo:
                key = mo.group(1)
                if msgids.has_key(key) == False:
                    msgids[key] = []
                    
                msgids[mo.group(1)].append(filename) 

keys = msgids.keys()
keys.sort()
for msgid in keys:
    if msgid == "schema_":
        continue
        
    for filename in msgids[msgid]:
        result.append('#: schema | %s' % filename)
        
    result.append('msgid "%s"' % msgid)
    result.append('msgstr ""\n')
            
new = open('./easyshop-schema.pot', "w")
new.write(header)
new.write("\n".join(result))