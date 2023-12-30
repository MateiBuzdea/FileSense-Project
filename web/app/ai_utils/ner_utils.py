import spacy


NER_CATEGORIES = {
    "owner": ["author", "owner", "writer", "creator"],
    "title": ["title", "name"],
    "content": ["content", "body", "text", "article", "description", "summary"],
    "date": ["date", "time", "year", "month", "day"]
}

def init_ner():
    nlp = spacy.load('en_core_web_sm')
    return nlp

def extract_keywords(nlp, query):
    parsed_query = nlp(query)
    sql_query = 'SELECT * FROM documents WHERE {}'

    conditions = []
    for token in parsed_query.ents:
        for category, keywords in NER_CATEGORIES.items():
            if token.label_ in keywords:
                conditions.append(f'{category}="{token.text}"')

    sql_query = sql_query.format(" AND ".join(conditions))

    return sql_query