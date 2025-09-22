# neo4j_loader/loaders/annual_report_cypher.py

def create_policing_handbook_tx(tx, data):
    query = (
        """
        MERGE (report:Report {title: $title})
        
        // Create parent company node
        MERGE (pc:ParentCompany {name: SPLIT($title, " ")[0]})
        MERGE (pc)-[:HAS_DOCUMENT]->(report)
        
        WITH report, $page AS page
        
        MERGE (report)-[:CONTAINS]->(p:Page {page_number: page.page_number})
        
        WITH p, page.llm_response as llm_response, page
        
        SET p.raw_text = page.text
        SET p.page_embedding = llm_response.page_embedding
        SET p.summary_embedding = llm_response.summary_embedding
        SET p.summary = llm_response.summary
        SET p.source = $title + " - Page " + toString(page.page_number)
        
        WITH p, llm_response
        
        // Subquery for handling topics
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.topics IS NULL THEN [null] ELSE llm_response.topics END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:Topic {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.description = thing.description
                SET node.entity_embedding = thing.entity_embedding
            MERGE (p)-[:HAS_TOPIC {relevance_score: thing.relevance_score}]->(node)
        }
        
        RETURN 'Completed'
        """
    )
    parameters = {
        "title": data["title"], "page": data["data"]}
    tx.run(query, parameters)
    return "Completed"
