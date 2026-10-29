# Features and limitations

## Included in this local bundle
- React/Vite web interface and FastAPI backend.
- Existing classifier and embedding-based RAG retrieval.
- PDF, DOCX, TXT and Markdown source/evidence upload (20 MB per file).
- Source metadata: title, URL, jurisdiction, effective date and category.
- Pending-review workflow; operator explicitly promotes reviewed documents into the approved RAG corpus.
- Clarification prompts, next-step checklist and evidence checklist.
- Downloadable DOCX representation and notice-reply starter templates plus TXT evidence checklist.
- API health endpoint and automated tests.

## Not a legal guarantee
- The project does not ship a complete verified copy of all Indian central/state legislation, subordinate legislation, notifications, circulars, forms and case law.
- No automatic full-site crawler or continuous update feed is configured. URL metadata alone does not download or monitor a website.
- OCR is not included for image-only PDFs.
- The classifier is a baseline, not a calibrated legal classifier. Retrieval quality depends on corpus quality and category/jurisdiction metadata.
- Templates are not official government forms. Confirm the authority, forum, form, deadline, fee and portal for each matter.
- Authentication, authorization, malware scanning, encrypted cloud storage, audit logs, retention controls and production hardening are not configured. Use non-sensitive test material until these are added.
