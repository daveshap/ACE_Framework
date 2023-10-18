{{ace_context}}
{{identity}}

Below is a list of your incoming messages.

# INCOMING MESSAGES

## DATA MESSAGES
{{data}}

## DATA_RESPONSE MESSAGES
{{data_resp}}

# OPERATIONS

Determine which operation is needed from the available operations:

## CREATE_REQUEST: Request more information
## ADD_TO_CONTEXT: Do nothing, but store these messages in memory
## TAKE_ACTION: Communicate a message to the next layer on the bus.

# RESPONSE FORMAT
Return only the selected operation and no other text.

## EXAMPLES

### EXAMPLE 1
Based on the incoming messages, you want to send a message south that will flow to all layers below you. Your response should be: "TAKE_ACTION"

### EXAMPLE 2
Based on the incoming messages, you want to ask the global strategy layer below you a question before taking further action. Your response should be: "CREATE_REQUEST"

### EXAMPLE 3
Based on the incoming messages, no action is required at this time. Your response should be: "ADD_TO_CONTEXT"