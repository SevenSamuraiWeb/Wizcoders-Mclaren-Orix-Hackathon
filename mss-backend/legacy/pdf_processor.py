import fitz  # PyMuPDF
import pdfplumber
import io


class PDFProcessor:
    """
    Handles PDF processing tasks including text and table extraction.
    """

    def __init__(self, file_bytes: bytes):
        """
        Initialize with PDF file bytes.
        """
        self.file_bytes = file_bytes
        self.stream = io.BytesIO(file_bytes)

    def parse(self):
        """
        Orchestrates the parsing of the PDF to extract text and tables.

        Returns:
            list: A list of result objects for each page.
                  Example: [{'page': 1, 'text': '...', 'tables': [...]}, ...]
        """
        text_data = self._extract_text_with_fitz()
        table_data = self._extract_tables_with_plumber()

        # Merge data by page index
        merged_data = []
        num_pages = max(len(text_data), len(table_data))

        for i in range(num_pages):
            page_content = {
                "page": i + 1,
                "text": text_data[i] if i < len(text_data) else "",
                "tables": table_data[i] if i < len(table_data) else [],
            }
            merged_data.append(page_content)

        return merged_data

    def _extract_text_with_fitz(self):
        """
        Extracts text page-by-page using PyMuPDF (fitz).
        """
        doc = fitz.open(stream=self.file_bytes, filetype="pdf")
        texts = []
        for page in doc:
            texts.append(page.get_text())
        doc.close()
        return texts

    def _extract_tables_with_plumber(self):
        """
        Extracts tables page-by-page using pdfplumber.
        """
        tables_list = []
        # pdfplumber requires a file-like object
        with pdfplumber.open(self.stream) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                tables_list.append(extracted_tables)
        return tables_list
