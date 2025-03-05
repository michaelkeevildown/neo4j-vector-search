# llm/chains/insurance_policy_chain.py

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from src.llm.models.insurance_policy_model import InsurancePolicyExtractorModel
from src.utils.env_variables import load_env_variables


class InsurancePolicyChain:
    def __init__(self):
        # Load environment variables
        env_vars = load_env_variables()

        # Initialize the language model
        self.llm = ChatOpenAI(model=env_vars['OPENAI_MODEL'], temperature=env_vars['OPENAI_MODEL_TEMPERATURE'],
                              openai_api_key=env_vars['OPENAI_API_KEY'])

        # Initialize the parser with the extractor class
        self.parser = JsonOutputParser(pydantic_object=InsurancePolicyExtractorModel)

        # Define the prompt template
        self.prompt = PromptTemplate(
            template="""
  ### Your job is to extract key information from the current text which is part of a insurance policy, which has been taken from {title}.
  ### You will create a relevance_score which is a float illustrating the percentage relevance between 0 (low relevance to wider context) and 1 max (high relevance to wider context) for reach extracted entity.
  - You MUST ensure that when multiple entity type are extracted e.g. topics, that the total sum of thier relevancy score does not exceed 1 (100%)
  - Create an id for each entity that is extracted to allow for deduplication
  {text}
  ### Use the the following context to get a better understanding of the current policy document, but do not use this in the response. This is for reference only:
  {wider_context}
  ### Use the following to provide a valid format for the output:
  {format_instructions}
  """,
            input_variables=["text", "wider_context", "title"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()},
        )

        # Automatically create and set the processing chain upon initialization
        self.chain = self.create_chain()

    def create_chain(self):
        # Create the processing chain using instance variables
        chain = self.prompt | self.llm | self.parser
        return chain
