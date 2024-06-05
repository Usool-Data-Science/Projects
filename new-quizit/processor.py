import PyPDF2
import docx
import os

def read_file_content(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    tempfile = ""

    if file_extension == '.pdf':
        tempfile = read_pdf(file_path)
    elif file_extension == '.docx':
        tempfile = read_docx(file_path)
    elif file_extension == '.txt':
        tempfile = read_txt(file_path)
    else:
        raise ValueError("Unsupported file type: {}".format(file_extension))

    return tempfile

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = []
        for page in reader.pages:
            content.append(page.extract_text())
        return "\n".join(content)

def read_docx(file_path):
    doc = docx.Document(file_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return "\n".join(content)

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    pass
