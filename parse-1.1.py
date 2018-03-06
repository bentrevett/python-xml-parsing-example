import xml.etree.ElementTree as etree
tree = etree.parse('data/raw_data/1.1.text.xml')
doc = tree.getroot()

#the whole .xml file is a "doc"
#within that "doc" are multiple "text"s
#each "text" has an "id" attribute
#each "text" has a "title" and an "abstract"
#"titles" have 0 or more "entities", each with their own "id"
#"abstracts" have 0 or more "entities", each with their own "id"

for text in doc:
    
    #text is just an Element
    #to get the attributes, need to use .attrib which gets a dict of attributes
    #text_id will be something like H01-1001
    text_id = text.attrib['id']

    #length of an Element is the number of children it has 
    #should always be 2, a title and an abstract
    assert len(text) == 2, f'a <text> should have 2 children, a title and an abstract, found: {len(text)}'
    
    #get title and abstract Elements
    title = text[0]
    abstract = text[1]

    #getting the number of children but not using
    n_title_entities = len(title)
    
    #this is how you get the raw text from inside the "title" Element
    #if title has elements inside of it, then title.text will only get the text in the title up to
    #the first element, this is not what we want, so we use the tostring method instead
    #encoder='unicode' makes it a unicode string instead of a byte-string by default
    #method='text' strips away all the tags inside the Element
    title_text = etree.tostring(title, encoding='unicode', method='text').strip()

    #for every entity in the title, get it's attribute, and text
    #every entity should have no children, hence why we don't need to use the tostring method
    #but just to be sure, we assert each element's length (i.e. it's number of children) is 0
    for entity in title:
        assert len(entity) == 0, f'Entities should have no children, found: {len(entity)}'
        entity_id = entity.attrib['id']
        entity_text = entity.text 

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
    #every entity should have no children, hence why we don't need to use the tostring method
    #but just to be sure, we assert each element's length (i.e. it's number of children) is 0
    for entity in abstract.findall('entity'):
        assert len(entity) == 0, f'Entities should have no children, found: {len(entity)} in {entity.text}'
        entity_id = entity.attrib['id']
        entity_text = entity.text