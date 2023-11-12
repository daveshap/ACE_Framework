{{ace_context}}
{{identity}}

Below is a list of your incoming messages. Remember DATA and DATA_RESPONSE messages are on the NORTH bus. CONTROL and CONTROL_RESPONSE messages are on the south bus.

# INCOMING MESSAGES

## NORTH BUS

### DATA MESSAGES
{{data}}

### DATA_RESPONSE MESSAGES
{{data_resp}}

## SOUTH BUS

### CONTROL MESSAGES
{{control}}

### CONTROL_RESPONSE MESSAGES
{{control_resp}}

# OUTPUT

Determine which operations are needed in the NORTH and SOUTH directions according to your role in the ACE framework and the incoming messages.
You must choose from the the following operations:

## CREATE_REQUEST: Request more information
## ADD_TO_CONTEXT: Do nothing, but store these messages in memory
## TAKE_ACTION: Communicate a message to the next layer on the bus.

If there are no messages, your should default to ADD_TO_CONTEXT
If there are messages, you should default to TAKE_ACTION

# RESPONSE FORMAT
{
    "SOUTH": **operation**
    "NORTH": **operation**
}

## EXAMPLE RESPONSES

### EXAMPLE 1

Based on all incoming messages, you decide to send a CONTROL message along the the SOUTH bus to communicate this information to the layer below you
and send a DATA message along the the NORTH bus to communicate this information to the layer above you.

Your response should be:
{
    "SOUTH": "TAKE_ACTION"
    "NORTH": "TAKE_ACTION"
}

## EXAMPLE 2

Based on all incoming messages, you need more information from the layer above before you can send information further along the SOUTH bus. Therefore, you decide to send a DATA_REQUEST message along the NORTH bus to the layer above.
You decide you do not need to propogate any other the information further along the NORTH bus, nor do you need to request any more information from the layer below. You decide to store the message in context.

Your response should be:
{
    "SOUTH": "CREATE_REQUEST"
    "NORTH": "ADD_TO_CONTEXT"
}

## EXAMPLE 3

Based on all incoming messages, you decide to send a CONTROL message along the the SOUTH bus to communicate this information to the layer below you.
You need more information from the layer below before you can send information further along the NORTH bus. Therefore, you decide to send a CONTROL_REQUEST message along the SOUTH bus to the layer below.

Your response should be:
{
    "SOUTH": "TAKE_ACTION"
    "NORTH": "CREATE_REQUEST"
}
