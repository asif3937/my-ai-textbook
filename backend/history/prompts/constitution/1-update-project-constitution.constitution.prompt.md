---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-15
surface: agent
model: GPT-4
feature: none
branch: main
user: AA
command: /sp.constitution
labels: ["constitution", "governance", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution /sp.constitution
Project Name

Integrated RAG Chatbot for Book-Centric Question Answering

Purpose

Design and build an AI-native, book-embedded Retrieval-Augmented Generation (RAG) chatbot that allows readers to ask questions about the book's content and receive accurate answers strictly grounded in the book text.

The system must support:

Full-book question answering

Selected-text → Ask AI interactions

Clean UI embedding inside the published book

Free-tier infrastructure

Production-ready architecture

The chatbot must be implemented using:

Cohere API (LLM + embeddings)

Qwen CLI for local orchestration and tooling

FastAPI backend

Qdrant Cloud (Free Tier) vector database

Scope
Core Components

Book Content Layer

Structured chapters (Markdown / MDX / HTML)

Chunked text optimized for RAG

Metadata per chunk:

chapter

section

page / heading

source ID

Embedding & Retrieval Layer

Cohere embeddings (lightweight, free-tier safe)

Qdrant Cloud (Free Tier)

Semantic search with metadata filtering

Support for:

whole-book queries

user-selected text as the retrieval scope

Backend API

FastAPI

Endpoints:

/embed

/search

/chat

/chat/selection

Stateless request handling

Strict RAG enforcement

Chatbot UI

Embedded in the book UI

Floating or sidebar chat

"Ask about selected text" feature

Minimal, distraction-free design

CLI & Dev Tooling

Qwen CLI for:

local testing

prompt validation

RAG behavior verification

Core Principles

Grounded Responses Only

The chatbot must answer only from retrieved book content.

No hallucinations.

No external knowledge.

RAG First

If no relevant text is retrieved, the chatbot must say:

"The answer is not found in the book."

Minimalism

Lightweight embeddings

Small chunk sizes

Simple architecture

No unnecessary services

Free-Tier Friendly

Qdrant Cloud Free Tier

Cohere free or low-cost models

No GPU dependency

Fast & Clean

Low-latency retrieval

Clear, readable answers

Clean UI

RAG Behavior Rules

The chatbot must follow these rules without exception:

Context Restriction

Answers must be generated only from retrieved chunks.

The system prompt must explicitly forbid external knowledge.

Selected Text Mode

When user selects text:

Retrieval must be limited to that text or its derived chunks

The answer must reference only the selected content

No Fabrication

If context is insufficient:

Respond with a refusal message

Do not guess or infer

Citation Awareness

Internally track source chunks

Optionally show chapter/section references in responses

Prompting Constitution (LLM Behavior)

The system prompt for the chatbot must enforce:

You are a book-bound assistant

You do not know anything outside this book

You answer only using provided context

You must clearly say when the answer is not present

You must be concise, clear, and factual

Example refusal:

"This information is not present in the provided book content."

Technical Constraints

❌ No OpenAI API

❌ No heavy GPU usage

❌ No large embedding models

❌ No external web search

❌ No hallucinated explanations

✅ Cohere API only

✅ Qdrant Cloud Free Tier

✅ FastAPI

✅ Qwen CLI

✅ Static or lightweight frontend

Success Criteria

The project is considered successful when:

The chatbot answers accurately using only book content

Selected-text queries work correctly

No hallucinations occur

UI is clean and embedded in the book

Runs entirely on free-tier infrastructure

FastAPI backend is stable

Qdrant retrieval is correct and efficient

The system is reproducible and maintainable

Non-Goals

General-purpose AI assistant

Web-wide knowledge answering

Creative writing outside book scope

Heavy personalization or analytics

Paid infrastructure dependency

Final Statement

This project prioritizes accuracy, minimalism, and trust.
The chatbot is not a general AI—it is a precise, book-bound intelligence layer designed to enhance learning without compromising correctness or cost.

## Response snapshot

The project constitution for the Integrated RAG Chatbot for Book-Centric Question Answering has been successfully created and saved to `.specify/memory/constitution.md`. The constitution document now contains all the provided principles and guidelines, with a version number of 1.0.0 and the amendment date set to today (2025-12-15).

The constitution includes:
- Core principles (Grounded Responses Only, RAG First, Minimalism, Free-Tier Friendly, Fast & Clean, Selected Text Mode)
- Core Components sections (Book Content Layer, Embedding & Retrieval Layer, Backend API, Chatbot UI, CLI & Dev Tooling)
- RAG Behavior Rules
- Prompting Constitution (LLM Behavior)
- Technical Constraints
- Success Criteria
- Non-Goals
- Governance statement

A sync impact report was included at the top of the file indicating this is the initial constitution (version 1.0.0), with all principles added and several new sections incorporated. The templates were checked for consistency but didn't require updates.

No files require manual follow-up as all necessary changes have been implemented.

## Outcome

- ✅ Impact: Created project constitution with all specified principles and requirements
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: NA
- 🧠 Reflection: NA

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A