from txtai.embeddings import Embeddings

from app.core.models import Document
from app.config import basedir


EMBEDDINGS_PATH = basedir + "/ai_data/embeddings"

def init_txtai():
    embeddings = Embeddings({"path": "sentence-transformers/paraphrase-MiniLM-L6-v2"})
    try:
        embeddings.load(EMBEDDINGS_PATH)
    except:
        pass

    return embeddings

def add_document(embeddings, document: Document):
    embeddings.upsert([(document.id, document.content, None)])
    embeddings.save(EMBEDDINGS_PATH)

def search_documents(embeddings, query, n=3):
    return embeddings.search(query,n)

def delete_document(embeddings, document: Document):
    embeddings.delete([document.id])
    embeddings.save(EMBEDDINGS_PATH)