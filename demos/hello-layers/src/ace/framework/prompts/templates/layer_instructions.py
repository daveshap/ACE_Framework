from jinja2 import Template

layer_instructions = Template(
    """
    {{ace_context}}
    {{identitiy}}

    Below is a list of your incoming messages.
    
    # INCOMING MESSAGES

    ## TELEMETRY MESSAGES
    {{telemetry}}

    ## NORTH BUS

    ### DATA MESSAGES
    {{data}}

    ### DATA_RESPONSE MESSAGES
    {{data_resp}}

    ### DATA_REQUEST MESSAGES
    {{data_req}}

    ## SOUTH BUS

    ### CONTROL MESSAGES
    {{control}}

    ### CONTROL_RESPONSE MESSAGES
    {{control_resp}}

    ### CONTROL_REQUEST MESSAGES
    {{control_req}}

    # RESPONSE 

    Request message types require immediate response. Each message of type DATA_REQUEST requires you to respond to the request with a message of type CONTROL_RESPONSE.
    Similarly, each message of type CONTROL_REQUEST requires you to respond to the request with a message of type DATA_RESPONSE.
    Your responses should use "question in answer" format.

    {{control_operation_prompt}}

    {{data_operation_prompt}}

    ## FORMAT 

    Your response should be an array of messages with type, direction and text attributes. For example:
    [
        {
            "type": "DATA_RESPONSE",
            "direction": "NORTH",
            "text": "Please clarify the mission"
        },
        {
            "type": "DATA",
            "direction": "NORTH",
            "text": "We received the following input from the user: How can I live a healthier lifestyle?"
        }
    ]

    """
)