# AI Textbook RAG Chatbot - Fullstack Implementation

This project implements a RAG (Retrieval-Augmented Generation) chatbot that connects to your textbook content. The system consists of a backend API and a frontend Docusaurus site with an integrated AI chat interface.

## Security Notice

⚠️ **IMPORTANT**: This project contains sensitive configuration that must be properly secured before public deployment. Please read the [SECURITY.md](./SECURITY.md) file for complete security guidelines.

## Project Structure

- `backend/` - FastAPI backend with RAG functionality
- `textbook/` - Docusaurus frontend with AI Chat integration

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Access to Cohere API key (for embeddings)
- Access to Qdrant vector database
- PostgreSQL database (Neon)

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   # or if using the basic requirements
   pip install -r requirements-basic.txt
   ```

3. **Security Setup**: Create a `.env` file in the backend directory with your actual credentials (do NOT commit this file):
   ```env
   # Database Configuration
   NEON_DATABASE_URL=your_neon_database_url_here

   # Vector Database Configuration
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=book_content_chunks

   # Embeddings and AI Services
   COHERE_API_KEY=your_cohere_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here

   # LLM Configuration
   LLM_MODEL=gpt-3.5-turbo
   LANGUAGE_MODEL_PROVIDER=cohere

   # Application Configuration
   SECRET_KEY=your_secret_key_here
   DEBUG=true
   ```

4. Start the backend server:
   ```bash
   python -m uvicorn main:app --reload
   ```
   The backend will be available at `http://127.0.0.1:8000`

## Frontend Setup

1. Navigate to the textbook directory:
   ```bash
   cd textbook  # from the root of the project
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```
   The frontend will be available at `http://localhost:3000`

## Book Ingestion

Before using the chatbot, you need to ingest your textbook content:

1. Make sure your backend server is running
2. Run the ingestion script:
   ```bash
   python ingest_real_textbook.py
   ```
   This will read your textbook content from the `textbook/docs` directory and ingest it into the RAG system

The default book ID for your textbook is: `bd8add9a-3444-4a7d-978b-ca0952c59bca`

## Using the AI Chat

1. Access the AI Chat through the "AI Chat" link in the navigation bar
2. Type your questions about the textbook content
3. The AI assistant will retrieve relevant information from your textbook and generate responses

## API Endpoints

- `POST /api/v1/chat` - Chat with the RAG system
- `POST /api/v1/books/ingest` - Ingest new book content
- `POST /api/v1/sessions` - Create a new chat session

## Security Guidelines

For complete security guidelines, please read the [SECURITY.md](./SECURITY.md) file which explains:
- How credentials are protected
- Best practices for environment variables
- What files are excluded from Git
- How to properly set up for public deployment

## Troubleshooting

1. **Backend not responding**: Make sure the backend server is running on `http://127.0.0.1:8000`
2. **No responses**: Verify that your textbook content has been properly ingested
3. **API key errors**: Check that your Cohere and Qdrant API keys are valid
4. **Database errors**: Ensure your Neon database connection is working

## Production Deployment

For production deployment:

1. Update the `url` in `docusaurus.config.ts` to your production domain
2. Set up environment variables for your hosting platform (do not commit actual credentials)
3. Build the frontend: `npm run build`
4. Deploy the build output to your hosting service
5. Deploy the backend to a service like Railway, Render, or AWS
6. Follow security guidelines in [SECURITY.md](./SECURITY.md)

## Default Book ID

The AI Chat component is configured to use your textbook content by default with the book ID: `bd8add9a-3444-4a7d-978b-ca0952c59bca`. This means users don't need to specify a book ID when asking questions.