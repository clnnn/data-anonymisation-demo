import streamlit as st
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import TransformersNlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import pandas as pd

examples = [
    """Patient: Jane Doe
Date of Birth: 05/15/1980
Diagnosis: Hypertension
Medication: Lisinopril 10mg""",
    """Hi John,
I hope you're doing well. Please find the attached invoice for your recent purchase.
Best regards,
Alice Smith
alice.smith@emailprovider.com""",
    """Transaction ID: 10
Amount: $500.00
Card Number: 5425-2334-3010-9903
Expiry Date: 12/25""",
    """Hello, my name is David Johnson and I live in Maine.
My credit card number is 4095-2609-9393-4932 and my crypto wallet id is 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ.

On September 18 I visited microsoft.com and sent an email to test@presidio.site,  from the IP 192.168.0.1.

My passport: 191280342 and my phone number: (212) 555-1234.

This is a valid International Bank Account Number: IL150120690000003111111 . Can you please check the status on bank account 954567876544?

Kate's social security number is 078-05-1126.  Her driver license? it is 1234567A.""",
]


st.set_page_config(page_title="Raw Text", page_icon="📝")
st.title("Raw Text")

text_area_element = st.empty()
text_area_element.text_area("Enter some text:")
choice = st.selectbox(
    "Predefined examples:",
    examples,
    index=None,
    placeholder="Choose an example",
)
text = text_area_element.text_area("Enter some text", value=choice, height=200)

if text:
    # Define which transformers model to use
    model_config = [
        {
            "lang_code": "en",
            "model_name": {
                "spacy": "en_core_web_sm",  # use a small spaCy model for lemmas, tokens etc.
                "transformers": "dslim/bert-base-NER",
            },
        }
    ]

    nlp_engine = TransformersNlpEngine(models=model_config)

    # Set up the engine, loads the NLP module (spaCy model by default)
    # and other PII recognizers
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine)

    # Call analyzer to get results
    results = analyzer.analyze(text=text, language="en")

    # Analyzer results are passed to the AnonymizerEngine for anonymization

    anonymizer = AnonymizerEngine()
    operator = "mask"
    operator_config = {
        "type": operator,
        "masking_char": "*",
        "chars_to_mask": 100,
        "from_end": False,
    }
    anonymized_text = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={"DEFAULT": OperatorConfig(operator, operator_config)},
    )

    st.text_area(
        "Anonymized text:", value=anonymized_text.text, disabled=True, height=200
    )

    df = pd.DataFrame(
        [
            {
                "Text": text[entity.start : entity.end],
                "Entity": entity.entity_type,
                "Score": entity.score,
                "Start": entity.start,
                "End": entity.end,
            }
            for entity in results
        ]
    )
    st.table(df)
