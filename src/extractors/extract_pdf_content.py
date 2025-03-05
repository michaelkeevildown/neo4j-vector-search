import fitz


def read_pdf_split_by_page(pdf_bytes, title):
    """
    Processes the given PDF bytes and extracts information page by page.
    Returns a structured document containing the extracted data.
    """
    # Open the PDF from bytes
    doc = fitz.open("pdf", pdf_bytes)

    # Initialize variables
    page_num = 0
    parsed_document = {'title': title, 'document_type': "pdf", 'pages': []}

    # Process each page in the PDF
    for page in doc:
        page_text = page.get_text()
        page_num += 1

        # Check if the page is not blank
        if page_text.strip():
            # Append processed content to the document
            parsed_document['pages'].append({'page_number': page_num, 'text': page_text})

        # if page_num == 10:  # Assuming you want to stop after 3 pages for demonstration
        #     break

    print("PDF Parsed")

    doc.close()
    return parsed_document
