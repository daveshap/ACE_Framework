import yaml
import functools
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Dialog, Frame, Button, Label, TextArea, RadioList
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.data import YamlLexer
from prompt_toolkit.filters import Condition

HELP_MESSAGE = """
Keyboard shortcuts:
    1-6: Switch to layer 1-6
    c: Add to 'control' list.
    d: Add to 'data' list.
    r: Add to 'request' list.
    s: Add to 'response' list.
    t: Add to 'telemetry' list.
    q: Quit the application.
"""

style = Style.from_dict({
    'dialog': 'noinherit',
    'dialog.body': 'noinherit',
    'dialog.shadow': 'noinherit',
    'dialog.border': 'noinherit',
    'label': 'noinherit',
    'button.focused': 'bg:#00FFFF #FFFFFF',
    'radiolist': 'noinherit',
    'radiolist.current': 'bold underline',
    'text-area': 'bg:#000000 #FFFFFF',
})

layers = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
]

# The dict we're building
data_dict = {}
for layer in layers:
    data_dict[f"layer_{layer}"] = {
        'data': [],
        'control': [],
        'request': [],
        'response': [],
        'telemetry': []
    }

active_layer = None
active_layer_name = None

# Key bindings
kb = KeyBindings()

dialog = None

# Create a condition that checks if the dialog is not focused.
dialog_not_focused = Condition(lambda: dialog is None)

# Create the TextArea and assign it to a variable
text_area = TextArea(multiline=False)

# Create the RadioList and assign it to a variable
radio_list = RadioList(values=[
    ('northbound', 'Northbound'),
    ('southbound', 'Southbound'),
])

data_display = TextArea(lexer=PygmentsLexer(YamlLexer), read_only=True)


@kb.add('q', filter=dialog_not_focused)
def _(event):
    " Handle 'c-q': Quit the application. "
    event.app.exit()


def layer_kb_callback(layer):
    def callback(event):
        set_active_layer(layer)
    return callback


for layer in layers:
    kb.add(layer, filter=dialog_not_focused)(layer_kb_callback(layer))


@kb.add('c', filter=dialog_not_focused)
def _(event):
    " Handle 'c-d': Open the dialog for adding a dict to the 'control' list."
    global dialog
    global active_layer_name
    dialog = Dialog(
        title=f"{active_layer_name}: Add CONTROL messages",
        body=HSplit([
            Label(text='Message:'),
            text_area,
        ]),
        buttons=[
            Button(text='Add', handler=functools.partial(add, "control")),
            Button(text='Cancel', handler=cancel),
            Button(text="Clear data", handler=functools.partial(clear, "control")),
        ]
    )
    event.app.layout = Layout(dialog, focused_element=dialog)


@kb.add('d', filter=dialog_not_focused)
def _(event):
    " Handle 'c-d': Open the dialog for adding a dict to the 'data' list."
    global dialog
    global active_layer_name
    dialog = Dialog(
        title=f"{active_layer_name}: Add DATA messages",
        body=HSplit([
            Label(text='Message:'),
            text_area,
        ]),
        buttons=[
            Button(text='Add', handler=functools.partial(add, "data")),
            Button(text='Cancel', handler=cancel),
            Button(text="Clear data", handler=functools.partial(clear, "data")),
        ]
    )
    event.app.layout = Layout(dialog, focused_element=dialog)


@kb.add('r', filter=dialog_not_focused)
def _(event):
    global dialog
    global active_layer_name
    " Handle 'c-r': Open the dialog for adding a dict to the 'request' list."
    dialog = Dialog(
        title=f"{active_layer_name}: Add REQUEST messages",
        body=HSplit([
            Label(text='Direction:'),
            radio_list,
            Label(text='Message:'),
            text_area,
        ]),
        buttons=[
            Button(text='Add', handler=functools.partial(add, "request")),
            Button(text='Cancel', handler=cancel),
            Button(text="Clear data", handler=functools.partial(clear, "request")),
        ]
    )
    event.app.layout = Layout(dialog, focused_element=dialog)


@kb.add('s', filter=dialog_not_focused)
def _(event):
    global dialog
    global active_layer_name
    " Handle 'c-s': Open the dialog for adding a dict to the 'response' list."
    dialog = Dialog(
        title=f"{active_layer_name}: Add RESPONSE messages",
        body=HSplit([
            Label(text='Direction:'),
            radio_list,
            Label(text='Message:'),
            text_area,
        ]),
        buttons=[
            Button(text='Add', handler=functools.partial(add, "response")),
            Button(text='Cancel', handler=cancel),
            Button(text="Clear data", handler=functools.partial(clear, "response")),
        ]
    )
    event.app.layout = Layout(dialog, focused_element=dialog)


@kb.add('t', filter=dialog_not_focused)
def _(event):
    " Handle 'c-t': Open the dialog for adding a dict to the 'telemetry' list."
    global dialog
    global active_layer_name
    dialog = Dialog(
        title=f"{active_layer_name}: Add TELEMETRY messages",
        body=HSplit([
            Label(text='Message:'),
            text_area,
        ]),
        buttons=[
            Button(text='Add', handler=functools.partial(add, "telemetry")),
            Button(text='Cancel', handler=cancel),
            Button(text="Clear data", handler=functools.partial(clear, "telemetry")),
        ]
    )
    event.app.layout = Layout(dialog, focused_element=dialog)


def clear(key):
    global dialog
    global active_layer_name
    " Clear the list. "
    data_dict[active_layer_name][key] = []
    reset_values()
    update_output_display()
    # Reset the layout
    app.layout = layout
    dialog = None


def add(key):
    " Add a dict to the 'data' list. "
    global dialog
    global active_layer_name
    # Get the message from the TextArea
    new_message = {
        'message': text_area.text,
    }
    if key in ['request', 'response']:
        new_message['direction'] = radio_list.current_value
    reset_values()
    data_dict[active_layer_name][key].append(new_message)
    update_output_display()
    # Reset the layout
    app.layout = layout
    dialog = None


def update_output_display():
    global active_layer
    global active_layer_name
    data_display.text = f"# {active_layer_name.upper()}\n\n" + yaml.dump(active_layer, default_flow_style=False)


def set_active_layer(layer):
    global active_layer
    global active_layer_name
    active_layer_name = f"layer_{layer}"
    active_layer = data_dict[active_layer_name]
    update_output_display()


def cancel():
    " Cancel adding a dict to the 'data' list. "
    global dialog
    # Reset the layout
    reset_values()
    app.layout = layout
    dialog = None


def reset_values():
    text_area.text = ''
    radio_list.current_value = None


set_active_layer(layers[0])
# The initial layout
body = Frame(body=HSplit([
    Label(text=HELP_MESSAGE),
    data_display,
]))
root_container = VSplit([body])
layout = Layout(root_container)

# The application
app = Application(key_bindings=kb, layout=layout, full_screen=True, style=style)

# Run the application
app.run()
