from pydantic import BaseModel, Field


class AnnualReportExtractorModel(BaseModel):
    summary: str = Field(
        description="Provide a one-sentence summary of the current text.")
    companies: list = Field(
        description="Provide a list of all companies referenced. Score each Company by its relevance in current text: [{'id': 'neo4j', 'company_name': 'Neo4j','relevance_score': 0.856}, {'company_name': 'Azure','relevance_score': 0.144}]")
    people: list = Field(
        description="Any people mentioned and their relationship with the company. Score each person by their relevance in current text: [{'id': 'michael-down', 'name': 'Michael Down', relationship': 'Investor','relevance_score': 0.69}, {'name': 'Arie Chapman', 'relationship': 'Directror','relevance_score': 0.31}]")
    topics: list = Field(
        description="Provide a list of topics that are discussed. Score each topic by its relevance in current text. Score each topic by its relevance in current text: [{'id': 'aura-db', 'description': 'AuraDB','relevance_score': 0.55}, {'id': 'vector-search', 'description': 'Vector Search','relevance_score': 0.45}]")
    business_trends: list = Field(
        description="Any known business trend terms. Score each trend by its relevance in current text: [{'id': 'interest-rates', 'description': 'Interest Rates','relevance_score': 0.91}, {'id': 'recession', 'description': 'Recession','relevance_score': 0.09}]")
    technology_trends: list = Field(
        description="Any known technology trends terms. Score each technology trend by its relevance in current text: [{'id': 'llm', 'description': 'LLM','relevance_score': 0.5}, {'id': 'rag', 'description': 'RAG','relevance_score': 0.5}]")
    risks: list = Field(
        description="Any known risk factor which might present a risk to the organisation. Score each risk by its relevance in current text: [{'id': 'cyber-attack', 'description': 'Cyber Attacks','relevance_score': 0.31}, {'id': 'rapid-innovation', 'description': 'Rapid Innovation','relevance_score': 0.69}]")
    ma: list = Field(
        description="Any known mergers or acquisitions completed or planned. Score each M&A activity by its relevance in current text: [{'id': 'twitter-aquisition', 'description': 'Twitter Acquisition','relevance_score': 1}]")
    external_factors: list = Field(
        description="Any known external factors which might influence or impact the organisation. Score each external factor by its relevance in current text: [{'id': 'global-economy', 'description': 'Global Economy','relevance_score': 0.8}, {'id': 'uk-economy', 'description': 'UK Economy','relevance_score': 0.2}]")
    legal_actions: list = Field(
        description="Any known legal issues which might impact the organisation. Score each legal issue by its relevance in current text: [{'id': 'elastic-aws-legals', 'description': 'Elastic is suing AWS','relevance_score': 1}]")
