# main.py

from src.llm.llm_router import llm_router
from src.neo4j_loader.neo4j_loader_base import Neo4jBaseLoader
from src.parsers.url_parser import url_parser

neo4j_loader = Neo4jBaseLoader()

pdfs = [
    ## AXA Policy Documents
    # AXA Home Insurance
    {
        "url": 'https://www.axa.co.uk/globalassets/pdfs/home/policy-docs/april-2023/axa-direct-home-policy-wording-acpd0400p-b.pdf/',
        "title": 'AXA Home Insurance policy document',
        "context": "Insurance Document"
    },
    {
        "url": 'https://www.axa.co.uk/globalassets/pdfs/home/policy-docs/april-2023/axa-direct-home-plus-policy-wording-acpd0401p-b.pdf/',
        "title": 'AXA Plus Home Insurance policy document',
        "context": "Insurance Document"
    },
    {
        "url": 'https://www.axa.co.uk/globalassets/pdfs/home/policy-docs/april-2023/axa-direct-home-premier-policy-wording-acpd0402p-b.pdf/',
        "title": 'AXA Premier Home Insurance policy document',
        "context": "Insurance Document"
    },
    # AXA Car Insurance
    {
        "url": 'https://www.axa.co.uk/globalassets/pdfs/motor/april-2023/axa-direct-car-policy-wording-acpd0392p-c.pdf/',
        "title": 'AXA Car Insurance policy document',
        "context": "Insurance Document"
    },
    {
        "url": 'https://www.axa.co.uk/globalassets/pdfs/motor/april-2023/axa-direct-car-plus-policy-wording-acpd0393p-c.pdf/',
        "title": 'AXA Plus Car Insurance policy document',
        "context": "Insurance Document"
    },
    # AXA Van Insurance
    {
        "url": 'https://www.axa.co.uk/globalassets/pdfs/van/policy-docs/june-2023-update/axa-van-summary-of-cover-june-23--acld0486z-k.pdf/',
        "title": 'AXA Van Insurance Summary of cover',
        "context": "Insurance Document"
    },
    {
        "url": 'https://www.axa.co.uk/globalassets/pdfs/van/policy-docs/june-2023-update/axa-van-insurance-policy-wording-june-23--acld0486p-m.pdf/',
        "title": 'AXA Van Insurance policy document',
        "context": "Insurance Document"
    },

    ## Admiral Policy Documents
    # Admiral Car Insurance
    {
        "url": 'https://eui-pdf-assets.s3.eu-west-1.amazonaws.com/admiral/AD-003-037-Your-Car-Insurance-Guide.pdf',
        "title": 'Admiral Car Insurance Guide',
        "context": "Insurance Document"
    },
    {
        "url": 'https://eui-pdf-assets.s3.eu-west-1.amazonaws.com/admiral/IP-MO-2-005.pdf',
        "title": 'Admiral Insurance Product Information Document (Essential, Admiral, Gold & Platinum)',
        "context": "Insurance Document"
    },
    {
        "url": 'https://eui-pdf-assets.s3.eu-west-1.amazonaws.com/admiral/AD046-001-Claims-Flyer.pdf',
        "title": 'Admiral Claim Information Flyer',
        "context": "Insurance Document"
    },
    {
        "url": 'https://eui-pdf-assets.s3.eu-west-1.amazonaws.com/admiral/AD-004-025-Renewal-Brochure.pdf',
        "title": 'Admiral Renewals document',
        "context": "Insurance Document"
    },

    # 10-K's
    {
        "url": 'https://www.ubs.com/global/en/investor-relations/financial-information/sec-filings/_jcr_content/mainpar/toplevelgrid/col1/tabteaser/tabteasersplit_2037369950/innergrid_2025441247/xcol1/linklist/link_667226045_copy.1332933720.file/PS9jb250ZW50L2RhbS9hc3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL3F1YXJ0ZXJsaWVzLzIwMjMvNHEyMy9zZWMtZmlsaW5ncy8yMGYtZnVsbC1yZXBvcnQtdWJzLWdyb3VwLWFnLWNvbnNvbGlkYXRlZC0yMDIzLnBkZg==/20f-full-report-ubs-group-ag-consolidated-2023.pdf',
        "title": 'UBS Group AG 2023 20-f',
        "context": "Annual Report"
    },
    {
        "url": 'https://d18rn0p25nwr6d.cloudfront.net/CIK-0001321655/301c4e7c-bc97-4414-ad8b-3c84568750eb.pdf',
        "title": 'Palantir 2023 10-k',
        "context": "Annual Report"
    },
    {
        "url": 'https://s2.q4cdn.com/470004039/files/doc_earnings/2023/q4/filing/_10-K-Q4-2023-As-Filed.pdf',
        "title": 'Apple 2023 10-K',
        "context": "Annual Report"
    },

    # Mashreq Documents
    {
        "url": 'https://www.mashreq.com/-/jssmedia/pdfs/neo/cards/noon/20200721_Digital_Card_FAQs_TCs_Digital_Onboarding.ashx',
        "title": 'Mashreq - Instant Digital Credit card from Mashreq Frequently Asked Questions and Terms & Conditions',
        "context": "Annual Report"
    },
    {
        "url": 'https://www.mashreq.com/-/jssmedia/pdfs/neo/accounts-deposits/KFS/Local_Transfers_KFS_Eng.ashx',
        "title": 'Mashreq - KEY FACTS STATEMENT - MONEY TRANSFERS',
        "context": "Annual Report"
    },
    {
        "url": 'https://digital.mashreqbank.com/creditcards/dynamic/media/documents/SPC92-C/Cashback_Offers_Terms.pdf',
        "title": 'Mashreq - Pure Savings on your new Mashreq Credit Card!',
        "context": "Annual Report"
    },
    {
        "url": 'https://www.mashreq.com/-/jssmedia/pdfs/aboutus/audit/Mashreq_Sustainability_Report_2023_EN.ashx',
        "title": 'Mashreq - Sustainability Report 2023',
        "context": "Annual Report"
    },
    {
        "url": 'https://www.mashreq.com/-/jssmedia/pdfs/aboutus/investors/2023/FY-2023-Results-Presentation.ashx',
        "title": 'Mashreq - FY 2023 Results Presentation',
        "context": "Annual Report"
    },

    # Policing Handbook
    {
        "url": 'https://www.homeworkforyou.com/static_media/uploadedfiles/An%20Introduction%20to%20Policing.pdf',
        "title": 'Introduction to Policing',
        "context": "Policing Handbook"
    }
]

# Example usage
if __name__ == "__main__":
    for pdf in pdfs:
        print(" #### Processing: " + pdf['title'] + " ####")
        print("Starting Text Extraction Process")
        # Pass on parsed content
        llm_enriched_text = llm_router(
            content=url_parser(
                url=pdf['url'],
                title=pdf['title']
            ),
            context=pdf['context'],
            title=pdf['title']
        )
