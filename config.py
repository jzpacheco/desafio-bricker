import boto3
from langchain_openai import ChatOpenAI
from langchain.chains import create_structured_output_runnable
from langchain.prompts import ChatPromptTemplate

textract = boto3.client('textract')
openai_key = ""

structured_schema = {
    "type": "object",
    "properties": {
        "expedition_date": {"type": "string", "description":"data de emissão do presente documento retorne no formato dd/mm/aaaa"},
        "responsible_registry": {"type": "string", "description": "nome do cartório que emitiu o documento"},
        "registration_number": {"type": "string", "description": "Número da matrícula do imóvel"},
        "property_type": {"type": "string", "description": "Tipo do imóvel (lote, prédio residencial, apartamento, terreno, vaga de garagem) IMPORTANTE: converta 'terreno urbano' é a mesma coisa que 'terreno' então retorne 'terreno' se o tipo for 'terreno urbano'; IMPORTANTE: no caso de prédio e respectivo terreno sempre retorne prédio;"},
        "batch": {"type": "string", "description": "apenas o lote do terreno, indique se é o lote inteiro ou se é partes ou parte do lote;"},
        "block": {"type": "string", "description": "a quadra do imóvel (se houver, somente número/nome da quadra)"},
        "street": {"type": "string", "description": "A primeira rua do imóvel, escrever no começo se é rua, avenida, etc"},
        "street_2": {"type": "string", "description": "A segunda rua do imóvel, escrever no começo se é rua, avenida, etc"},
        "property_number": {"type": "string", "description": "sempre que houver, Número endereço do imóvel. Apenas o primeiro número encontrado no endereço."},
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
    "required": ["garnishment", "expedition_date", "responsible_registry", "registration_number", "property_type", "batch", "block", "street", "street_2", "property_number", "property_number_2", "address_complement", "neighborhood", "city", "state", "property_footage", "owners_quantity", "owner_1", "owner_2", "document_owner_1", "document_owner_2", "mortgage", "mortgage_owner_name", "mortgage_owner_document", "fiduciary_alienation", "fiduciary_alienation_owner_name", "fiduciary_alienation_owner_document"]
}

prompt = ChatPromptTemplate.from_messages([
    ("system", "When not found a value and isnt explicit the return, return 'n/a' instead a empty string"), 
    ("human", "{input}")
])

llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=openai_key)
extraction_chain = create_structured_output_runnable(structured_schema, llm)