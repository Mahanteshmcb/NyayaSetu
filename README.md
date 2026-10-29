# NyayaSetu — Multilingual legal-information workspace

A local React/Vite + FastAPI application with a ChatGPT-style conversation UI in NyayaSetu's forest-green, cream and antique-gold theme. It supports case intake, reviewed-source RAG ingestion, document upload and text extraction, saved conversations, editable templates, and official legal-aid links.

## Features in this build

- **Chat-style workspace:** sidebar with saved conversations, new chat, message history, language and state selectors. Conversation metadata and summaries are stored in this browser's local storage; uploaded originals are stored locally by the backend.
- **Document analysis:** upload PDF, DOCX, TXT or Markdown, extract text, preview extracted content, request an analysis in the selected language, and access the locally stored original from that conversation. PDF text extraction works for text PDFs. Scanned PDFs require the optional OCR setup below.
- **Multilingual interface/model:** English, Kannada, Tamil, Telugu, Malayalam and Hindi selection. A configured OpenAI-compatible model is asked to answer in the selected language and preserve names, amounts, dates and section numbers. Auto-detect asks the model to respond in the user's language.
- **Legal source RAG:** upload official legal sources, track pending/approved status, and approve only after human review. The RAG corpus is not automatically exhaustive and source URLs are metadata, not a crawler.
- **Legal aid resources:** official NALSA/state legal services links and available contact details. These are legal-aid authority contacts, not endorsements or rankings of private lawyers. Reconfirm details on the linked official page.
- **Templates:** editable general representation, notice reply, and evidence checklist downloads.
- **Safety:** the app distinguishes unavailable model configuration from a real model response and warns users to verify legal claims. It does not guarantee case outcomes.

## Windows setup (Bun frontend)

Install Python 3.11+ and Bun. From this folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn backend.main:app --reload --port 8008
```

Open a second terminal:

```powershell
cd frontend
bun install
bun run dev
```

Open the URL shown by Vite (usually `http://127.0.0.1:5173`). API docs: `http://127.0.0.1:8008/docs`; health: `http://127.0.0.1:8008/health`.

## Enable the multilingual AI model

The UI and upload routes work without a model key, but **semantic multilingual analysis, translation and conversational follow-up require a configured model provider**. This project uses an OpenAI-compatible Chat Completions endpoint. Edit `.env`:

```dotenv
OPENAI_API_KEY=your_provider_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

Use the model/provider you have access to and its current supported endpoint. `OPENAI_BASE_URL` can point to a compatible provider or a local gateway. Never commit `.env` or expose the API key in frontend code. Restart FastAPI after changing it. If the key is absent or the provider fails, the API explicitly reports that model-based analysis was not performed.

## OCR for scanned PDFs

For PDFs with selectable text, extraction uses `pypdf`. Image-only/scanned PDFs need Tesseract OCR, Poppler, Python packages `pytesseract` and `pdf2image`, and Tesseract language data for the languages you want. Install at least `eng`, `kan`, `tam`, `tel`, `mal`, `hin` language packs. Then uncomment/install the optional packages in `requirements.txt`. OCR quality varies; compare dates, names, amounts and quoted clauses against the original PDF. If OCR dependencies are missing, the app reports that it could not read the scanned PDF rather than pretending it analyzed it.

## Knowledge base workflow

1. Obtain an official source from a relevant authority (for example India Code, an official Gazette, a State department or court website).
2. Upload the document and enter its exact title, source URL, jurisdiction and known effective/publication date.
3. Review extracted text and verify that the source is official, current, applicable and not superseded.
4. Approve it for retrieval only after review. Test queries and inspect the retrieved excerpts/citations.

No bundled ZIP can credibly claim to contain every Indian law, regulation, notification and amendment. The app does not automatically download the internet or infer that a source URL is proof of validity.

## Privacy and legal-aid notes

- This is a local development app. Chat history is stored in browser local storage; backend uploads are saved in `data/uploads/`. Do not use a shared computer or upload confidential files unless you understand who can access that machine. Remove files manually from the local upload folder when no longer needed.
- Before public deployment, add authentication, user-scoped access control, encryption, malware scanning, retention/deletion controls, audit logs, quotas, rate limits, backups and security testing. Current local upload/download endpoints are not a production document vault.
- The legal-help page links to official legal services authorities. It does not recommend a specific private lawyer or verify individual advocate availability. For private advocates, independently verify State Bar Council enrolment, relevant experience, fees and engagement terms.
- Generic templates are not official government forms. Confirm the proper forum, prescribed form, filing channel, fee and limitation period.

## Tests

```powershell
pytest -q
```

The test suite checks the existing API/classifier/retriever/agent paths. It does not replace end-to-end browser tests or legal review. Verify the frontend build locally with `bun run build` after `bun install`.


## OpenRouter and multilingual PDF troubleshooting

Set `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`, and `OPENROUTER_MODEL` in the root `.env`. Use a model identifier available in your OpenRouter account. Restart Uvicorn after changing `.env`. The response language selector is passed to the backend and is enforced by the model prompt; the provider/model must support the requested language. If no model answer is returned, document analysis now reports an error instead of presenting English fallback text as if it were an AI analysis.

For PDFs with garbled text, native PDF text extraction may be broken by a missing ToUnicode map. NyayaSetu now detects common corruption and attempts OCR via PyMuPDF/Tesseract. Install Tesseract OCR and its language data (`eng`, `kan`, `tam`, `tel`, `mal`, `hin`). If OCR fails, the app should stop and explain the problem instead of analyzing unreadable text. Verify names, amounts, section numbers and dates against the original PDF.

## Google sign-in and nearby lawyer finder

See [`Docs/FIREBASE_AND_LAWYER_FINDER_SETUP.md`](Docs/FIREBASE_AND_LAWYER_FINDER_SETUP.md) for the Firebase project setup and local run instructions. The frontend includes Google and email/password authentication UI using Firebase Authentication. The nearby advocate finder asks for browser location permission and opens Google Maps searches for relevant practice areas; Maps listings may provide phone numbers, addresses and directions.

**Deployment security note:** the current FastAPI endpoints do not yet validate Firebase ID tokens. Frontend authentication is not backend access control. Add Firebase Admin token verification to protected API routes before deploying with private data. Lawyer listings are third-party Maps data and must be independently verified.


## SAP HANA Cloud (optional)

NyayaSetu can use SAP HANA Cloud for persistent legal-source metadata, chunk storage and vector similarity retrieval. Local development remains available with `USE_HANA=false`. See [`Docs/HANA_CLOUD_SETUP.md`](Docs/HANA_CLOUD_SETUP.md) for setup, schema, secure configuration, ingestion, verification and troubleshooting. Run `python scripts/check_hana_connection.py` after configuring the root `.env`.

HANA PAL classification and a legal knowledge graph are planned extensions, not prerequisites for RAG. Do not use synthetic fixtures as legal authority.
