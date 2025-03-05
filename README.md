# Neo4j Knowledge Graph Generator

This tool facilitates the creation of a knowledge graph from unstructured text from PDF documents and their subsequent storage in a Neo4j database. It is ideal for processing documents like insurance policies or annual reports.

## Prerequisites

Before you begin, ensure that Python 3.x is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

## Setting Up PDF Ingestion

### Prepare your PDFs

Ensure your PDF files are formatted correctly for ingestion. Update the `main.py` file with a list of documents as shown in the sample structure:

```json
{
    "url": "PDF URL https://...",
    "title": "Title of the pdf",
    "context": "Insurance Document or Annual Report"
}
```

### Install Dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Set up the necessary environment variables:

1. Copy the sample environment configuration file:
```bash
cp .env.example .env
```

2. Fill in the details in `.env` for OpenAI and your Neo4j database.

### Start the Ingestion Process

Launch the application to begin importing your PDFs into Neo4j:

```bash
python main.py
```

## Launching the User Interface

### Run the Streamlit Application

To start the Streamlit-based user interface, use the following command from the root of the repository:

```bash
streamlit run ./ui/chatbot.py
```

This command initializes the UI, allowing you to interact with the extracted text data through a convenient web interface.