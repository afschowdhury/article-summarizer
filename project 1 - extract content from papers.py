import os

from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path, output_txt="extracted_text.txt"):
    """Extracts and saves text from a PDF file."""
    try:
        if not os.path.exists(pdf_path):
            print("Error: File not found.")
            return None

        text = extract_text(pdf_path)  # Extract text

        if not text.strip():
            print(" No text found in PDF. It may be scanned.")
            return None

        # Save extracted text to a file
        with open(output_txt, "w", encoding="utf-8") as file:
            file.write(text)

        print(f" Text extracted and saved to {output_txt}")
        return text  # Return the extracted text

    except Exception as e:
        print(f" Error extracting text: {e}")
        return None

#Use the correct file path format
#you can add here the paths for 9 other pdfs
pdf_path = r"C:\Users\menna_zoi0oau\Desktop\python-project.pdf"  # Ensure this file exists

# Run the function
extracted_text = extract_text_from_pdf(pdf_path)

# Print a preview of the extracted text
if extracted_text:
    print("\n Extracted Text (Preview):\n", extracted_text[:500])  # First 500 characters











