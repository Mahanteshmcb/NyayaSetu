"""OpenAI-compatible multilingual adapter (supports OpenRouter)."""
import os
import httpx

LANG_NAMES = {
    'auto': 'the same language as the user message',
    'en': 'English', 'kn': 'Kannada (ಕನ್ನಡ)', 'ta': 'Tamil (தமிழ்)',
    'te': 'Telugu (తెలుగు)', 'ml': 'Malayalam (മലയാളം)', 'hi': 'Hindi (हिन्दी)',
}
LANG_RULES = {
    'kn': 'Write the entire answer in natural Kannada using Kannada script (ಕನ್ನಡ). Do not answer in English except for proper names, unavoidable legal titles, URLs, and quoted source text. Translate all headings and next-step instructions into Kannada.',
    'ta': 'Write the entire answer in natural Tamil using Tamil script (தமிழ்). Do not answer in English except for proper names, unavoidable legal titles, URLs, and quoted source text. Translate all headings and next-step instructions into Tamil.',
    'te': 'Write the entire answer in natural Telugu using Telugu script (తెలుగు). Do not answer in English except for proper names, unavoidable legal titles, URLs, and quoted source text. Translate all headings and next-step instructions into Telugu.',
    'ml': 'Write the entire answer in natural Malayalam using Malayalam script (മലയാളം). Do not answer in English except for proper names, unavoidable legal titles, URLs, and quoted source text. Translate all headings and next-step instructions into Malayalam.',
    'hi': 'Write the entire answer in natural Hindi using Devanagari script (हिन्दी). Do not answer in English except for proper names, unavoidable legal titles, URLs, and quoted source text. Translate all headings and next-step instructions into Hindi.',
    'en': 'Write the entire answer in English.',
}


def _provider_config():
    # Prefer OpenRouter-specific variables when supplied; retain backwards compatibility.
    openrouter_key = os.getenv('OPENROUTER_API_KEY', '').strip()
    api_key = openrouter_key or os.getenv('OPENAI_API_KEY', '').strip()
    if openrouter_key:
        base = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1').strip()
        model = os.getenv('OPENROUTER_MODEL', '').strip() or os.getenv('OPENAI_MODEL', '').strip()
    else:
        base = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1').strip()
        model = os.getenv('OPENAI_MODEL', '').strip()
    if not model:
        model = 'openai/gpt-4o-mini' if 'openrouter.ai' in base else 'gpt-4o-mini'
    return api_key, base.rstrip('/'), model


def ask_model(messages, temperature=0.2):
    api_key, base, model = _provider_config()
    if not api_key:
        return None
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': os.getenv('OPENROUTER_SITE_URL', 'http://localhost:5173'),
        'X-Title': os.getenv('OPENROUTER_APP_NAME', 'NyayaSetu'),
    }
    try:
        r = httpx.post(f'{base}/chat/completions', headers=headers,
                       json={'model': model, 'messages': messages, 'temperature': temperature}, timeout=120)
        r.raise_for_status()
        content = r.json()['choices'][0]['message']['content']
        if isinstance(content, list):
            content = ''.join(str(x.get('text', '')) for x in content if isinstance(x, dict))
        return content.strip() if isinstance(content, str) and content.strip() else None
    except Exception:
        # Do not expose provider keys or raw provider error bodies to users.
        return None


def _language_instruction(language):
    language = (language or 'auto').lower()
    if language in LANG_RULES:
        return LANG_RULES[language]
    return 'Detect the language of the user message and answer in that same language. If the user writes in Kannada, Tamil, Telugu, Malayalam or Hindi, use that language and its native script.'


def analyze_document_text(text, filename, language='auto'):
    instruction = _language_instruction(language)
    prompt = (
        'You are NyayaSetu, a careful Indian legal-information assistant, not a lawyer. '
        'The response language instruction is mandatory: ' + instruction + ' '
        'Do not default to English. If you cannot confidently write in the requested language, say so in that language. '
        'Preserve names, dates, amounts, section numbers and quoted wording accurately. '
        'Return translated headings for: document type; plain-language summary; important names/dates/amounts; '
        'obligations or deadlines explicitly stated; potential issues or missing pages; questions to ask the user; '
        'practical next steps; documents to keep. Distinguish explicit text from inference. '
        'Do not claim a clause is enforceable or give definitive legal conclusions. Never invent statutes, citations, '
        'deadlines, lawyer details or facts. If text is incomplete or OCR may be wrong, say so.'
    )
    answer = ask_model([
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': f'Filename: {filename}\n\nDocument text (may be incomplete):\n{text[:24000]}'}
    ])
    if answer:
        return {'analysis': answer, 'model_used': True}
    return {'analysis': '', 'model_used': False,
            'provider_error': 'OpenRouter/model provider is not configured or did not return a usable response. Check the backend .env settings and server logs; no AI analysis was generated.'}


def answer_chat(question, language='auto', context=''):
    instruction = _language_instruction(language)
    system = (
        'You are NyayaSetu, a multilingual Indian legal-information assistant. '
        'MANDATORY RESPONSE LANGUAGE: ' + instruction + ' '
        'Keep the entire answer in the selected language, including headings, questions, caveats and next steps. '
        'Do not switch to English just because source documents are in English; explain their meaning in the requested language. '
        'Use plain language, ask concise follow-up questions, distinguish general information from legal advice, '
        'cite only sources provided in the context, and never invent law citations, current legal rules, lawyer contact details or outcomes. '
        'If source text appears corrupted or incomplete, state that clearly and ask for a clearer copy rather than guessing. '
        'For urgent danger, imminent eviction, arrest, violence or a deadline, direct the user to appropriate emergency services/qualified legal aid. '
        'This is not a lawyer-client relationship.'
    )
    return ask_model([
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': f'Context from this saved case/document:\n{context[:16000]}\n\nUser question:\n{question}'}
    ])
