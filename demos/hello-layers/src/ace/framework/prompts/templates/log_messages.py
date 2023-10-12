from jinja2 import Template

op_classifier_log = Template(
    """
    # OPERATION CLASSIFIER PROMPT

    {{op_classifier_req}}


    # OPERATION CLASSIFIER RESPONSE

    {{op_classifier_resp}}
    """
)

layer_messages_log = Template(
    """
    # LLM PROMPT

    {{llm_req}}


    # LLM RESPONSE

    {{llm_resp}}
    """
)