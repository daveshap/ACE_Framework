from jinja2 import Template

layer_instructions = Template(
    """
    {{ace_context}}
    {{identitiy}}

    Below is a list of your incoming messages.
    
    # INCOMING MESSAGES

    ### DATA MESSAGES
    {{data}}

    ### DATA_RESPONSE MESSAGES
    {{data_resp}}

    ### DATA_REQUEST MESSAGES
    {{data_req}}

    ## TELEMETRY MESSAGES
    {{telemetry}}

    # RESPONSE 

    DATA_REQUEST message types require immediate response. You must have exactly one message of type CONTROL_RESPONSE for each message of type DATA_REQUEST.

    {{control_operation_prompt}}
    
    ## FORMAT

    Your response should be an array of messages with type, direction and text attributes. 
    The direction should always be "SOUTH". The type should always be "CONTROL" or "CONTROL_RESPONSE".
    If no messages are needed, retunr an empty array.
    For example:
    [
        {
            "type": "CONTROL_RESPONSE",
            "direction": "SOUTH",
            "text": "Send additional data"
        },
        {
            "type": "CONTROL",
            "direction": "SOUTH",
            "text": "Create a strategy to end hunger worldwide"
        }
    ]
    """
)