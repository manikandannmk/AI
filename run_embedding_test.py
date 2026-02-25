#!/usr/bin/env python3
"""
Generate a 2-page PDF with >200 sentences, upload it, wait for embedding processing,
then query the search endpoint with a question formed from one sentence and validate
that the returned chunks include that sentence.
"""
import time
from pathlib import Path
import requests

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

API_URL = "http://localhost:5000"
UPLOAD_ENDPOINT = f"{API_URL}/api/upload"
STATS_ENDPOINT = f"{API_URL}/api/embeddings/stats"
DOCUMENTS_ENDPOINT = f"{API_URL}/api/documents"
SEARCH_ENDPOINT = f"{API_URL}/api/search"

PDF_PATH = Path('uploads/large_test_200_sentences.pdf')
PDF_PATH.parent.mkdir(exist_ok=True)


def create_large_pdf(path: Path, total_sentences: int = 220):
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 11)

    sentences = []
    for i in range(1, total_sentences + 1):
        # make sentences varied and include keywords for testing
        sentences.append(f"Sentence {i}: This is a test sentence number {i} about machine learning and embeddings.")

    # split into two pages roughly evenly
    per_page = total_sentences // 2
    for page_idx in range(2):
        y = height - 50
        start = page_idx * per_page
        end = start + per_page if page_idx < 1 else total_sentences
        for s in sentences[start:end]:
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 50
            c.drawString(40, y, s)
            y -= 14
        c.showPage()

    c.save()
    return sentences


def upload_pdf(path: Path):
    with open(path, 'rb') as f:
        files = {'files': (path.name, f, 'application/pdf')}
        r = requests.post(UPLOAD_ENDPOINT, files=files)
        return r


def wait_for_processing(timeout=120, poll_interval=3):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(STATS_ENDPOINT, timeout=5)
            if r.status_code == 200:
                stats = r.json().get('statistics', {})
                if stats.get('total_embeddings', 0) > 0 and stats.get('completed_documents', 0) > 0:
                    return True, stats
        except Exception:
            pass
        time.sleep(poll_interval)
    return False, None


def pick_sentence_and_question(sentences):
    # pick sentence 50 as example
    idx = min(50, len(sentences)-1)
    sentence = sentences[idx]
    question = f"What does the document say in sentence {idx+1} about machine learning?"
    return sentence, question


def search_question(question, top_k=5, threshold=0.1):
    payload = {'query': question, 'top_k': top_k, 'threshold': threshold}
    r = requests.post(SEARCH_ENDPOINT, json=payload, timeout=30)
    return r


if __name__ == '__main__':
    print('\n[1] Creating 2-page PDF with >200 sentences...')
    sentences = create_large_pdf(PDF_PATH, total_sentences=220)
    print(f'   Created {PDF_PATH} with {len(sentences)} sentences')

    print('\n[2] Uploading PDF to server...')
    resp = upload_pdf(PDF_PATH)
    print(f'   Upload status: {resp.status_code}, response: {resp.text[:200]}')

    print('\n[3] Waiting for background embedding processing...')
    ok, stats = wait_for_processing(timeout=240, poll_interval=4)
    if not ok:
        print('   Timeout waiting for processing. Stats:', stats)
        raise SystemExit(1)
    print('   Processing complete. Stats:', stats)

    print('\n[4] Selecting a sentence and forming a question...')
    sentence, question = pick_sentence_and_question(sentences)
    print('   Selected sentence:', sentence)
    print('   Question to ask:', question)

    print('\n[5] Sending question to /api/search')
    sr = search_question(question, top_k=5, threshold=0.01)
    print('   Search status:', sr.status_code)
    print('   Search response (truncated):', sr.text[:800])

    results = sr.json().get('results', []) if sr.status_code == 200 else []
    found = False
    for r in results:
        txt = r.get('chunk_text','')
        if sentence.split(':',1)[1].strip() in txt:
            found = True
            print('\n   ✅ Found matching chunk in search results:')
            print('      chunk_id:', r.get('chunk_id'))
            print('      similarity_score:', r.get('similarity_score'))
            print('      chunk_text (truncated):', txt[:200])
            break

    if not found:
        print('\n   ❌ Did not find an exact match; showing top result:')
        if results:
            r = results[0]
            print('      chunk_id:', r.get('chunk_id'))
            print('      similarity_score:', r.get('similarity_score'))
            print('      chunk_text (truncated):', r.get('chunk_text','')[:200])
        else:
            print('      No results returned')

    print('\n[6] Done')
