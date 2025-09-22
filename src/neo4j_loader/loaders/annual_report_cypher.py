# neo4j_loader/loaders/annual_report_cypher.py

def create_annual_report_tx(tx, data):
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
        
        // Subquery for handling companies
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.companies IS NULL THEN [null] ELSE llm_response.companies END AS company
            WITH p, company WHERE company IS NOT NULL AND company.relevance_score IS NOT NULL and company.name IS NOT NULL
            MERGE (node:Company {name: company.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.name = company.company_name
                SET node.entity_embedding = company.entity_embedding
            MERGE (p)-[:HAS_COMPANY {relevance_score: company.relevance_score}]->(node)
        }
        
        WITH p, llm_response
        
        // Subquery for handling people
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.people IS NULL THEN [null] ELSE llm_response.people END AS person
            WITH p, person WHERE person IS NOT NULL AND person.relevance_score IS NOT NULL
            MERGE (node:Person {id: person.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.name = person.name
                SET node.entity_embedding = person.entity_embedding
            MERGE (p)-[:HAS_PERSON {relationship: person.relationship, relevance_score: person.relevance_score}]->(node)
        }
        
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
        
        WITH p, llm_response
        
        // Subquery for handling business trends
        CALL (p, llm_response)  {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.business_trends IS NULL THEN [null] ELSE llm_response.business_trends END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:BusinessTrend {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.description = thing.description
                SET node.entity_embedding = thing.entity_embedding
            MERGE (p)-[:HAS_BUSINESS_TREND {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response
        
        // Subquery for handling technology trends
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.technology_trends IS NULL THEN [null] ELSE llm_response.technology_trends END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:TechnologyTrend {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.description = thing.description
                SET node.entity_embedding = thing.entity_embedding
            MERGE (p)-[:HAS_TECHNOLOGY_TREND {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response
        
        // Subquery for handling risks
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.risks IS NULL THEN [null] ELSE llm_response.risks END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:Risk {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.description = thing.description
                SET node.entity_embedding = thing.entity_embedding
            MERGE (p)-[:HAS_RISK {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response
        
        // Subquery for handling mergers and acquisitions
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.ma IS NULL THEN [null] ELSE llm_response.ma END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:MergerAndAcquisition {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.description = thing.description
                SET node.entity_embedding = thing.entity_embedding
            MERGE (p)-[:HAS_MERGER_AND_ACQUISITION {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response
        
        // Subquery for handling external factors
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.external_factors IS NULL THEN [null] ELSE llm_response.external_factors END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:ExternalFactors {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.description = thing.description
                SET node.entity_embedding = thing.entity_embedding
            MERGE (p)-[:HAS_EXTERNAL_FACTORS {relevance_score: thing.relevance_score}]->(node)
        }
        
        WITH p, llm_response
        
        // Subquery for handling legal actions
        CALL (p, llm_response) {
            WITH p, llm_response
            UNWIND CASE WHEN llm_response.legal_actions IS NULL THEN [null] ELSE llm_response.legal_actions END AS thing
            WITH p, thing WHERE thing IS NOT NULL AND thing.relevance_score IS NOT NULL
            MERGE (node:Legal {id: thing.id})
            ON CREATE
                SET node:ExtractedEntity
                SET node.description = thing.description
                SET node.entity_embedding = thing.entity_embedding
            MERGE (p)-[:HAS_LEGAL {relevance_score: thing.relevance_score}]->(node)
        }
        
        RETURN 'Completed'
        """
    )
    parameters = {
        "title": data["title"], "page": data["data"]}
    tx.run(query, parameters)
    return "Completed"
