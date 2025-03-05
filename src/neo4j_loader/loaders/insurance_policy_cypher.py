# neo4j_loader/loaders/insurance_policy_cypher.py

from neo4j.exceptions import ClientError


def create_insurance_policy_tx(tx, data):
    query = (
        """
        MERGE (report:Report {title: $title})
        
        // Create parent company node
        MERGE (pc:ParentCompany {name: SPLIT($title, " ")[0]})
        MERGE (pc)-[:HAS_DOCUMENT]->(report)
        
        WITH report, $page AS page

        MERGE (report)-[:CONTAINS]->(p:Page {page_number: page.page_number})

        WITH p, page.llm_response as llm_response, page, report

        SET p.raw_text = page.text
        SET p.page_embedding = llm_response.page_embedding
        SET p.summary_embedding = llm_response.summary_embedding
        SET p.summary = llm_response.summary

        WITH p, llm_response

        // Subquery for handling topics
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.topics IS NULL THEN [null] ELSE llm_response.topics END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:Topic {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.entity_embedding = thing.entity_embedding
                SET node.description = thing.description
            MERGE (p)-[:HAS_TOPIC {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response

        // Subquery for handling exclusions
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.exclusions IS NULL THEN [null] ELSE llm_response.exclusions END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:Exclusion {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.entity_embedding = thing.entity_embedding
                SET node.description = thing.description
            MERGE (p)-[:HAS_EXCLUSION {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response

        // Subquery for handling notifiable actions
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.notifiableActions IS NULL THEN [null] ELSE llm_response.notifiableActions END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:NotifiableAction {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.entity_embedding = thing.entity_embedding
                SET node.description = thing.description
            MERGE (p)-[:HAS_NOTIFIABLE_ACTION {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response

        // Subquery for handling phone number
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.phoneNumbers IS NULL THEN [null] ELSE llm_response.phoneNumbers END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:Phone {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.entity_embedding = thing.entity_embedding
                SET node.number = thing.number
            MERGE (p)-[:HAS_NOTIFIABLE_ACTION {relevance_score: thing.relevance_score, description: thing.description}]->(node)
        }
        
        WITH p, llm_response

        // Subquery for handling definitions
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.definitions IS NULL THEN [null] ELSE llm_response.definitions END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:Definition {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.entity_embedding = thing.entity_embedding
                SET node.description = thing.description
                SET node.term = thing.term
            MERGE (p)-[:HAS_DEFINITION {relevance_score: thing.relevance_score}]->(node)
        }
        
        RETURN 'Completed'
        """
    )
    parameters = {
        "title": data["title"], "page": data["data"]}
    try:
        tx.run(query, parameters)
        return "Completed"
    except ClientError as e:
        # Handle the error
        print(f"An error occurred: {e}")
        print(data['data']['llm_response'])
        return "An error occurred"
