---

description: "Task list for RAG Chatbot implementation"
---

# Tasks: Integrated RAG Chatbot for Book Content

**Input**: Design documents from `/specs/001-rag-chatbot-book/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `api/`, `config/`, `models/`, `services/`, `utils/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume backend structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan: api/, config/, models/, services/, utils/
- [ ] T002 Initialize Python 3.9+ project with FastAPI, Qdrant, Cohere API, OpenAI API, SQLAlchemy, Pydantic dependencies in requirements.txt
- [ ] T003 [P] Create requirements.txt with all required dependencies
- [ ] T004 [P] Create .env.example with all required environment variables
- [ ] T005 Create main.py with basic FastAPI app setup
- [ ] T006 Setup Dockerfile for containerization

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T007 Setup PostgreSQL database connection in config/database.py using SQLAlchemy
- [ ] T008 [P] Configure environment configuration management in config/__init__.py
- [ ] T009 [P] Setup Qdrant vector database service in services/qdrant_service.py
- [ ] T010 Create base models: BookContent, Session, and ChatHistory in models/ directory
- [ ] T011 Configure error handling and logging infrastructure in utils/
- [ ] T012 Setup API routing structure in api/ with proper endpoints organization
- [ ] T013 Implement security utilities for credential handling in utils/security.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Book-Aware Question Answering (Priority: P1) 🎯 MVP

**Goal**: Enable users to ask questions about book content and receive accurate answers based only on the book's text, preventing hallucinations.

**Independent Test**: Can be fully tested by asking questions about book content and verifying that answers come from the text, not external sources, delivering immediate value to readers.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T014 [P] [US1] Contract test for POST /chat endpoint in tests/contract/test_chat.py
- [ ] T015 [P] [US1] Integration test for book-aware QA flow in tests/integration/test_book_qa.py

### Implementation for User Story 1

- [ ] T016 [P] [US1] Create UserQuery model in models/user_query.py
- [ ] T017 [P] [US1] Create RetrievedContext model in models/retrieved_context.py
- [ ] T018 [P] [US1] Create GeneratedResponse model in models/generated_response.py
- [ ] T019 [P] [US1] Create ContentChunk model in models/content_chunk.py
- [ ] T020 [US1] Implement EmbeddingService in services/embedding_service.py
- [ ] T021 [US1] Implement RetrievalService in services/retrieval_service.py
- [ ] T022 [US1] Implement GenerationService in services/generation_service.py
- [ ] T023 [US1] Implement BookContentService in services/book_content_service.py
- [ ] T024 [US1] Create chat endpoints in api/rag/routes/chat.py
- [ ] T025 [US1] Implement query validation logic for book-aware mode
- [ ] T026 [US1] Add logic to detect and reject external information in responses
- [ ] T027 [US1] Add logging for book-aware question answering operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Selected-Text-Only Mode (Priority: P1)

**Goal**: Allow users to select specific text in the book and get answers based only on that selection, refusing to answer if information is missing.

**Independent Test**: Can be fully tested by selecting specific text, asking questions about it, and ensuring the chatbot uses only that text as context, delivering focused answers.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T028 [P] [US2] Contract test for selected-text mode in POST /chat endpoint in tests/contract/test_chat.py
- [ ] T029 [P] [US2] Integration test for selected-text-only flow in tests/integration/test_selected_text.py

### Implementation for User Story 2

- [ ] T030 [P] [US2] Enhance UserQuery model to support selected text in models/user_query.py
- [ ] T031 [US2] Implement validation for selected-text mode in services/book_content_service.py
- [ ] T032 [US2] Add query router logic to detect selected-text mode in api/rag/services/retrieval_service.py
- [ ] T033 [US2] Implement selected-text-only constraint enforcement in GenerationService
- [ ] T034 [US2] Add logic to return "The answer is not available in the provided text." when context is insufficient
- [ ] T035 [US2] Update chat endpoints to handle selected text mode in api/rag/routes/chat.py
- [ ] T036 [US2] Add logging for selected-text-only operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Full-Book RAG Mode (Priority: P2)

**Goal**: Enable users to ask general questions about the book without selecting specific text, getting comprehensive answers from the entire book.

**Independent Test**: Can be tested by asking general questions about the book and verifying that relevant passages from the entire book are used to generate answers.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US3] Contract test for full-book RAG mode in POST /chat endpoint in tests/contract/test_chat.py
- [ ] T038 [P] [US3] Integration test for full-book RAG flow in tests/integration/test_full_book_rag.py

### Implementation for User Story 3

- [ ] T039 [P] [US3] Enhance RetrievalService to support full-book search in services/retrieval_service.py
- [ ] T040 [US3] Implement top-k chunk retrieval from entire book in services/retrieval_service.py
- [ ] T041 [US3] Add relevance filtering for full-book RAG results in services/retrieval_service.py
- [ ] T042 [US3] Update chat endpoints to handle full-book mode in api/rag/routes/chat.py
- [ ] T043 [US3] Add logging for full-book RAG operations

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Explainable Responses with Citations (Priority: P2)

**Goal**: Provide citations for where the chatbot got its answers from in the book, allowing users to verify information and navigate to source content.

**Independent Test**: Can be tested by asking questions and verifying that responses include proper citations to specific chapters, pages or paragraphs from the book.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T044 [P] [US4] Contract test for citation format in POST /chat response in tests/contract/test_chat.py
- [ ] T045 [P] [US4] Integration test for citation functionality in tests/integration/test_citations.py

### Implementation for User Story 4

- [ ] T046 [P] [US4] Enhance GeneratedResponse model to include citations in models/generated_response.py
- [ ] T047 [US4] Implement citation formatting logic in services/generation_service.py
- [ ] T048 [US4] Update chat endpoints to include citations in response in api/rag/routes/chat.py
- [ ] T049 [US4] Add citation accuracy validation to ensure exact text matches
- [ ] T050 [US4] Implement citation metadata handling in ContentChunk model
- [ ] T051 [US4] Add logging for citation generation operations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T052 [P] Documentation updates for API endpoints and usage in docs/
- [ ] T053 Code cleanup and refactoring across all services and models
- [ ] T054 Performance optimization to ensure responses under 3 seconds
- [ ] T055 [P] Additional unit tests for all services in tests/unit/
- [ ] T056 Security hardening to ensure no credential exposure
- [ ] T057 Run quickstart.md validation to ensure setup works as described
- [ ] T058 [P] Add proper error handling and validation across all endpoints
- [ ] T059 Add comprehensive logging for observability
- [ ] T060 Update README.md with deployment and usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /chat endpoint in tests/contract/test_chat.py"
Task: "Integration test for book-aware QA flow in tests/integration/test_book_qa.py"

# Launch all models for User Story 1 together:
Task: "Create UserQuery model in models/user_query.py"
Task: "Create RetrievedContext model in models/retrieved_context.py"
Task: "Create GeneratedResponse model in models/generated_response.py"
Task: "Create ContentChunk model in models/content_chunk.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence