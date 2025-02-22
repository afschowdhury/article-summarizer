import os
import requests
import certifi

# Define the folder where papers should be saved
save_folder = "C:/Users/menna_zoi0oau/desktop"

# Define the full file path - write any name you like
pdf_file = os.path.join(save_folder, "Tipping_in_Restaurants.pdf")

#PDF URL - has to be open access

pdf_url1 = "https://d1wqtxts1xzle7.cloudfront.net/1961510/Structure_of_Behavior_TOC-libre.pdf?1390824250=&response-content-disposition=inline%3B+filename%3DTable_of_Contents_from_Merleau_Pontys_La.pdf&Expires=1740188719&Signature=GexC2L3qyN1wvgSo-VC7ZBn9yfhXgrxGj-z~gWpYKjBNC0vlpo68xJ6uoNmitPjMRMBMlSNuUq49V1aw1faWwbSdHBD63IPy-nGITIyu~Yygly0yMJvv4iGJotaT8xbLjcB6Lmko3vl6T-jLerqzKl5kfeCBnfEf~os9-BLuJttnCGvmX1vzb4-~sdnkELTY7v9upOFRDKZWLAWZOoItwdHrDN7uNVcuM~Zm9S7FvbG7FGuGKqDO1k1pG7Zd760A2I5f5L2uYggtnTcGTD40-CLLkn-HprrwR6OHWRZ4O8iBkL7Loa3c6Jb181ewNvZoc464mz8vdm1flQ1zpMyckA__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA"


# Download the PDF -make sure to change the path

response = requests.get(pdf_url1, verify=certifi.where())

# Save to the specific folder
with open(pdf_file, "wb") as file:
    file.write(response.content)

print(f"PDF downloaded successfully to: {pdf_file}")   #make sure it downloads




#Use the correct file path format
#you can add here the paths for 9 other pdfs
pdf_path = r"C:\Users\menna_zoi0oau\Desktop\Tipping_in_Restaurants.pdf"  # Ensure this file exists


#make sure the pdf opens and sees how many pages are there
import PyPDF2

pdf_path = "C:/Users/menna_zoi0oau/Desktop/Tipping_in_Restaurants.pdf"

try:
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        print(f"PDF contains {len(reader.pages)} pages.")
except Exception as e:
    print("Error opening PDF:", e)


#read pdfs

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



# Run the function to extract everything uptp 10000 words 
extracted_text = extract_text_from_pdf(pdf_path)

# Print a preview of the extracted text
if extracted_text:
    print("\n Extracted Text (Preview):\n", extracted_text[:10000])  # First 10000 characters



























