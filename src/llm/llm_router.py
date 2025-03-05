# llm/llm_router.py

import time  # Import the time module

from langchain_openai import OpenAIEmbeddings

from src.llm.chains.annual_report_chain import AnnualReportChain
from src.llm.chains.insurance_policy_chain import InsurancePolicyChain
from src.llm.chains.policing_handbook_chain import PolicingHandbookChain
from src.neo4j_loader.neo4j_loader_base import Neo4jBaseLoader

neo4j_loader = Neo4jBaseLoader()

# Initialize the OpenAIChain class
annual_report_chain_instance = AnnualReportChain()
insurance_policy_chain_instance = InsurancePolicyChain()
policing_handbook_chain_instance = PolicingHandbookChain()
# Initialize the embeddings and language model with specific configurations
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=256)


def embed_and_update_context(llm_response, page_text, last_three_pages):
    for key, value in list(llm_response.items()):
        if isinstance(value, list) and all(isinstance(item, dict) for item in value):
            for item in value:
                for item_key, item_value in list(item.items()):
                    if item_key in ['description', 'company_name', 'name']:
                        embedding = embeddings.embed_documents([item_value])
                        item['entity_embedding'] = embedding[0]

    # Embed summaries and pages
    summary_embedding = embeddings.embed_documents([llm_response['summary']])
    page_embedding = embeddings.embed_documents([page_text])
    llm_response.update({
        'summary_embedding': summary_embedding[0],
        'page_embedding': page_embedding[0]
    })

    # Update the context for the next page
    last_three_pages.append(page_text)
    if len(last_three_pages) > 3:
        last_three_pages.pop(0)

    return llm_response, last_three_pages


def llm_router(content, context, title):
    last_three_pages = []  # Store the last 3 pages for context

    # Get last page from neo4j db
    last_processed_page = neo4j_loader.get_last_page(
        title=title
    )

    print("- Last page processed: " + str(last_processed_page))

    print("- Starting LLM Extraction")

    if context == 'Annual Report':
        for idx, page in enumerate(content['pages']):

            if idx > 30:
                break

            if page['page_number'] > last_processed_page:
                start_time = time.time()  # Record the start time before processing the page

                print("--- Extracting Page: " + str(idx + 1) + "/" + str(
                    len(content['pages'])) + " -- Actual Document Page: " + str(page["page_number"]))

                # Process the text with the defined chain from the AnnualReportChain instance
                llm_response = annual_report_chain_instance.chain.invoke({
                    "title": title,
                    "wider_context": ''.join(last_three_pages),
                    "text": page['text']
                })

                llm_response, last_three_pages = embed_and_update_context(llm_response, page['text'], last_three_pages)
                page['llm_response'] = llm_response

                end_time = time.time()  # Record the end time after processing
                time_taken = end_time - start_time  # Calculate the duration

                neo4j_loader.insert_data(
                    title=title,
                    data=page,
                    context=context
                )

                print(f"--- Extracted Page: {idx + 1}/{len(content['pages'])} - {time_taken:.2f} seconds")

    elif context == 'Insurance Document':
        for idx, page in enumerate(content['pages']):

            # if idx > 10:
            #     break

            if page['page_number'] > last_processed_page:
                start_time = time.time()  # Record the start time before processing the page
                print("--- Extracting Page: " + str(idx + 1) + "/" + str(
                    len(content['pages'])) + " -- Actual Document Page: " + str(page["page_number"]))

                llm_response = insurance_policy_chain_instance.chain.invoke({
                    "title": title,
                    "wider_context": ''.join(last_three_pages),
                    "text": page['text']
                })

                llm_response, last_three_pages = embed_and_update_context(llm_response, page['text'], last_three_pages)
                page['llm_response'] = llm_response

                end_time = time.time()  # Record the end time after processing
                time_taken = end_time - start_time  # Calculate the duration

                neo4j_loader.insert_data(
                    title=title,
                    data=page,
                    context=context
                )

                print(f"--- Extracted Page: {idx + 1}/{len(content['pages'])} - {time_taken:.2f} seconds")
    
    elif context == 'Policing Handbook':
        for idx, page in enumerate(content['pages']):

            if idx > 150:
                break

            if page['page_number'] > last_processed_page:
                start_time = time.time()  # Record the start time before processing the page
                print("--- Extracting Page: " + str(idx + 1) + "/" + str(
                    len(content['pages'])) + " -- Actual Document Page: " + str(page["page_number"]))
                
                llm_response = policing_handbook_chain_instance.chain.invoke({
                    "title": title,
                    "wider_context": ''.join(last_three_pages),
                    "text": page['text']
                })

                llm_response, last_three_pages = embed_and_update_context(llm_response, page['text'], last_three_pages)
                page['llm_response'] = llm_response

                end_time = time.time()  # Record the end time after processing
                time_taken = end_time - start_time  # Calculate the duration

                neo4j_loader.insert_data(
                    title=title,
                    data=page,
                    context=context
                )

                print(f"--- Extracted Page: {idx + 1}/{len(content['pages'])} - {time_taken:.2f} seconds")  

    neo4j_loader.close()
    return content
