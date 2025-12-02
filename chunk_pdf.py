"""
FILENAME: chunk_pdf.py
1. Loads a PDF
2. Extracts all text
3. Chunks the text automatically into configurable sizes (set to 2000)
4. Outputs a list of chunks OR saves them to disk as a JSON file
5. Is plug and play for loading later into RAG engine

Bottom of code is commented out example of output and how to use in RAG engine
"""

import json
from pathlib import Path
from pypdf import PdfReader
import nltk

# pip install pypdf
# pip install nltk

# Ensure sentence tokenizer is available
nltk.download("punkt")


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extracts all text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF handbook.

    Returns:
        str: Raw extracted text.
    """
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def chunk_text(text: str, max_chars: int = 1000) -> list:
    """
    Splits text into chunks using sentence boundaries,
    ensuring each chunk does not exceed max_chars.

    Args:
        text (str): Raw text.
        max_chars (int): Target size of each chunk.

    Returns:
        list: List of chunk strings.
    """

    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding the sentence exceeds the size, start a new chunk
        if len(current_chunk) + len(sentence) + 1 > max_chars:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence

    # Append the final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def save_chunks_to_json(chunks: list, output_path: str):
    """
    Saves chunks to a JSON file for loading into RAG engine.

    Args:
        chunks (list): List of text chunks.
        output_path (str): File path to save output JSON.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks}, f, indent=2, ensure_ascii=False)


def main():
    PDF_INPUT = "student-handbook-25-26.pdf" # change pdf file name as needed
    OUTPUT_JSON = "student_handbook-25-26_chunks.json" # change json file name as needed
    MAX_CHARS = 2000  # adjust if needed

    print("Extracting PDF text...")
    text = extract_pdf_text(PDF_INPUT)

    print("Chunking text...")
    chunks = chunk_text(text, max_chars=MAX_CHARS)

    print(f"Total chunks created: {len(chunks)}")

    print("Saving to JSON...")
    save_chunks_to_json(chunks, OUTPUT_JSON)

    print(f"Done! Chunks saved in: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()



"""
Example of output Structure
Stored in student-handbook-25-26_chunks.json

{
  "chunks": [
    "Chunk 1 text...",
    "Chunk 2 text...",
    "Chunk 3 text..."
  ]
}

"""

"""
How to use these chucks in our RAG Engine
inside the RAG engine ingestion function:

import json

def load_chunks_into_rag(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for chunk in data["chunks"]:
        rag_engine.add_document(chunk)  # your vector insert method
"""

"""
Working on a version that will chunk and embed automatically with Ollama...
TO BE CONTINUED.....
"""