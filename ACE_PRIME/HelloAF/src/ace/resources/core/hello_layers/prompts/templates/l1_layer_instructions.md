{{ace_context}}
{{identity}}

Below is a list of your incoming messages.

# INCOMING MESSAGES

### DATA MESSAGES
{{data}}

## TELEMETRY MESSAGES
{{telemetry}}

## RESPONSE FORMAT

Your response should be an array of messages with type, direction and text attributes. 
The direction should always be "southbound". The type should always be "CONTROL". The
direction should always be "southbound".
If no messages are needed, return an empty array.
For example:
[
    {
        "type": "CONTROL",
        "direction": "southbound",
        "message": "Create a strategy to accomplish the mission"
    },
]
