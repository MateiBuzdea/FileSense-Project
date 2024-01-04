from txtai.embeddings import Embeddings

from app.core.models import Document
from app.config import basedir


EMBEDDINGS_PATH = basedir + "/ai_data/embeddings"

def init_txtai():
    embeddings = Embeddings({
        "method": "transformers",
        "path": "sentence-transformers/bert-base-nli-mean-tokens"
        })
    try:
        embeddings.load(EMBEDDINGS_PATH)
    except:
        pass

    return embeddings

def add_document(embeddings, document: Document):
    embeddings.upsert([(document.id, document.content)])
    embeddings.save(EMBEDDINGS_PATH)

def search_documents(embeddings, query, n=5):
    print("Searching for:", query)
    print("Top", n, "results:", embeddings.search(query, 10))
    return embeddings.search(query, n)

def delete_document(embeddings, document: Document):
    embeddings.delete([document.id])
    embeddings.save(EMBEDDINGS_PATH)