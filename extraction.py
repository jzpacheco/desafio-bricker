import fitz
from config import textract, extraction_chain, prompt
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

def process_pdf(pdf_path):
    doc = extract_image_from_pdf(pdf_path)
    chain = prompt | extraction_chain
    data = chain.invoke({"input": doc})
    return data