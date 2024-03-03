import fitz
import boto3

textract = boto3.client('textract')



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
    
    

extract_image_from_pdf('C:/Users/jeffe/Downloads/matricula-6.pdf')