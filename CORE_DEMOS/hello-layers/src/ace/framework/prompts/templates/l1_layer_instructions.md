{{ace_context}}
{{identity}}

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

{{operation_prompt}}

## FORMAT

Your response should be an array of messages with type, direction and text attributes. 
The direction should always be "southbound". The type should always be "CONTROL" or "CONTROL_RESPONSE".
If no messages are needed, retunr an empty array.
For example:
[
    {
        "type": "CONTROL",
        "direction": "southbound",
        "message": "Create a strategy to accomplish the mission"
    },
    {
        "type": "CONTROL_RESPONSE",
        "direction": "southbound",
        "message": "The global strategy you created does not align with our moral principles"
    }
]