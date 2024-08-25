import fitz  # PyMuPDF
import os

def extract_first_image_from_pdf(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through pages
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)

        if image_list:
            xref = image_list[0][0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(output_folder, f"profile_picture.{image_ext}")
            
            # Save the image
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            print(f"Profile picture saved: {image_filename}")
            return  # Exit after saving the first image

    print("No images found in the PDF.")

# Usage
pdf_path = r"C:\Users\Mega-Pc\Desktop\wrk\source-code-face-recognition\source code\cv.pdf"  # Path to your PDF file
output_folder = r"C:\Users\Mega-Pc\Desktop\wrk\source-code-face-recognition\source code\images"  # Path to your output folder

extract_first_image_from_pdf(pdf_path, output_folder)
