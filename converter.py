def transform(text_content, entities):
    '''adds hyperlinks to text'''
    import re
    
    for entity in entities:
        wiki = entity['wiki']
        for mention in entity['mentions']:
            text_content = re.sub(mention+'(?!<)', f'<a href="{wiki}">{mention}</a>', text_content)
            
    return(text_content)

def analyze(text_content):
    '''çalls the google entity recognition api returns entities in text with a wiki page'''
    from google.cloud import language_v1
    
    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    document = {"content": text_content, "type_": type_}

    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    # Loop through entitites returned from the API
    entities = []
    for entity in response.entities:
        for metadata_name, metadata_value in entity.metadata.items():
            if metadata_name == 'wikipedia_url':
                wiki = metadata_value
                break
        else:
            wiki = False
        # append entities with a wiki page to list
        if wiki:
            entities.append({'wiki': wiki, 
                             'mentions': set([mention.text.content for mention in entity.mentions])})

    return entities
    
def convert_pdf(file_path):
    '''turn pdf into plaintext'''
    from io import StringIO

    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfparser import PDFParser

    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return(output_string.getvalue())

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\SemKj\Downloads\skilful-nexus-344522-3d57dd4a3fa9.json"
plaintext = convert_pdf('example.pdf')
entities = analyze(plaintext)
output_text = transform(plaintext, entities)
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(output_text)