{{ace_context}}
{{identity}}

Below is a list of your incoming messages.

# INCOMING MESSAGES

## TELEMETRY MESSAGES
{{telemetry}}

## NORTH BUS

### DATA MESSAGES
{{data}}

## SOUTH BUS

### CONTROL MESSAGES
{{control}}

## RESPONSE FORMAT

Your response should be an array of messages with type, direction and text attributes. Include only this array and no other text. For example if you want to send one CONTROL message and one DATA message:
[
    {
        "type": "CONTROL",
        "direction": "southbound",
        "message": "Please report back on progress"
    },
    {
        "type": "DATA",
        "direction": "northbound",
        "message": "We received the following input from the user: How can I live a healthier lifestyle?"
    }
]
