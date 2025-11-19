# pip install pdfreader
from pdfreader import SimplePDFViewer
import os

# This file is for computer reading only it is hard for people to read
def read_pdf(file_path):
    # Variables
    pdf_full_text = ""

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Open the pdf file
    fd = open("student-handbook-25-26.pdf", "rb")
    viewer = SimplePDFViewer(fd)

    for canvas in viewer:
        viewer.render()
        text = viewer.canvas.text_content
        pdf_full_text += text + " "

    # close the file
    fd.close()

    return pdf_full_text


def main():
    prompt = read_pdf("student-handbook-25-26.pdf")
    print(prompt)


if __name__ == "__main__":
    main()




