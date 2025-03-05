# llm/models/insurance_policy_model.py

from pydantic import BaseModel, Field


class InsurancePolicyExtractorModel(BaseModel):
    summary: str = Field(
        description="Provide a one-sentence summary of the current text.")
    topics: list = Field(
        description="Provide a list of topics that are discussed. Score each topic by its relevance in current text: [{'id': 'single-car-policy', 'description': 'Single Car Policy','relevance_score': 0.85}, {'id': 'multicover-car-policy', 'description': 'MultiCover Policy','relevance_score': 0.15}]")
    exclusions: list = Field(
        description="Provide a list of insruance exclusions that are discussed. Score each insruance exclusion by its relevance in current text: [{'id': 'aggressive-authroised-contractors-prevent-access-home', 'description': 'A repair if you are aggressive towards our authorised contractors or staff or impede or prevent access to your home at reasonable times to complete the repair','relevance_score': 0.45}, {'id': 'loss-did-not-contact-arrange-replair', 'description': 'Any loss where you did not contact us to arrange repairs','relevance_score': 0.55}]")
    notifiableActions: list = Field(
        description="Provide a list of notifable actions that are discussed. Score each notifiable action by its relevance in current text: [{'id': 'contact-after-incident', 'description': 'Contact us straight after an incident','relevance_score': 0.75}, {'id': 'contact-change-address', 'description': 'Contact us if your address changes','relevance_score': 0.25}]")
    phoneNumbers: list = Field(
        description="Provide a list of phone numbers that are discussed. If number does not exist do not include the description in output e.g. [{'id': 'uk-car-insurance-helpline', 'description': 'UK Car Insurance Helpline', 'number': '+44123456789'}]")
    definitions: list = Field(
        description="Provide a list of definintion that are discussed. Score each definintion by its relevance in current text: [{'id': 'storm-definition', 'term': 'Storm - A period of violent weather', 'description': 'Wind speeds with gusts of at least 48 knots (55mph) which are the equivalent to Storm Force 10 on the Beaufort Scale.','relevance_score': 1}")