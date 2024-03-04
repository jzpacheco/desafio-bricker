import fitz
import boto3

from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain, create_structured_output_runnable

textract = boto3.client('textract')
openai_key = "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"

structured_schema = {
    "type": "object",
    "properties": {
        "expedition_date": {"type": "string", "description": "Data de emissão do certificado, DD/MM/YYYY"},
        "responsible_registry": {"type": "string"},
        "registration_number": {"type": "string"},
        "property_type": {"type": "string"},
        "batch": {"type": "string"},
        "block": {"type": "string"},
        "street": {"type": "string"},
        "street_2": {"type": "string"},
        "property_number": {"type": "string"},
        "property_number_2": {"type": "string"},
        "address_complement": {"type": "string"},
        "neighborhood": {"type": "string"},
        "city": {"type": "string"},
        "state": {"type": "string"},
        "property_footage": {"type": "string"},
        "owners_quantity": {"type": "string"},
        "owner_1": {"type": "string"},
        "owner_2": {"type": "string"},
        "document_owner_1": {"type": "string", "description":"CPF / CNPJ"},
        "document_owner_2": {"type": "string"},
        "mortgage": {"type": "string"},
        "mortgage_owner_name": {"type": "string"},
        "mortgage_owner_document": {"type": "string"},
        "fiduciary_alienation": {"type": "string"},
        "fiduciary_alienation_owner_name": {"type": "string"},
        "fiduciary_alienation_owner_document": {"type": "string"},
        "garnishment": {"type": "string"}
    }
}

llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo", openai_api_key=openai_key)

extraction_chain = create_structured_output_runnable(structured_schema, llm)

def extract_image_from_pdf(pdf_path):
  
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            images = page.get_images(full=True)
            for i, img in enumerate(images):
                xref= img[0]
                image_bytes = doc.extract_image(xref)["image"]
                text = extract_text_from_image(image_bytes)
                print('LA: '+ text)
                return text

                


def extract_text_from_image(image_bytes):
    text = ''
    response = textract.detect_document_text(Document={'Bytes': image_bytes})
    
    for item in response['Blocks']:
        if item['BlockType' ] == 'LINE':
            text += item['Text'] + '\n'
    print('AQUI: '+ text)
    return text
    
    

doc = extract_image_from_pdf('C:/Users/jeffe/Downloads/matricula-6.pdf')

response = extraction_chain.invoke(doc)
print(response)