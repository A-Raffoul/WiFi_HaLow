import fitz  # PyMuPDF
import os

# Get the path to the user's desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Define paths
input_path = os.path.join(desktop_path, "Conference presentation_6_50.pdf")
output_path = os.path.join(desktop_path, "Conference_presentation_handout.pdf")

# Open the PDF
doc = fitz.open(input_path)

# Create a new PDF for the handout
handout_doc = fitz.open()

# Get the size of the pages
page_width = doc[0].rect.width
page_height = doc[0].rect.height

# Iterate through the pages, two at a time
for i in range(0, len(doc), 2):
    # Create a new page with double width
    new_page = handout_doc.new_page(width=2 * page_width, height=page_height)
    
    # Insert the first slide on the left
    new_page.show_pdf_page(fitz.Rect(0, 0, page_width, page_height), doc, i)
    
    # Insert the second slide on the right, if it exists
    if i + 1 < len(doc):
        new_page.show_pdf_page(fitz.Rect(page_width, 0, 2 * page_width, page_height), doc, i + 1)

# Save the handout PDF
handout_doc.save(output_path)

output_path
