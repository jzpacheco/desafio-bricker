import fitz

def extract_image_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            images = page.get_images(full=True)
            print(images)

            for i, img in enumerate(images):
                xref= img[0]
                image_bytes = doc.extract_image(xref)["image"]
                print(image_bytes)


def extract_text_from_image(image_bytes):
    

extract_image_from_pdf('C:/Users/jeffe/Downloads/matricula-6.pdf')