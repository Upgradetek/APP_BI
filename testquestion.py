import spacy
from spacy.matcher import Matcher
from connecteDB import connecte


def question_to_sql(question):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(question)
    docs=list(doc)


    # Define the spaCy matcher
    matcher = Matcher(nlp.vocab)

    # Define patterns for SQL-related keywords
    sql_keyword_patterns = [
        [{"LOWER": {"in": ["select", 'retrieve', 'show', 'find', 'count']}}],
        [{"LOWER": {"in": ["from", "of"]}}],
        [{"LOWER": {"in": ["where", "were"]}}],
        [{"LOWER": "and"}],
        [{"LOWER": "or"}],
        [{"LOWER": "not"}],
        [{"LOWER": {"in": ["group", "order", "by", "egal"]}}],
    ]
    def operation(opp):
        doc={"=": ["egal","equal","identical","alike","similar","same","uniform","equivalent","matching","parallel","indistinguishable"],
            "!=": ["different","distinct","divergent","varied","differing","unalike","disparate","separate","contrasting","unique","various"]
            }
        for key,val in doc.items():
            if opp.lower() in val:
                return key
        return opp


    # Add the patterns to the matcher
    matcher.add("sql_keywords", sql_keyword_patterns)

    # Use the matcher to find SQL-related keywords in the question
    matches = matcher(doc)
    sql_keywords = [doc[start:end].text for _, start, end in matches]

    # Extract entities and keywords from the question
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    keywords = [token.text
                for token in doc if not token.is_stop and token.is_alpha and token.text not in sql_keywords]
    print("entities:", entities)
    print("keywords:", keywords)
    conditions = []
    result_affiche = ""
    name_tabs = ""


    for index, con in enumerate(docs):
        ind = index
        if ind > 0 and ind + 2 < len(docs):
            if docs[ind - 1].text.lower() in sql_keywords[0]:
                # Access 'text' property of the token
                result_affiche += " " + str(con.text)
                print("resaff", result_affiche)
            elif docs[ind - 1].text.lower() in sql_keywords[1]:
                # Access 'text' property of the token
                name_tabs = " " + str(con.text)
                print("tabs", name_tabs)
            elif docs[ind - 1].text.lower() in sql_keywords[2]:
                for ents, label in entities:
                    ent = False
                    if str(docs[ind + 2].text) in ents:
                        ent = f"'{str(docs[ind + 2].text)}'"
                if ent:
                    condition = str(con.text) + " " + \
                        operation(str(docs[ind + 1].text)) + " " + \
                        ent  # Access 'text' property of the token
                else:
                    ent = f"'{str(docs[ind + 2].text)}'"
                    condition = str(con.text) + " " + \
                        operation(str(docs[ind + 1].text)) + " " + \
                        ent
                conditions.append(condition)

        # Extract the SQL query type from the question
    query_type = "SELECT"
    if "how many" in question.lower():
        query_type = "SELECT COUNT"

    # Generate the SQL query
    if query_type == "SELECT COUNT":
        sql_query = f"{query_type}(NCompte) FROM compte"
    else:
        sql_query = f"{query_type} {result_affiche} FROM {name_tabs}"

    # Add WHERE clause only if conditions are present
    if conditions:
        sql_query += f" WHERE {' AND '.join(conditions)};"

    print(sql_query)
    return sql_query


# Example usage:
question = "find NCompte from compte were Devise egal EUR?"
sql_query = question_to_sql(question)
print(sql_query, "########################33")
results = connecte(sql_query)

formatted_results = [value for row in results for value in row]

print(formatted_results)
