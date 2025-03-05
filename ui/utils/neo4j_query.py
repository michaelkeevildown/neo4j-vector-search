from langchain_openai import OpenAIEmbeddings
from neo4j import GraphDatabase

from src.utils.env_variables import load_env_variables

env_vars = load_env_variables()

# Define your connection URI and authentication details
uri = env_vars['NEO4J_URI']
username = env_vars['NEO4J_USER']
password = env_vars['NEO4J_PASSWORD']
database = env_vars['NEO4J_DATABASE']

# Initialize the driver
driver = GraphDatabase.driver(uri, auth=(username, password))


def execute_query(query, params, database_name):
    results_list = []  # Initialize an empty list to store results
    with driver.session(database=database_name) as session:
        result = session.run(query, params)
        for record in result:
            results_list.append(record)
    return results_list


def raw_text(question, titles):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=256,
                                  openai_api_key=env_vars['OPENAI_API_KEY'])

    query_result = embeddings.embed_query(question)

    # Your Cypher query
    vector_search_only = """
    MATCH (p:Page)<-[]-(r:Report)
        WHERE r.title IN $report_title
    WITH
        p,
        vector.similarity.cosine(p.page_embedding, $query_result) AS page_vector_score
    RETURN 
        page_vector_score AS page_score,
        page_vector_score AS score,
        p.summary AS summary,
        p.raw_text AS raw_text,
        p.source AS source,
        p.page_number AS page_number
    ORDER BY score DESC
    LIMIT 10
    """

    vector_page_first_search = """
    MATCH (e:ExtractedEntity)<-[rel]-(p:Page)<-[]-(r:Report)
        WHERE r.title IN $report_title
    WITH
        p,
        vector.similarity.cosine(p.page_embedding, $query_result) AS page_vector_score,
        SUM(rel.relevance_score * vector.similarity.cosine(e.entity_embedding, $query_result)) AS entity_scores_sum
    RETURN 
        page_vector_score AS page_score,
        entity_scores_sum AS entity_score,
        page_vector_score * entity_scores_sum AS score,
        p.summary AS summary,
        p.raw_text AS raw_text,
        p.source AS source,
        p.page_number AS page_number
    ORDER BY score DESC
    LIMIT 10
    """

    vector_entity_first_search = """
MATCH (e:ExtractedEntity)<-[rel]-(p:Page)<-[]-(r:Report)
WHERE r.title IN $report_title
WITH rel, e, p, vector.similarity.cosine(e.entity_embedding, $query_result) AS e_vector_score
ORDER BY e_vector_score DESC
LIMIT 15    

WITH p,
     vector.similarity.cosine(p.page_embedding, $query_result) AS page_vector_score,
     SUM(rel.relevance_score * vector.similarity.cosine(e.entity_embedding, $query_result)) AS entity_scores_sum,
     COUNT(e) AS entity_count  // Count of entities contributing to this page

// Aggregate by page
WITH p.page_number AS page_number, 
     p.summary AS summary,
     p.raw_text AS raw_text,
     p.source AS source,
     SUM(page_vector_score) AS total_page_score,
     SUM(entity_scores_sum) AS total_entity_score,
     SUM(page_vector_score) * SUM(entity_scores_sum) AS score,
     entity_count

ORDER BY score DESC, entity_count DESC
RETURN 
    page_number,
    summary,
    raw_text,
    source,
    total_page_score AS page_score,
    total_entity_score AS entity_score,
    score,
    entity_count
LIMIT 10
    """

    fulltext_search = """
    """

    params = {
        "report_title": titles,
        "query_result": query_result
    }

    # Execute the function
    results_vector_page_first_search = execute_query(vector_page_first_search, params, database)
    results_vector_entity_first_search = execute_query(vector_entity_first_search, params, database)
    results_vector_search_only = execute_query(vector_search_only, params, database)


    # Define a boost factor
    boost_factor = 2

    # Convert each record in results_vector_entity_first_search to a dictionary and apply the boost
    boosted_results_vector_entity_first_search = []
    for record in results_vector_entity_first_search:
        record_dict = dict(record)  # Convert the Record to a dictionary
        record_dict["score"] *= boost_factor  # Apply the boost
        boosted_results_vector_entity_first_search.append(record_dict)

    # Merge the results
    results = [dict(result) for result in results_vector_page_first_search] + boosted_results_vector_entity_first_search

    # Sort the results by score in descending order
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # Create a dictionary to store combined results by page number
    combined_results = {}

    # Iterate over the results and sum the scores for duplicates by page number
    for result in results:
        result_dict = dict(result)  # Convert Record to dictionary
        page_number = result_dict['page_number']
        if page_number in combined_results:
            combined_results[page_number]['score'] += result_dict['score']
            # Optionally, concatenate or update other fields if needed
            combined_results[page_number]['raw_text'] += ' ' + result_dict['raw_text']
        else:
            combined_results[page_number] = result_dict

    # Convert the dictionary back to a list
    results = list(combined_results.values())

    # Take top 5 results
    results = results[:5]

    print(">>> ")
    print("\n\n>> Question: " + question)
    print(">>> ")
    print("------ Vector Page First Query ------")
    for result in results_vector_page_first_search:
        print("Page: " + str(result["page_number"]) + " - Vector Score: " + str(result["page_score"]) + " - Entity Score: " + str(result["entity_score"]) +  " - DRVB Sore: " + str(result["score"]))
    
    print("\n------ Vector Entity First Query ------")
    for result in results_vector_entity_first_search:
        print("Page: " + str(result["page_number"]) + " - Vector Score: " + str(result["page_score"]) + " - Entity Score: " + str(result["entity_score"]) +  " - DRVB Sore: " + str(result["score"]))

    print("\n------ Vector Search Only Query ------")
    for result in results_vector_search_only:
        print("Page: " + str(result["page_number"]) + " - Vector Score: " + str(result["score"]))

    print("\n------ Final Results ------")
    for result in results:
        print("Page: " + str(result["page_number"]) + " - Vector Score: " + str(result["page_score"]) + " - Final Score: " + str(result["score"]))

    raw_content = ""
    for record in results:
        raw_content += record['raw_text'] + "  "

    # Close the driver connection when done
    driver.close()

    return raw_content, results
