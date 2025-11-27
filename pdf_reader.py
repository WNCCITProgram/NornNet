import os
try:
    # Optional dependency; install with `pip install pdfreader` if you need PDF parsing
    from pdfreader import SimplePDFViewer
except Exception:
    SimplePDFViewer = None


def read_pdf(file_path):
    """Read text from `file_path` using pdfreader when available.

    Returns an empty string if pdfreader is not installed or the file is missing.
    """
    pdf_full_text = ""
    if not os.path.exists(file_path):
        print(f"PDF not found: {file_path}")
        return pdf_full_text

    if SimplePDFViewer is None:
        print("pdfreader package not installed; skipping PDF parsing.")
        return pdf_full_text

    try:
        with open(file_path, "rb") as fd:
            viewer = SimplePDFViewer(fd)
            for canvas in viewer:
                viewer.render()
                text = getattr(viewer.canvas, 'text_content', '')
                pdf_full_text += (text or '') + " "
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")

    return pdf_full_text


def main():
    prompt = read_pdf("student-handbook-25-26.pdf")
    print(prompt)


if __name__ == "__main__":
    main()




