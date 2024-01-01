import spacy


NER_CATEGORIES = {
    "title": ["title", "name"],
    "content": ["content", "body", "text", "article", "description", "summary"],
    "date": ["date", "time", "year", "month", "day"]
}

def init_ner():
    nlp = spacy.load('en_core_web_sm')
    return nlp

# beta feature
def ner_query(nlp, query):
    parsed_query = nlp(query)
    sql_query = 'SELECT * FROM documents WHERE owner_id=%s {}'

    conditions = []
    for token in parsed_query.ents:
        for category, keywords in NER_CATEGORIES.items():
            if token.label_ in keywords:
                conditions.append(f'AND {category} LIKE "%{token.text}%"')

    sql_query = sql_query.format(" ".join(conditions))

    return sql_query


def extract_keywords(nlp, query):
    parsed_query = nlp(query)

    keywords = []
    for token in parsed_query:
        if token.pos_ == "NOUN":
            keywords.append(token.text)

    return keywords