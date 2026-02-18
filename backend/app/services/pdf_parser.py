import pdfplumber
from io import BytesIO


def extract_text_from_pdf(file_bytes):

    text_blocks = []

    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            if tables:
                for table in tables:
                    for row in table:
                        if row:
                            cleaned = [cell.strip() for cell in row if cell]
                            text_blocks.append(" ".join(cleaned))

            else:
                page_text = page.extract_text()
                if page_text:
                    text_blocks.append(page_text)

    return "\n".join(text_blocks)
