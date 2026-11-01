"""Copy only human-approved candidate chunks into the app's approved corpus.

Edit candidates first: set review_status='approved', add official_source_url,
and complete review_note with the reviewer/date/validity check.
"""
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_IN=ROOT/"rag"/"data"/"legal_dataset_candidates.json"
DEFAULT_OUT=ROOT/"rag"/"data"/"legal_documents_approved.json"
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,default=DEFAULT_IN)
    p.add_argument("--output",type=Path,default=DEFAULT_OUT)
    a=p.parse_args()
    if not a.input.exists(): raise SystemExit(f"Candidate file not found: {a.input}. Run scripts/import_hf_legal_dataset.py first.")
    rows=json.loads(a.input.read_text(encoding="utf-8"))
    approved=[]
    for row in rows:
        if row.get("review_status") != "approved": continue
        if not row.get("official_source_url") or not row.get("review_note") or len(row.get("review_note", "").strip()) < 12:
            print(f"Skipping {row.get('chunk_id')}: add official_source_url and reviewer note")
            continue
        approved.append(row)
    if not approved: raise SystemExit("No fully reviewed rows found; nothing written.")
    a.output.write_text(json.dumps(approved,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Wrote {len(approved)} reviewed chunks to {a.output}")
if __name__=="__main__": main()
