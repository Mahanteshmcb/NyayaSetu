from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
from backend.models.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.agent import analyze_case
from backend.services.validation import InputValidationError
from backend.services import document_tools
router=APIRouter()
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data'/'generated'; UPLOADS=ROOT/'data'/'uploads'; OUT.mkdir(parents=True,exist_ok=True); UPLOADS.mkdir(parents=True,exist_ok=True)
@router.get('/')
def root():return {'name':'NyayaSetu API','docs':'/docs','disclaimer':'Legal information only; not legal advice.'}
@router.get('/health')
def health():return {'status':'ok','service':'nyayasetu-api'}
@router.post('/analyze')
def analyze(payload:AnalyzeRequest):
    try:
        result=analyze_case(payload.description,payload.state,payload.language or 'auto')
        category=result.get('category','unknown')
        q={
        'rent_or_deposit':['When did the tenancy end and where is the property located?','Was there a written rental agreement and what does it say about the deposit?','Has the landlord explained any deductions?','Have you sent a written request or received a notice?'],
        'rent_deposit':['When did the tenancy end and where is the property located?','Was there a written rental agreement and what does it say about the deposit?','Has the landlord explained any deductions?','Have you sent a written request or received a notice?'],
        'unpaid_wages':['What period and approximate amount remain unpaid?','Do you have an appointment letter, payslip or attendance record?','Have you asked the employer in writing?'],
        'termination':['What date and reason were given for termination?','Do you have a written termination letter or employment contract?','Which state and industry did you work in?'],
        'workplace_harassment':['Is there an immediate safety concern or deadline?','When did the incident(s) occur, and is there a safe way to preserve evidence?','Have you contacted an Internal Committee, Local Committee or other authority?']}.get(category,['What happened, and what outcome do you want?','Which state or Union Territory is involved?','Have you received a notice, order, contract or other document?'])
        result['clarification_questions']=q if result.get('needs_clarification') or not result.get('sources') else []
        result['request_upload']=bool(result.get('needs_clarification') or not result.get('sources'))
        result['upload_request']='If available, upload a relevant notice, agreement, order, payslip, invoice, email or message. Redact unnecessary identifiers.' if result['request_upload'] else ''
        result['next_steps']=['Write a dated timeline and preserve original records.','Confirm the relevant state, authority and current version of the law.','Review each cited source and check whether it has been amended or superseded.','If appropriate, submit a factual written representation through a traceable channel and retain proof.','For deadlines, court matters, eviction, safety risks or significant financial consequences, contact a qualified advocate or the relevant authority promptly.']
        result['document_checklist']=['Timeline of events','Relevant agreement, notice, order or contract','Payment/salary/transaction records where relevant','Messages, emails and written requests','Replies and proof of delivery','Deadline or hearing date, if any']
        result['disclaimer']='Legal information only, not legal advice. Verify current official sources and seek qualified help for deadlines or urgent matters.'
        return result
    except InputValidationError as exc:raise HTTPException(status_code=422,detail=str(exc)) from exc
    except Exception as exc:
        import logging;logging.getLogger(__name__).exception('Analysis failed')
        raise HTTPException(status_code=503,detail='Analysis service unavailable. Check server logs and configuration.') from exc

@router.post('/clarify')
async def clarify(case_id:str=Form('local-case'), answers_json:str=Form('{}'), files:list[UploadFile]=File(default=[])):
    import json
    try: answers=json.loads(answers_json)
    except Exception: raise HTTPException(400,'answers_json must be valid JSON')
    stored=[]
    for file in files:
        if not file.filename: continue
        ext=Path(file.filename).suffix.lower()
        if ext not in {'.pdf','.docx','.txt','.md'}: raise HTTPException(400,'Supported formats: PDF, DOCX, TXT, MD')
        data=await file.read()
        if len(data)>20*1024*1024: raise HTTPException(413,'Maximum upload size is 20 MB')
        dest=UPLOADS/(uuid.uuid4().hex+'_'+Path(file.filename).name);dest.write_bytes(data)
        try:
            result=document_tools.ingest(dest,file.filename,'','User evidence - not legal authority','not_applicable','evidence')
            stored.append({'filename':file.filename,**result})
        except Exception as exc: stored.append({'filename':file.filename,'stored':True,'indexing_note':str(exc)})
    return {'case_id':case_id,'answers_received':answers,'uploads':stored,'message':'Evidence saved locally as pending review. Add key facts to the case description and re-run analysis.'}

@router.get('/api/knowledge/sources')
def sources():return {'sources':document_tools.list_sources()}
@router.post('/api/knowledge/upload')
async def upload_knowledge(file:UploadFile=File(...),title:str=Form(''),source_url:str=Form(''),jurisdiction:str=Form('India'),effective_date:str=Form(''),category:str=Form('general')):
    if not file.filename:raise HTTPException(400,'Filename required')
    ext=Path(file.filename).suffix.lower()
    if ext not in {'.pdf','.docx','.txt','.md'}:raise HTTPException(400,'Supported formats: PDF, DOCX, TXT, MD')
    data=await file.read()
    if len(data)>20*1024*1024:raise HTTPException(413,'Maximum upload size is 20 MB')
    dest=UPLOADS/(uuid.uuid4().hex+'_'+Path(file.filename).name);dest.write_bytes(data)
    try:return {'ok':True,**document_tools.ingest(dest,title or file.filename,source_url,jurisdiction,effective_date,category)}
    except Exception as exc:raise HTTPException(400,str(exc)) from exc
@router.post('/api/knowledge/promote/{source_id}')
def promote(source_id:str):
    if not document_tools.promote(source_id):raise HTTPException(404,'Pending source not found')
    return {'ok':True,'source_id':source_id,'status':'approved','note':'Approved by local operator. Confirm official provenance and currency before using.'}
@router.get('/api/templates')
def templates():return {'templates':[{'id':'representation','title':'General representation / complaint','description':'Editable starter to explain facts and request action.'},{'id':'notice_reply','title':'Reply to a notice','description':'Editable response structure; seek legal review before sending.'},{'id':'evidence_checklist','title':'Evidence checklist','description':'Checklist to prepare before contacting an authority or advocate.'}]}
@router.get('/api/templates/{template_id}')
def download_template(template_id:str):
    try:p=document_tools.make_template(template_id,OUT)
    except KeyError:raise HTTPException(404,'Template not found')
    return FileResponse(p,filename=p.name)

# Multilingual document analysis and conversational follow-up endpoints.
@router.post('/api/documents/analyze')
async def analyze_uploaded_document(file: UploadFile=File(...), language: str=Form('auto'), question: str=Form('')):
    from backend.services.multilingual import analyze_document_text, answer_chat
    if not file.filename: raise HTTPException(400,'Filename required')
    ext=Path(file.filename).suffix.lower()
    if ext not in {'.pdf','.docx','.txt','.md'}: raise HTTPException(400,'Supported formats: PDF, DOCX, TXT, MD')
    data=await file.read()
    if len(data)>20*1024*1024: raise HTTPException(413,'Maximum upload size is 20 MB')
    dest=UPLOADS/(uuid.uuid4().hex+'_'+Path(file.filename).name); dest.write_bytes(data)
    try:
        ocr_map={'auto':'eng+kan+tam+tel+mal+hin','en':'eng','kn':'kan+eng','ta':'tam+eng','te':'tel+eng','ml':'mal+eng','hi':'hin+eng'}
        text=document_tools.extract_text(dest, ocr_languages=ocr_map.get(language, 'eng+kan+tam+tel+mal+hin'))
        if len(text.strip()) < 20: raise ValueError('Very little readable text was extracted. This may be a scanned or protected file.')
        result=analyze_document_text(text,file.filename,language)
        if not result.get('model_used'):
            raise HTTPException(status_code=503, detail=result.get('provider_error','AI provider unavailable. Check OpenRouter configuration.'))
        result.update({'filename':file.filename,'characters_extracted':len(text),'preview':text[:3500],'language':language,'document_id':dest.name.split('_',1)[0],'note':'Document analysis is based only on extracted text; OCR can misread scans. Verify important details against the original.'})
        if question:
            result['question_answer']=answer_chat(question,language,text[:16000]) or 'A multilingual AI model is not configured. Add your provider settings to .env to enable document Q&A.'
        return result
    except Exception as exc:
        if isinstance(exc, HTTPException): raise exc
        raise HTTPException(422,str(exc)) from exc

@router.post('/api/chat')
def chat(payload: dict):
    from backend.services.multilingual import answer_chat
    question=str(payload.get('message','')).strip()
    if len(question)<1 or len(question)>8000: raise HTTPException(422,'Message must be between 1 and 8000 characters.')
    language=str(payload.get('language','auto'))
    context=str(payload.get('context',''))
    # Re-read full text from this conversation's locally stored uploads for follow-up questions.
    document_ids=payload.get('document_ids', [])
    if isinstance(document_ids, list):
        for document_id in document_ids[:5]:
            if not isinstance(document_id, str) or not document_id.isalnum(): continue
            matches=[p for p in UPLOADS.iterdir() if p.is_file() and p.name.startswith(document_id+'_')]
            if matches:
                try: context += '\n\nFull text of uploaded document '+matches[0].name.split('_',1)[1]+':\n'+document_tools.extract_text(matches[0])[:18000]
                except Exception: pass
    answer=answer_chat(question,language,context)
    if not answer:
        return {'answer':'The multilingual AI provider is not configured or is currently unavailable. No AI answer was generated. Configure OPENROUTER_API_KEY and OPENROUTER_MODEL (or compatible OPENAI_* settings) in the backend .env file, restart the server, and try again.','model_used':False}
    return {'answer':answer,'model_used':True,'disclaimer':'General legal information only, not legal advice. Verify current law and seek qualified help for deadlines or urgent matters.'}

@router.get('/api/documents/{document_id}/download')
def download_uploaded_document(document_id: str):
    # Only serve a stored upload whose generated identifier exactly matches the requested id.
    matches=[p for p in UPLOADS.iterdir() if p.is_file() and p.name.startswith(document_id+'_')]
    if not matches: raise HTTPException(404,'Stored document not found in this local installation.')
    p=matches[0]
    return FileResponse(p,filename=p.name.split('_',1)[1])
