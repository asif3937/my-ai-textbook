# Research: Integrated RAG Chatbot for Book Content

## Decision: Vector Database Selection
**Rationale**: Chose Qdrant Cloud for vector storage due to its managed service offering, which matches the feature requirements and allows for efficient similarity search operations needed for RAG.
**Alternatives considered**: 
- Pinecone: Another managed vector database but with potentially higher costs
- FAISS: Open source option but requires self-hosting and management
- Weaviate: Another vector database option but with different feature set

## Decision: AI Provider Selection
**Rationale**: Supporting both Cohere and OpenAI APIs based on the feature specification requirements. Cohere will be the primary provider for embeddings due to its efficient embedding models, with OpenAI for generation due to its strong language understanding capabilities.
**Alternatives considered**:
- Using only one provider: Limiting flexibility and potentially vendor lock-in
- Open source LLMs: Additional complexity for model hosting and maintenance

## Decision: Text Chunking Strategy
**Rationale**: Chapter- and paragraph-aware segmentation with overlapping windows to preserve context while enabling efficient retrieval. This approach maintains semantic coherence while allowing for accurate citations.
**Alternatives considered**:
- Fixed-length token chunks: Might break up semantic units
- Sentence-level chunks: Could result in too many small chunks
- Paragraph-level only: Might result in chunks that are too large for context windows

## Decision: API Architecture
**Rationale**: FastAPI-based RESTful API with Pydantic models for request/response validation, following the constitution's API-first design principle and async patterns for performance.
**Alternatives considered**:
- GraphQL API: More complex for this use case
- Traditional Flask: Doesn't align with the constitution's preference for FastAPI

## Decision: Book Content Format
**Rationale**: Support for plain text initially with potential expansion to Markdown and HTML, as these formats are easiest to process while maintaining structural information needed for citations.
**Alternatives considered**:
- PDF support: Complex processing required for layout and structure
- EPUB support: Additional parsing complexity
- Multiple format support from the start: Increased initial complexity

## Decision: Selected-Text Mode Implementation
**Rationale**: Client-side context passing with server-side validation. The selected text will be passed with each query when in selected-text mode, with server-side validation to ensure only that text is used for generation.
**Alternatives considered**:
- Server-side context management: More complex session management
- Storing selections in database: Unnecessary persistence for temporary selections

## Decision: Citation Format
**Rationale**: Citations will include chapter, page, and paragraph information that maps back to the original book content, allowing users to verify information and navigate to source content.
**Alternatives considered**:
- Just paragraph numbers: Less granular navigation
- Character ranges: More precise but less user-friendly
- Vector IDs: Not meaningful to users