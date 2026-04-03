from PIL import Image
import pytesseract

from langchain_community.document_loaders import PyPDFLoader

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

'''
OCR Weakness:
- Can't read human text
- Can't understand complex diagrams like tables
'''

def extract_text_from_image(path):
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf(path):
    loader = PyPDFLoader(path)
    docs = loader.load()

    text = "\n\n".join(doc.page_content for doc in docs)
    return text

def extract(paths):
    if not paths:
        return
    
    full_text = ''
    for path in paths:
        if path.endswith(".pdf"):
            full_text += extract_text_from_pdf(path)
        elif path.endswith((".png", ".jpg", ".jpeg")):
            full_text += extract_text_from_image(path)

    return full_text