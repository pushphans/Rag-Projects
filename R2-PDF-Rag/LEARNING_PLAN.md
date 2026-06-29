# RAG → Agentic RAG — Learning Plan & Progress Tracker

> **Is file ka maqsad (purpose):** Yeh ek living document hai. Isme poora roadmap hai —
> RAG basics se lekar Agentic RAG tak. Har step ka status maintained hai (DONE / NEXT).
> Agar session band ho jaye, to user yeh file kisi bhi AI model ko de kar **exactly usi
> point se** kaam continue karwa sakta hai jahan chhoda tha.

---

## 📌 HOW TO USE THIS FILE (READ THIS FIRST — for any AI model)

If you are an AI assistant reading this file to continue teaching:

1. **Read the "LEARNER PROFILE"** section — understand who you are teaching and HOW.
2. **Read "CURRENT PROJECT SNAPSHOT"** — this is the exact state of the codebase.
3. **Jump to "👉 RESUME HERE"** — this marker always points to the next thing to do.
4. **Follow the "TEACHING RULES"** strictly. The learner has strong preferences.
5. After completing any step, **update this file**: tick the checkbox, move the
   "👉 RESUME HERE" marker, and add a line to the CHANGELOG at the bottom.

Keep this file as the single source of truth. Update it as you go.

---

## 👤 LEARNER PROFILE

- **Name / role:** Pushp — works as an **AI Engineer + Flutter Developer**.
- **Strong in:** Agentic AI, **LangGraph**, Flutter/Dart, general app development.
- **Weak in / learning now:** **RAG (Retrieval-Augmented Generation)** — total beginner at RAG specifically.
- **Goal:** Learn RAG **from scratch, baby steps → advanced**, in a **production-oriented**
  way. Then move on to **Agentic RAG**. End goal: switch companies into a stronger **AI Engineer** role.
  **⚠️ REFINED GOAL (learner stated explicitly):** He does NOT want to master classic RAG or
  have RAG generate answers. He wants RAG as a **retriever TOOL / data source** that a
  **LangGraph agent** calls to get relevant context; the **agent** (not RAG) produces the
  answer. Build exactly enough RAG to be a perfect context-supplier tool for an agent.
- **Language:** Communicates in **Hinglish** (Hindi + English). Explain concepts in simple,
  friendly, "bro-to-bro" tone. Code and code-comments stay in English.

### 🧑‍🏫 TEACHING RULES (VERY IMPORTANT — follow these)

1. **Simple, readable code over clever one-liners.** The learner explicitly prefers code
   that is easy to understand even if it takes a few extra lines. Avoid dense one-liners
   that are hard to read. Spell things out.
2. **Baby steps.** Introduce ONE concept at a time. Explain the "why" before the "how".
3. **Production mindset.** Always relate to how things are actually done in real-world
   production systems (not just toy examples). Call out when something is "learning-only".
4. **Retrieval pipeline MUST use LangGraph, NOT LangChain chains.** The learner knows
   LangGraph and wants to use it. (Ingestion already uses LangChain loaders/splitters —
   that's fine, those are just utilities.)
5. **Don't dump everything at once.** Teach a step, let it sink in, then move to the next.
6. **Explain trade-offs** when choosing between options (e.g. chunk sizes, search types).
7. **WORKFLOW PREFERENCE:** From Phase 1.3 onward, the learner wants to **write the code
   himself in the files**. So TEACH the code in chat (explain it line-by-line, simply), and
   let him type it into the files. Do NOT edit his files directly unless he asks — guide and
   review instead. (Exception: small earlier edits like 1.2 were fine; this is his new pref.)

---

## 🛠️ TECH STACK & DECISIONS (fixed for this project)

| Component | Choice | Notes |
|-----------|--------|-------|
| API framework | **FastAPI + Uvicorn** | Already set up |
| LLM | **DeepSeek Chat** (`deepseek-chat`) | API key in `.env` as `DEEPSEEK_API_KEY` |
| Embeddings | **`sentence-transformers/all-MiniLM-L6-v2`** | 384-dim, runs on CPU |
| Vector DB | **Qdrant** (cloud-hosted) | URL + API key in `.env` |
| Orchestration (retrieval) | **LangGraph** | ⚠️ NOT LangChain chains — this is a hard rule |
| Ingestion utilities | LangChain loaders + splitters | OK to use (just helpers) |

---

## 📂 CURRENT PROJECT SNAPSHOT (as of last update)

```
R2-PDF-Rag/
├── app/
│   ├── main.py                         # FastAPI app, includes rag_router
│   ├── core/config.py                  # Settings (env vars): DEEPSEEK_API_KEY, QDRANT_URL, QDRANT_API_KEY
│   ├── api/rag_router.py               # Routes. Currently: POST /rag/ingest
│   ├── rag/
│   │   └── ingestion_pipeline/
│   │       ├── ingestion.py            # Loads + chunks the hardcoded sample.pdf
│   │       └── embedder.py             # HuggingFaceEmbeddings (MiniLM, 384-dim)
│   ├── vector_db/
│   │   └── qdrant_vector_db.py         # Qdrant client + LangChain QdrantVectorStore wrapper
│   └── sample_data/sample.pdf          # The single test PDF (hardcoded path)
├── requirements.txt
├── pyproject.toml
└── LEARNING_PLAN.md                    # 👈 this file
```

### What each file does right now (verified):

- **`ingestion.py`** — Loads `app/sample_data/sample.pdf` via `PyPDFLoader`, splits with
  `RecursiveCharacterTextSplitter`. ⚠️ **Issues to fix later:** (a) file path is **hardcoded**
  (no dynamic upload yet), (b) `chunk_size=100, chunk_overlap=10` is **too small** for
  production (should be ~500-1000 / ~100-150).
- **`embedder.py`** — Creates the MiniLM embedder (384-dim, CPU). ✅ Fine.
- **`qdrant_vector_db.py`** — Creates Qdrant client, ensures collection `pdf_collection`
  exists (size=384, distance=COSINE), wraps it in `QdrantVectorStore`. ✅ Fine.
- **`rag_router.py`** — `POST /rag/ingest`: creates collection if missing, skips if already
  has points, else chunks + embeds + stores the sample PDF. ✅ Works for learning.
- **`config.py`** — Pydantic settings, reads `.env`. ✅ Fine.

### ✅ What WORKS today:
Ingestion of one hardcoded PDF → chunks → embeddings → stored in Qdrant. That's it.

### ❌ What does NOT exist yet:
- Dynamic file **upload** endpoint
- Any **retrieval** (search) logic
- Any **LLM answer generation**
- The **LangGraph** retrieval pipeline
- Any **evaluation** or **agentic** behavior

---

## 🗺️ THE FULL CURRICULUM (high-level map)

Think of it as a staircase. We climb ONE step at a time.

```
PHASE 0  Foundations (concepts only, no new code)            [understanding]
PHASE 1  Solid Ingestion (dynamic upload + good chunking)    [fix what exists]
PHASE 2  Basic Retrieval Pipeline with LangGraph             [THE core of RAG]
PHASE 3  Better Retrieval (metadata, hybrid, reranking)      [production quality]
PHASE 4  Evaluation (is our RAG actually good?)              [measure it]
PHASE 5  Agentic RAG with LangGraph                          [the advanced goal]
```

---

## ✅ PROGRESS TRACKER (tick as we go)

### PHASE 0 — Foundations (concepts)
- [x] 0.1 What is RAG and WHY it exists (the "LLM doesn't know your data" problem)
- [x] 0.2 The 2 halves: **Ingestion** (offline) vs **Retrieval** (online/runtime)
- [x] 0.3 What are **embeddings** and **vectors** (intuition, not math)
- [x] 0.4 What a **vector database** does (similarity search) — and what Qdrant is
- [x] 0.5 What **chunking** is and why chunk size matters
- [x] 0.6 The full RAG request lifecycle, end-to-end (one diagram in the head)

### PHASE 1 — Solid Ingestion
- [x] 1.1 Load a PDF, chunk it, embed it, store in Qdrant *(already done by learner)*
- [x] 1.2 Understand & fix chunk size/overlap (why 100 is too small)
- [x] 1.3 Add a **dynamic file upload** endpoint (`POST /rag/upload`) — no more hardcoded path
- [~] 1.4 Add useful **metadata** to chunks (source filename, page number) — page_number DONE;
      `source` + upsert (delete-then-add by filename) TAUGHT but learner DEFERRED to later
      ("production mein dekh lunga"). Resume here if revisiting Phase 1.
- [ ] 1.5 (Optional) Support more file types (DOCX/TXT) — learn loaders

### PHASE 2 — Retriever as a TOOL for a LangGraph agent  ⭐ (learner's actual goal)
> **IMPORTANT — learner's chosen architecture (do NOT build classic RAG):** RAG here is just a
> **data source / context supplier**, NOT an answer-generator. The flow is **AGENTIC RAG**:
> a LangGraph **agent** owns the LLM; when it needs context it calls the **retriever tool**
> (similarity_search) which returns relevant chunks; the **agent itself** writes the answer.
> So we do NOT put an LLM "generate" node inside the RAG pipeline. We make retrieval clean &
> reliable, wrap it as a tool, and build a LangGraph agent that uses that tool.
- [x] 2.1 Concept: what "retrieval" means (query → embed → search → top-k chunks)
- [x] 2.2 Write a simple similarity search against Qdrant (no LLM yet) — see raw chunks
- [ ] 2.3 Make retrieval return CLEAN context (text + minimal metadata: source, page) — agent-ready
- [ ] 2.4 Concept: LangGraph **tool** + agent **State** (what flows through the graph)
- [ ] 2.5 Wrap the retriever as a LangGraph **tool** (the agent can call it)
- [ ] 2.6 Build a LangGraph **agent** with DeepSeek that calls the retriever tool, then answers
- [ ] 2.7 Expose it as `POST /rag/ask` (query → agent → tool(context) → agent answer)

### PHASE 3 — Better Retrieval (production quality, makes the tool stronger)
- [ ] 3.1 Metadata filtering (search within one document/source)
- [ ] 3.2 Tune top-k and understand the precision/recall trade-off
- [ ] 3.3 Hybrid search (dense + keyword/BM25) — concept + Qdrant support
- [ ] 3.4 Re-ranking with a cross-encoder (why it boosts quality)
- [ ] 3.5 Query rewriting / expansion (concept)

### PHASE 4 — Evaluation
- [ ] 4.1 Why eval matters (you can't improve what you don't measure)
- [ ] 4.2 Core metrics: context precision/recall (retrieval quality), answer faithfulness
- [ ] 4.3 Build a tiny eval set + measure the retriever tool

### PHASE 5 — Advanced Agentic RAG with LangGraph
- [ ] 5.1 Query routing (agent decides: retrieve vs answer directly vs other tool)
- [ ] 5.2 Self-correction loop (grade retrieved docs; re-retrieve if bad)
- [ ] 5.3 Multi-step / multi-source agentic retrieval
- [ ] 5.4 (Stretch) Add more tools (web search, calculator) alongside the retriever tool

---

## 👉 RESUME HERE  ←←← (this marker = the next thing to do)

**Current position:** ✅ Phase 2.1 & 2.2 DONE — raw `similarity_search` working via
`retriever.py` (`asimilarity_search` + await) and a temp `/rag/docs` search endpoint. Hit &
debugged real bugs together: collection-not-exist 404, empty-list vs not-exist distinction,
and the async/sync rules (await only on async methods; `a`-prefix = async version). Also
ensured `ensure_collection()` is sync and called in `/upload`. Learner chose to DEFER further
edge-case polish (empty messages) to focus on adding the LLM. **Corrected a key
misconception:** the LLM does NOT do retrieval — similarity_search IS retrieval; the LLM only
does *generation* on top of the retrieved chunks. similarity_search stays; LLM is added above it.

**NEXT STEP → Phase 1.4 first (learner chose to harden INGESTION to production-grade BEFORE
the retriever).** Order agreed (1→2→3→4→5): (1) add `source` filename to chunk metadata;
(2) upsert / delete-then-add by `metadata.source` (fixes the duplicate bug he saw himself);
(3) validation hardening (filename None, case-insensitive `.pdf`, empty/0-byte file);
(4) empty/scanned-PDF detection (0 chunks → don't report success — silent-failure guard);
(5) response polish (`chunks_added`, specific errors, fix "succssfully" typo). Currently doing
#1+#2 together (upsert needs source). AFTER ingestion is production-grade, return to Phase
2.3+ (retriever as a tool: `get_context_and_sources` → LangGraph tool → agent). Teach in chat;
he writes the code. He wants context+sources separated: context→agent, sources→separate state
key for UI only.

> Teaching tip for the next AI: don't info-dump all of Phase 0 at once. Do 0.1–0.2 first,
> check understanding, then continue. The learner values understanding over speed.

---

## 📖 CONCEPT GLOSSARY (grows as we learn — quick-reference for the learner)

- **RAG (Retrieval-Augmented Generation):** Instead of relying only on what the LLM
  memorized, we first *retrieve* relevant pieces of YOUR data and feed them to the LLM as
  context, so it answers from real, up-to-date, private knowledge.
- **Ingestion pipeline:** The *offline* half. Runs when you add documents. Steps:
  load → chunk → embed → store in vector DB.
- **Retrieval pipeline:** The *online* half. Runs at query time. Steps:
  embed the question → search vector DB → pass top chunks + question to LLM → answer.
- **Embedding:** A list of numbers (a vector) that represents the *meaning* of a piece of
  text. Similar meanings → vectors that are close together. (MiniLM gives 384 numbers.)
- **Vector / dimension:** Our vectors have 384 dimensions (because MiniLM outputs 384).
  That's why the Qdrant collection is created with `size=384`.
- **Vector database (Qdrant):** A database optimized to store millions of vectors and find
  the "nearest" ones to a query vector very fast (similarity search).
- **Cosine distance:** The "closeness" measure we use (COSINE in the Qdrant config). Smaller
  distance = more similar meaning.
- **Chunk:** A small slice of a document. We split big docs into chunks so we can retrieve
  just the relevant slice instead of a whole 100-page PDF.
- **chunk_size / chunk_overlap:** How big each slice is, and how much consecutive slices
  overlap (overlap avoids cutting a sentence/idea badly at the boundary).
- **top-k:** How many of the most-similar chunks we pull back from the vector DB per query.
- **LangGraph:** A library to build LLM workflows as a **graph** of nodes with shared
  **state**. We'll model retrieval as: `retrieve` node → `generate` node. (Learner's strength.)

---

## 📝 CHANGELOG (newest first — append one line per working session)

- **2026-06-28 (session 3)** — ✅ Phase 1.3 done (`/upload` working, in-memory BytesIO+pypdf,
  `/ingest` removed). Taught upsert-by-filename (delete-then-add) but learner deferred it.
  Reviewed his code & fixed 3 bugs he hit (page_content=text, await file.read(), correct kwarg
  name). Career discussion: AI-assisted dev is hireable if you understand/own/debug/defend it.
  Now starting Phase 2 (LangGraph retrieval).

- **2026-06-25 (session 2)** — ✅ Completed all of PHASE 0 (foundations). Taught 0.1→0.6
  bro-to-bro with concept checks after each. Learner explained back correctly throughout.
  Key corrections made & logged: "1 chunk = 1 vector", "overlap repeats text at boundaries",
  and "embedding model (not vector DB) is the component that must be identical across
  ingestion & retrieval". Next: start coding at Phase 1.2.

- **2026-06-25** — Created this learning plan. Reviewed existing codebase (ingestion +
  Qdrant working). Answered learner's doubts: (1) hardcoded data is learning-only, prod uses
  dynamic upload; (2) PDF is the most-used data type in production RAG. Set up full
  curriculum Phase 0→5. Next: Phase 0 foundations, then Phase 1.2/1.3.
