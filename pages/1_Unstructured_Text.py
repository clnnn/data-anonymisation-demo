import streamlit as st

from pages.data.text_examples import text_examples
from pages.data.operators import operators
from pages.data.spacy_models import spacy_models

from presidio_analyzer.nlp_engine import TransformersNlpEngine
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
from presidio_anonymizer.entities import OperatorConfig

page_title = "Unstructured Text"
st.set_page_config(page_title=page_title, page_icon="📝")
st.title(page_title)

# Configure the text example, anonymization method, and model
with st.sidebar:
    st.markdown("## Configuration")

    model = st.selectbox(
        "Model:", list(spacy_models.keys()), placeholder="Choose a model"
    )
    spacy_model = (
        spacy_models[model] if model in spacy_models else spacy_models["English"]
    )

    example = st.selectbox(
        "Text Examples:",
        list(text_examples.keys()),
        index=None,
        placeholder="Choose an example",
    )
    text_example = text_examples[example] if example in text_examples else ""

    method = st.selectbox(
        "Anonymization Method:", list(operators.keys()), placeholder="Choose a method"
    )
    operator = operators[method] if method in operators else operators["Masking"]
    if operator["type"] == "encrypt":
        st.info(
            f'The encryption key `{operator["key"]}` is hardcoded in this example. For production use, store the key securely.'
        )

text = st.text_area("Text:", text_example.strip(), height=400)

if text.strip() == "":
    st.stop()

# Analyze the text
model_config = [
    {
        "lang_code": "en",
        "model_name": {
            "spacy": spacy_model,  # use a small spaCy model for lemmas, tokens etc.
            "transformers": "dslim/bert-base-NER",
        },
    }
]
nlp_engine = TransformersNlpEngine(models=model_config)
pii_analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
entities = pii_analyzer.analyze(text=text, language="en")

# Display entities
with st.expander("Identified PII Entities"):
    st.table(
        [
            {
                "Text": text[entity.start : entity.end],
                "Entity": entity.entity_type,
                "Score": entity.score,
                "Start": entity.start,
                "End": entity.end,
            }
            for entity in entities
        ]
    )

# Anonymize the text
anonymizer = AnonymizerEngine()
anonymized_result = anonymizer.anonymize(
    text=text,
    analyzer_results=entities,
    operators={"DEFAULT": OperatorConfig(operator["type"], operator)},
)

# Display anonymized text
st.text_area(
    "Anonymized text:", value=anonymized_result.text, disabled=True, height=400
)

# Decrypt the text and deanonymize it
if operator["type"] == "encrypt":
    decrypt_key = st.text_input("Decryption Key:")
    try:
        deanonymizer = DeanonymizeEngine()
        deanonymized_text = deanonymizer.deanonymize(
            text=anonymized_result.text,
            entities=anonymized_result.items,
            operators={"DEFAULT": OperatorConfig("decrypt", {"key": decrypt_key})},
        )
        st.text(deanonymized_text.text)
    except Exception as e:
        st.error("Invalid decryption key")
