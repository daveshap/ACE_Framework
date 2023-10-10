from jinja2 import Template

take_action_data = Template("""
    Process the information from all message types and output a new DATA message for the layer above you.

    {{layer_outputs}}
"""
)

take_action_data_l1 = Template("""
    Process the information from all message types and create a new CONTROL message with your response.

    {{layer_outputs}}
"""
)

take_action_control = Template("""
    Process the information from all message types and create a new CONTROL message to communicate relevant information to the layer below you.

    {{layer_outputs}}
"""
)

create_request_data = """
    Process the information from the DATA and DATA_RESPONSE message types and create a request asking for more information. Be specific about what information you need. 
"""

create_request_control = """
    Process the information from the CONTROL and CONTROL_RESPONSE message types create a request asking for more information. Be specific about what information you need. 
"""

do_nothing_data= """
    Do not do anything in response to the DATA and DATA_RESPONSE message types. 
"""

do_nothing_data= """
    Do not do anything in response to the CONTROL and CONTROL_RESPONSE message types. 
"""