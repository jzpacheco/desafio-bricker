import fitz
import boto3

from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain, create_structured_output_runnable
#from google.cloud import vision

textract = boto3.client('textract')
#client = vision.ImageAnnotatorClient()
openai_key = "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"

structured_schema = {
    "type": "object",
    "properties": {
        "expedition_date": {"type": "string", "description": "Data em que a certidão está sendo redigida retorne no formato dd/mm/aaaa"},
        "responsible_registry": {"type": "string", "description": "nome do cartório que emitiu o documento"},
        "registration_number": {"type": "string", "description": "Número da matrícula do imóvel"},
        "property_type": {"type": "string", "description": "Tipo do imóvel (lote, prédio residencial, apartamento, terreno, vaga de garagem) IMPORTANTE: converta 'terreno urbano' é a mesma coisa que 'terreno' então retorne 'terreno' se o tipo for 'terreno urbano'; IMPORTANTE: no caso de prédio e respectivo terreno sempre retorne prédio;"},
        "batch": {"type": "string", "description": "apenas o lote do terreno, indique se é o lote inteiro ou se é partes ou parte do lote;"},
        "block": {"type": "string", "description": "a quadra do imóvel (se houver, somente número/nome da quadra)"},
        "street": {"type": "string", "description": "A primeira rua do imóvel, escrever no começo se é rua, avenida, etc"},
        "street_2": {"type": "string", "description": "A segunda rua do imóvel, escrever no começo se é rua, avenida, etc"},
        "property_number": {"type": "string", "description": "sempre que houver, pegar o primeiro número do endereço do imóvel"},
        "property_number_2": {"type": "string", "description": "sempre que houver, pegar o segundo número do endereço do imóvel"},
        "address_complement": {"type": "string", "description": "o número do apartamento, número do bloco ou número da vaga de garagem. IMPORTANTE: SOMENTE o número;"},
        "neighborhood": {"type": "string", "description": "pegar APENAS o bairro onde fica localizado o imóvel"},
        "city": {"type": "string", "description": "pegar APENAS a cidade onde fica localizado o imóvel"},
        "state": {"type": "string", "description": "estado onde o imóvel fica localizado retorne o nome COMPLETO do estado"},
        "property_footage": {"type": "string", "description": "pegar APENAS o primeiro tamanho do imóvel que encontrar e remover a unidade de medida"},
        "owners_quantity": {"type": "string", "description": "Quantidade de donos ATUAIS do imóvel, retorne como número"},
        "owner_1": {"type": "string", "description": "Nome Completo do primeiro proprietário"},
        "owner_2": {"type": "string", "description": "Nome Completo do segundo proprietário (se houver)"},
        "document_owner_1": {"type": "string", "description": "CPF ou CNPJ do proprietário principal (PADRÃO CPF: 000.000.000-00) (PADRÃO CNPJ: 00.000.000/0000-00)"},
        "document_owner_2": {"type": "string", "description": "CPF ou CNPJ do proprietário secundário (se houver) (PADRÃO CPF: 000.000.000-00) (PADRÃO CNPJ: 00.000.000/0000-00)"},
        "mortgage": {"type": "string", "description": "Indique se o imóvel está em hipoteca (sim ou não) retorne sim ou não"},
        "mortgage_owner_name": {"type": "string", "description": "Nome do dono da hipoteca (se houver)"},
        "mortgage_owner_document": {"type": "string", "description": "CPF ou CNPJ do proprietário da hipoteca (se houver)"},
        "fiduciary_alienation": {"type": "string", "description": "Indique se o imóvel está em alienação fiduciária retorne sim ou não"},
        "fiduciary_alienation_owner_name": {"type": "string", "description": "Nome do dono da alienação fiduciária (se houver)"},
        "fiduciary_alienation_owner_document": {"type": "string", "description": "CPF ou CNPJ do proprietário da alienação fiduciária (se houver) (PADRÃO CPF: 000.000.000-00) (PADRÃO CNPJ: 00.000.000/0000-00)"},
        "garnishment": {"type": "string", "description": "Imóvel está em penhora (sim ou não) retorne sim ou não"}
    },
    "required":["garnishment"]
}

llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=openai_key)

extraction_chain = create_structured_output_runnable(structured_schema, llm)

def extract_image_from_pdf(pdf_path):
  
    with fitz.open(pdf_path) as doc:
        all_text = ''
        for page_num, page in enumerate(doc):
            
            images = page.get_images(full=True)
            for i, img in enumerate(images):
                xref= img[0]
                image_bytes = doc.extract_image(xref)["image"]
                text = extract_text_from_image(image_bytes)
                all_text += text

        return all_text

                


def extract_text_from_image(image_bytes):
    text = ''
    params = {"Document":{'Bytes': image_bytes}}
    next_token = None
    while True:
        if next_token:
            response = textract.detect_document_text(**params, NextToken = next_token)
        else:
            response = textract.detect_document_text(**params)

        for item in response['Blocks']:
            if item['BlockType' ] == 'LINE':
                text += item['Text'] + '\n'

        if 'NextToken' in response:
            print("ENTROU")
            next_token = response['NextToken']
        else:
            break
    return text
    
    

doc = extract_image_from_pdf('C:/Users/jeffe/Downloads/matricula-6.pdf')

data = extraction_chain.invoke(doc)
print(data)