from jinja2 import Template

take_action_data = Template(
"""
    Process the information from all message types and output a new DATA message for the layer above you.

    {{layer_outputs}}
"""
)

take_action_data_l1 = Template(
"""
    Process the information from all message types and create a new CONTROL message with your response. 

    {{layer_outputs}}

    If there are no incoming messages, then communicate the your mission to the layer below.
"""
)

take_action_control = Template(
"""
    Process the information from all message types and create a new CONTROL message to communicate relevant information to the layer below you.

    {{layer_outputs}}
"""
)

create_request_data = """
    Process the information from the DATA and DATA_RESPONSE message types and create a CONTROL_REQUEST message asking for more information. Be specific about what information you need. 
"""

create_request_control = """
    Process the information from the CONTROL and CONTROL_RESPONSE message types create a DATA_REQUEST request asking for more information. Be specific about what information you need. 
"""

do_nothing_data= """
    Do not create any DATA or DATA_REQUEST messages. 
"""

do_nothing_control= """
    Do not create any CONTROL or CONTROL_REQUEST messages. 
"""