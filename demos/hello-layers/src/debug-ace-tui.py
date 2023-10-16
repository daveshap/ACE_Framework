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

DEFAULT_HELP_MESSAGE = """
Keyboard shortcuts:
    1-6: Switch to layer 1-6
    c: Add to 'control' list.
    d: Add to 'data' list.
    r: Add to 'request' list.
    s: Add to 'response' list.
    t: Add to 'telemetry' list.
    e: Erase all for current layer.
    q: Quit the application.
"""

DEFAULT_STYLE = Style.from_dict({
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

DEFAULT_LAYERS = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
]


class DebugAceTui:
    def __init__(self):
        self.help_message = DEFAULT_HELP_MESSAGE
        self.style = DEFAULT_STYLE
        self.layers = DEFAULT_LAYERS

        self.data_dict = {f"layer_{layer}": self.empty_data() for layer in self.layers}
        self.active_layer = None
        self.active_layer_name = None
        self.active_layer_number = self.layers[0]
        self.dialog = None
        self.dialog_not_focused = Condition(lambda: self.dialog is None)
        self.current_dialog_key = None
        self.text_area = TextArea(multiline=True)
        self.radio_list = RadioList(values=[('northbound', 'Northbound'), ('southbound', 'Southbound')])
        self.data_display = TextArea(lexer=PygmentsLexer(YamlLexer), read_only=True)
        # self.current_messages_display = TextArea(lexer=PygmentsLexer(YamlLexer), read_only=True)
        self.kb = KeyBindings()
        self.app = Application(key_bindings=self.kb, full_screen=True, style=self.style)

        self._init_key_bindings()
        self.set_active_layer(self.active_layer_number)

    def empty_data(self):
        return {
            'data': [],
            'control': [],
            'request': [],
            'response': [],
            'telemetry': [],
        }

    def _init_key_bindings(self):
        @self.kb.add('q', filter=self.dialog_not_focused)
        def _(event):
            event.app.exit()

        for layer in self.layers:
            self.kb.add(layer, filter=self.dialog_not_focused)(self.layer_kb_callback(layer))

        @self.kb.add('c', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("control", "Add/edit CONTROL messages")

        @self.kb.add('d', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("data", "Add DATA/edit messages")

        @self.kb.add('r', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("request", "Add/edit REQUEST messages", include_direction=True)

        @self.kb.add('s', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("response", "Add/edit RESPONSE messages", include_direction=True)

        @self.kb.add('t', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("telemetry", "Add/edit TELEMETRY messages")

        @self.kb.add('e', filter=self.dialog_not_focused)
        def _(event):
            self.clear_layer()

        @self.kb.add('c-s', filter=~self.dialog_not_focused)
        def _(event):
            self.open_message_selector("edit")

        @self.kb.add('c-d', filter=~self.dialog_not_focused)
        def _(event):
            self.open_message_selector("delete")

    def layer_kb_callback(self, layer):
        def callback(event):
            self.set_active_layer(layer)
        return callback

    def build_fields(self, include_direction=False):
        fields = []
        if include_direction:
            fields.append(Label(text='Direction:'))
            fields.append(self.radio_list)
        fields.append(Label(text='Message:'))
        fields.append(self.text_area)
        return fields

    def open_dialog(self, key, title, include_direction=False):
        self.current_dialog_key = key
        full_title = f"{self.active_layer_name}: {title}"
        existing_messages = bool(self.data_dict[self.active_layer_name][key])
        fields = self.build_fields(include_direction=include_direction)
        # self.current_messages_display.text = yaml.dump(self.data_dict[self.active_layer_name][key], default_flow_style=False, sort_keys=True)
        # fields.append(self.current_messages_display)
        buttons = [
            Button(text='Add', handler=functools.partial(self.add, key)),
            Button(text='Cancel', handler=self.cancel),
            Button(text="Clear", handler=functools.partial(self.clear_type, key)),
        ]
        if existing_messages:
            full_title += " -- Ctrl-S to edit, Ctrl-D to delete"
            buttons.append(Button(text='Edit', handler=functools.partial(self.open_message_selector, "edit")))
            buttons.append(Button(text='Delete', handler=functools.partial(self.open_message_selector, "delete")))
        self.dialog = Dialog(
            title=full_title,
            body=HSplit(fields),
            buttons=buttons
        )
        self.app.layout = Layout(self.dialog, focused_element=self.dialog)

    def edit_dialog(self, key, index, title, include_direction=False):
        self.reset_values()
        message = self.data_dict[self.active_layer_name][key][index]
        self.text_area.text = message['message']
        if 'direction' in message:
            self.radio_list.current_value = message['direction']
        fields = self.build_fields(include_direction)
        buttons = [
            Button(text='OK', handler=functools.partial(self.edit, key, index)),
            Button(text='Cancel', handler=self.cancel),
        ]
        self.dialog = Dialog(
            title=f"{self.active_layer_name}: {title}",
            body=HSplit(fields),
            buttons=buttons
        )
        self.app.layout = Layout(self.dialog, focused_element=self.dialog)

    def clear_type(self, key):
        self.data_dict[self.active_layer_name][key] = []
        self.reset_values()
        self.update_output_display()
        self.app.layout = self.layout
        self.dialog = None

    def clear_layer(self):
        self.data_dict[self.active_layer_name] = self.empty_data()
        self.reset_values()
        self.set_active_layer(self.active_layer_number)
        self.app.layout = self.layout
        self.dialog = None

    def add(self, key):
        new_message = self.get_message_from_dialog(key)
        self.data_dict[self.active_layer_name][key].append(new_message)
        self.update_after_change(key)

    def edit(self, key, index):
        new_message = self.get_message_from_dialog(key)
        self.data_dict[self.active_layer_name][key][index] = new_message
        self.update_after_change(key)

    def get_message_from_dialog(self, key):
        new_message = {'message': self.text_area.text}
        if key in ['request', 'response']:
            new_message['direction'] = self.radio_list.current_value
        self.reset_values()
        return new_message

    def update_after_change(self, key):
        self.current_dialog_key = None
        self.update_output_display()
        self.app.layout = self.layout
        self.dialog = None

    def open_message_selector(self, action):
        key = self.current_dialog_key
        values = [(i, yaml.dump(msg, default_flow_style=False, sort_keys=True)) for i, msg in enumerate(self.data_dict[self.active_layer_name][key])]
        radio_list = RadioList(values)

        def handler():
            index = radio_list.current_value
            if action == "edit":
                self.edit_dialog(key, index, f"Edit {key.upper()} message", include_direction='direction' in self.data_dict[self.active_layer_name][key][index])
            elif action == "delete":
                self.delete_message(key, index)

        dialog = Dialog(
            title=f"Select a message to {action}",
            body=HSplit([Label(text='Message:'), radio_list]),
            buttons=[
                Button(text='OK', handler=handler),
                Button(text='Cancel', handler=self.cancel),
            ]
        )
        self.app.layout = Layout(dialog, focused_element=dialog)

    def delete_message(self, key, index):
        del self.data_dict[self.active_layer_name][key][index]
        self.update_after_change(key)

    def update_output_display(self):
        text = []
        text.append(f"# ACTIVE LAYER: {self.active_layer_name.upper()}")
        text.append(yaml.dump(self.active_layer, default_flow_style=False, sort_keys=True))
        text.append("# OTHER LAYERS:")
        for layer in self.layers:
            if layer != self.active_layer_number:
                name = f"layer_{layer}"
                text.append(f"## {name.upper()}")
                text.append(yaml.dump(self.data_dict[name], default_flow_style=False, sort_keys=True))
        self.data_display.text = "\n\n".join(text)

    def set_active_layer(self, layer):
        self.active_layer_number = layer
        self.active_layer_name = f"layer_{layer}"
        self.active_layer = self.data_dict[self.active_layer_name]
        self.update_output_display()

    def cancel(self):
        self.reset_values()
        self.app.layout = self.layout
        self.dialog = None

    def reset_values(self):
        self.text_area.text = ''
        self.radio_list.current_value = None

    def run(self):
        body = Frame(body=HSplit([Label(text=self.help_message), self.data_display]))
        root_container = VSplit([body])
        self.layout = Layout(root_container)
        self.app.layout = self.layout
        self.app.run()


if __name__ == "__main__":
    DebugAceTui().run()
