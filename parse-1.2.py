import re

TAG_RE = re.compile(r'<[^>]+>')

def fix_string(s):
    #some strings have text after the overlapped double entity end, so we remove these
    while not s.endswith('</entity></entity>'):
        s = s[:-1]
    #use regex to remove all the tags
    return TAG_RE.sub('', s)

import xml.etree.ElementTree as etree
tree = etree.parse('data/raw_data/1.2.text.xml')
doc = tree.getroot()

#the whole .xml file is a "doc"
#within that "doc" are multiple "text"s
#each "text" has an "id" attribute
#each "text" has a "title" and an "abstract"
#"titles" have 0 or more "entities", each with their own "id"
#"abstracts" have 0 or more "entities", each with their own "id"

for text in doc:
    
    #1.2 has an empty "abstract" tag randomly at line 1017 
    #which avoid by only looking at "text" with at least 1 child
    if len(text)>0:

        #text is just an Element
        #to get the attributes, need to use .attrib which gets a dict of attributes
        #text_id will be something like H01-1001
        text_id = text.attrib['id']

        #length of an Element is the number of children it has 
        #should always be 2, a title and an abstract
        #however, in 1.2 there is a text (A92-1035) with just a title and no abstract
        
        #get title Element
        title = text[0]
        
        #getting the number of children but not using
        n_title_entities = len(title)
        
        #this is how you get the raw text from inside the "title" Element
        #if title has elements inside of it, then title.text will only get the text in the title up to
        #the first element, this is not what we want, so we use the tostring method instead
        #encoder='unicode' makes it a unicode string instead of a byte-string by default
        #method='text' strips away all the tags inside the Element
        title_text = etree.tostring(title, encoding='unicode', method='text').strip()

        #for every entity in the title, get it's attribute, and text
        #in 1.2, there are entities with children, example:
        #<entity id="L08-1220.16">signal <entity id="L08-1220.17">processing</entity></entity>
        #entity.text would truncate the above to just "signal"
        #the .tostring method also doesn't handle these well, so we use a custom function
        for entity in title:
            if len(entity)>0:
                    entity_text = fix_string(etree.tostring(entity, encoding='unicode').strip())
            else:
                entity_text = entity.text
            entity_id = entity.attrib['id']

        #in 1.2 there is a text (A92-1035) with just a title and no abstract, so we need this check
        if len(text) == 2:
            abstract = text[1]

            #getting the number of children but not using
            n_abstract_entities = len(abstract)
            
            #this is how you get the raw text from inside the "abstract" Element
            #if abstract has elements inside of it, then abstract.text will only get the text in the abstract up to
            #the first element, this is not what we want, so we use the tostring method instead
            #encoder='unicode' makes it a unicode string instead of a byte-string by default
            #method='text' strips away all the tags inside the Element
            abstract_text = etree.tostring(abstract, encoding='unicode', method='text').strip()

            #this is a bit different than the titles as the abstract also contains some tagged items that
            #aren't entities, and hence they won't have an "id" attribute, so we just use the .findall method
            #to only find entities
            #for every entity in the abstract, get it's attribute, and text
            #in 1.2, there are entities with children, example:
            #<entity id="L08-1220.16">signal <entity id="L08-1220.17">processing</entity></entity>
            #entity.text would truncate the above to just "signal"
            #the .tostring method also doesn't handle these well, so we use a custom function
            for entity in abstract.findall('entity'):
                if len(entity)>0:
                        entity_text = fix_string(etree.tostring(entity, encoding='unicode').strip())
                else:
                    entity_text = entity.text
                entity_id = entity.attrib['id']