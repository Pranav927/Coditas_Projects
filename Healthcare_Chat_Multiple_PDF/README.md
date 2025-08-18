# Healthcare Document Intelligence System
### Problem Statement:
The purpose revolves around the endless research doctors have to do in case of emergencies or situations where research is the only way to resolve a patients problem.
### Solution:
An AI powered system which reads through multiple PDF documents and pin points to the content the doctor is looking for.

## Project Evolution
This healthcare document intelligence system builds upon a robust PDF chat foundation, enhanced specifically for medical professionals with:

Free, Local Processing: Migrated from OpenAI API to Ollama for cost-free, privacy-compliant operation

Real-time Medical Knowledge: Added PubMed integration for access to 35+ million medical citations

Medical Domain Expertise: Upgraded to BioBERT/ClinicalBERT embeddings for medical text understanding

Professional Healthcare UI: Clean, medical-grade interface without consumer app elements

HIPAA Compliance: All processing happens locally with medical disclaimers

## Key Features (Enhanced)

- Multiple PDF document processing

- Intelligent text chunking

- Vector similarity search

- Conversational memory

- Source attribution

- Clean Streamlit interface

## Healthcare Enhancements

- 100% Free Operation: Zero API costs with Ollama

- Medical Literature Access: Real-time PubMed integration

- Domain Expertise: BioBERT embeddings for medical accuracy

- Privacy Compliant: Local processing for HIPAA compliance

- Evidence-Based Responses: Automatic medical source citation

Professional UI: Medical-grade interface design
---

## ⚠Assumptions and Caveats

The following assumptions were made during the development of this project:

- **Assumption 1**: The uploaded PDFs are text-based (not scanned images).
- **Assumption 2**: The PDF text content is in a format that the language model can process effectively.
- **Assumption 3**: The embeddings created by the **Gemini model** are stored securely in the local environment.

---

## Project Links

![Chat with PDF image](https://github.com/user-attachments/assets/490dcdc8-b469-4f5b-ae50-d3ca78c802b3)

---

## How to Run the Project

1. Clone the repository.
2. Install the required dependencies using:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your **Google Generative AI** API Key in your `.env` file.
4. Run the application using:
    ```bash
    streamlit run app.py
    ```
5. Upload PDF files and ask questions to interact with the PDF content.

---
