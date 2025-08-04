import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


poppler_path = r"poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

def convert_image_to_pdf(image_path: str) -> str:
        """
        Converts an image file to PDF and returns the new PDF file path.
        """
        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")  # Ensure compatibility
                pdf_path = os.path.splitext(image_path)[0] + ".pdf"
                img.save(pdf_path, "PDF")
                print(f"Converted image to PDF: {pdf_path}")
                return pdf_path
        except Exception as e:
            print(f"Failed to convert image to PDF: {image_path}, Error: {e}")
            raise


def extract_text_from_page(pdf_path):
        try:
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img, lang="eng") + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from page: {e}")
            return ""


def extract_text_from_pdf(pdf_path):
        try:            
            final_text = extract_text_from_page(pdf_path)
            return final_text

        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""


def get_unique_output_txt_filename(input_filename, output_folder='output'):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Extract base name without extension
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    txt_filename = f"{base_name}.txt"
    txt_path = os.path.join(output_folder, txt_filename)

    # Check if file exists, and add counter if needed
    counter = 1
    while os.path.exists(txt_path):
        txt_filename = f"{base_name} ({counter}).txt"
        txt_path = os.path.join(output_folder, txt_filename)
        counter += 1

    return txt_path



file_path = input("Enter the file path: ")

ext = os.path.splitext(file_path)[1].lower()
if ext in ('.jpg', '.jpeg', '.png', '.webp'):
    file_path = convert_image_to_pdf(file_path)

print(f"Processing: {os.path.basename(file_path)}")
text = extract_text_from_pdf(file_path)

file_path = get_unique_output_txt_filename('sample.pdf')

with open(file_path, 'w') as file:
     file.write(text)

print(f"Text saved in f{file_path}")

