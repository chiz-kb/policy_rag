# Policy RAG Assistant

An AI-powered document question-answering application built with **Django, LangChain, Google Gemini, and ChromaDB**.

The application allows users to ask questions about office documents and receive context-aware answers using Retrieval-Augmented Generation (RAG).

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| LangChain | RAG pipeline orchestration |
| Google Gemini | Large Language Model (LLM) |
| Gemini Embeddings / Sentence Transformers | Text embeddings |
| ChromaDB | Vector database |
| PyPDF | PDF text extraction |
| Tesseract OCR | Extract text from scanned PDFs |
| HTML & CSS | Frontend interface |
| JavaScript | Chat interactions |
| Marked.js | Markdown rendering |
| DOMPurify | Sanitize rendered HTML |

## System Architecture

```text
             USER
               |
               v
       Django Web Interface
               |
               v
        User Question
               |
               v
        Question Embedding
               |
               v
           ChromaDB
               |
               v
       Relevant Document Chunks
               |
               v
        Context + Question
               |
               v
         Google Gemini
               |
               v
         Generated Answer
               |
               v
        Django Backend
               |
               v
        Chat Interface
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/office-rag.git
cd office-rag
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google Gemini API

Obtain a Gemini API key from:

https://aistudio.google.com/apikey

Create a `.env` file in your project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

GOOGLE_API_KEY=your-gemini-api-key
```

Load environment variables in Django/Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Django Server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## How RAG Works

The application follows these steps:

1. **Document Loading:** Extract text from PDF documents.
2. **Text Splitting:** Divide documents into manageable chunks.
3. **Embedding Generation:** Convert document chunks into vector representations.
4. **Vector Storage:** Store embeddings in ChromaDB.
5. **Retrieval:** Find relevant chunks based on the user's question.
6. **Augmentation:** Combine retrieved content with the user's question.
7. **Generation:** Google Gemini generates an answer using the retrieved context.
8. **Response:** Django returns the answer to the chat interface.

## Future Improvements

- Support multiple document formats.
- Add document upload and management.
- Implement conversation history and chat memory.
- Add source citations and page references.
- Support multiple users and document-level access control.
- Implement streaming responses.
- Add document management dashboards.
- Deploy using Docker and Nginx.

## Security Considerations

- Store Gemini API keys in environment variables.
- Never commit `.env` files.
- Validate uploaded documents.
- Sanitize Markdown-rendered HTML.
- Configure appropriate document access permissions.
- Set `DEBUG=False` in production.

## License

This project is available under the MIT License. Update this section if you choose a different license.

---

**Office RAG Assistant** – Making organizational knowledge accessible through AI-powered document search and question answering.
