from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_embedding(text):
    model = get_model()
    return model.encode(text, convert_to_numpy=True)

def get_embeddings_batch(texts):
    model = get_model()
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

def compute_similarity(text1, text2):
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    score = cosine_similarity([emb1], [emb2])[0][0]
    return float(score)

def rank_resumes(resume_texts, jd_text):
    jd_embedding = get_embedding(jd_text)
    resume_embeddings = get_embeddings_batch(resume_texts)
    scores = []
    for res_emb in resume_embeddings:
        score = cosine_similarity([res_emb], [jd_embedding])[0][0]
        scores.append(float(score))
    return scores