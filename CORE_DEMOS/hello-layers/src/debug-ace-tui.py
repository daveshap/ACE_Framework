import yaml
import httpx
import functools
from datetime import datetime

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.widgets import Dialog, Frame, Button, Label, TextArea, RadioList
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.data import YamlLexer
from prompt_toolkit.filters import Condition

from ace import constants
from ace.settings import Settings
from ace.debug_endpoint import DebugEndpoint
from ace.framework.resources.telemetry_manager import TelemetryManager

DEFAULT_HELP_MESSAGE = """
Keyboard shortcuts:
    1-6: Switch to layer 1-6
    c: Add to 'control' list.
    d: Add to 'data' list.
    r: Add to 'request' list.
    s: Add to 'response' list.
    t: Add to 'telemetry' list.
    b: Toggle debug state for all layers.
    x: Send the current messages for the active layer.
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


class DataType:
    def __init__(self, settings):
        self.settings = settings

    def multiline_text(self):
        return TextArea(multiline=True)

    def bus_direction(self):
        return RadioList(values=[('northbound', 'Northbound'), ('southbound', 'Southbound')])

    def get_southbound_source(self, layer):
        previous_index = self.settings.layers.index(layer) - 1
        return 'debug' if previous_index < 0 else self.settings.layers[previous_index]

    def get_northbound_source(self, layer):
        next_index = self.settings.layers.index(layer) + 1
        return 'debug' if next_index >= len(self.settings.layers) else self.settings.layers[next_index]

    def message_metadata(self, message, message_type, source, destination, direction):
        message['type'] = message_type
        message['resource'] = {
            'source': source,
            'destination': destination,
        }
        message['direction'] = direction
        message['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return message


class ControlDataType(DataType):
    key = 'control'

    def __init__(self, settings):
        super().__init__(settings)
        self.message = self.multiline_text()

    def build_fields(self, data=None):
        if data:
            self.message.text = data['message']
        else:
            self.reset_values()
        fields = []
        fields.append(Label(text='Message:'))
        fields.append(self.message)
        return fields

    def get_message_from_dialog(self):
        new_message = {
            'message': self.message.text,
        }
        self.reset_values()
        return new_message

    def build_ui_message(self, data):
        message = {
            'message': data['message'],
        }
        return message

    def build_layer_message(self, layer, data):
        source = self.get_southbound_source(layer)
        message = {
            'message': data['message'],
        }
        return self.message_metadata(message, 'control', source, layer, 'southbound')

    def reset_values(self):
        self.message.text = ''


class DataDataType(DataType):
    key = 'data'

    def __init__(self, settings):
        super().__init__(settings)
        self.message = self.multiline_text()

    def build_fields(self, data=None):
        if data:
            self.message.text = data['message']
        else:
            self.reset_values()
        fields = []
        fields.append(Label(text='Message:'))
        fields.append(self.message)
        return fields

    def get_message_from_dialog(self):
        new_message = {
            'message': self.message.text,
        }
        self.reset_values()
        return new_message

    def build_ui_message(self, data):
        message = {
            'message': data['message'],
        }
        return message

    def build_layer_message(self, layer, data):
        source = self.get_northbound_source(layer)
        message = {
            'message': data['message'],
        }
        return self.message_metadata(message, 'data', source, layer, 'northbound')

    def reset_values(self):
        self.message.text = ''


class RequestDataType(DataType):
    key = 'request'

    def __init__(self, settings):
        super().__init__(settings)
        self.direction = self.bus_direction()
        self.message = self.multiline_text()

    def build_fields(self, data=None):
        if data:
            self.direction.current_value = data['direction']
            self.message.text = data['message']
        else:
            self.reset_values()
        fields = []
        fields.append(Label(text='Direction:'))
        fields.append(self.direction)
        fields.append(Label(text='Message:'))
        fields.append(self.message)
        return fields

    def get_message_from_dialog(self):
        new_message = {
            'direction': self.direction.current_value,
            'message': self.message.text,
        }
        self.reset_values()
        return new_message

    def build_ui_message(self, data):
        message = {
            'direction': data['direction'],
            'message': data['message'],
        }
        return message

    def build_layer_message(self, layer, data):
        direction = data['direction']
        source = self.get_southbound_source(layer) if direction == 'southbound' else self.get_northbound_source(layer)
        message = {
            'message': data['message'],
        }
        return self.message_metadata(message, 'request', source, layer, direction)

    def reset_values(self):
        self.direction.current_value = None
        self.message.text = ''


class ResponseDataType(DataType):
    key = 'response'

    def __init__(self, settings):
        super().__init__(settings)
        self.direction = self.bus_direction()
        self.message = self.multiline_text()

    def build_fields(self, data=None):
        if data:
            self.direction.current_value = data['direction']
            self.message.text = data['message']
        else:
            self.reset_values()
        fields = []
        fields.append(Label(text='Direction:'))
        fields.append(self.direction)
        fields.append(Label(text='Message:'))
        fields.append(self.message)
        return fields

    def get_message_from_dialog(self):
        new_message = {
            'direction': self.direction.current_value,
            'message': self.message.text,
        }
        self.reset_values()
        return new_message

    def build_ui_message(self, data):
        message = {
            'direction': data['direction'],
            'message': data['message'],
        }
        return message

    def build_layer_message(self, layer, data):
        direction = data['direction']
        source = self.get_southbound_source(layer) if direction == 'southbound' else self.get_northbound_source(layer)
        message = {
            'message': data['message'],
        }
        return self.message_metadata(message, 'response', source, layer, direction)

    def reset_values(self):
        self.direction.current_value = None
        self.message.text = ''


class TelemetryDataType(DataType):
    key = 'telemetry'

    def __init__(self, settings):
        super().__init__(settings)
        self.telemetry_manager = TelemetryManager()
        self.namespace = RadioList(values=[(namespace, namespace) for namespace in self.telemetry_manager.namespace_map.keys()])
        self.data = self.multiline_text()

    def build_fields(self, data=None):
        if data:
            self.namespace.current_value = data['namespace']
            self.data.text = data['data']
        else:
            self.reset_values()
        fields = []
        fields.append(Label(text='Namespace:'))
        fields.append(self.namespace)
        fields.append(Label(text='Data:'))
        fields.append(self.data)
        return fields

    def get_message_from_dialog(self):
        new_message = {
            'namespace': self.namespace.current_value,
            'data': self.data.text,
        }
        self.reset_values()
        return new_message

    def build_ui_message(self, data):
        message = {
            'namespace': data['namespace'],
            'data': data['data'],
        }
        return message

    def build_layer_message(self, layer, data):
        namespace = data['namespace']
        destination = self.telemetry_manager.build_telemetry_exchange_name(self.telemetry_manager.namespace_root(namespace))
        message = {
            'data': data['data'],
            'namespace': namespace,
        }
        return self.message_metadata(message, 'telmetry', 'telmetry_manager', destination, 'telmetry')

    def reset_values(self):
        self.namespace.current_value = None
        self.data.text = ''


class DebugAceTui:
    def __init__(self):
        self.style = DEFAULT_STYLE
        self.layer_numbers = [layer[len('layer_'):] for layer in self.settings.layers]
        self.debug_state = False

        self.data_dict = {layer: self.empty_data() for layer in self.settings.layers}
        self.active_layer = None
        self.active_layer_name = None
        self.active_layer_number = self.layer_numbers[0]
        self.dialog = None
        self.dialog_not_focused = Condition(lambda: self.dialog is None)
        self.current_dialog_type = None
        self.data_types = self.build_data_types()

        self.help_message = FormattedTextControl(DEFAULT_HELP_MESSAGE)
        self.help_message_height = self.help_message.text.count('\n')
        self.help_message_width = max([len(x) for x in self.help_message.text.splitlines()])
        self.log_display = ''
        self.log_display_label = Label(text='Logs:')
        self.log_display_control = FormattedTextControl(self.update_log_display)

        self.data_display = TextArea(lexer=PygmentsLexer(YamlLexer), read_only=True)
        # self.current_messages_display = TextArea(lexer=PygmentsLexer(YamlLexer), read_only=True)
        self.debug_endpoint = DebugEndpoint(constants.DEFAULT_DEBUG_UI_ENDPOINT_PORT, self.debug_endpoint_routes)
        self.debug_endpoint_url = f"http://localhost:{constants.DEFAULT_DEBUG_ENDPOINT_PORT}"
        self.kb = KeyBindings()
        self.app = Application(key_bindings=self.kb, full_screen=True, style=self.style)

        self._init_key_bindings()
        self.set_active_layer(self.active_layer_number)
        self.debug_endpoint.start_endpoint()

    @property
    def settings(self):
        return Settings(
            name="debug_tui",
            label="Debug TUI",
        )

    @property
    def debug_endpoint_routes(self):
        return {
            'post': {
                '/debug-state': self.update_layer_debug_state,
                '/layer-messages': self.update_layer_messages,
            },
        }

    def empty_data(self):
        return {
            'control': [],
            'data': [],
            'request': [],
            'response': [],
            'telemetry': [],
        }

    def build_data_types(self):
        return {
            'control': ControlDataType(self.settings),
            'data': DataDataType(self.settings),
            'request': RequestDataType(self.settings),
            'response': ResponseDataType(self.settings),
            'telemetry': TelemetryDataType(self.settings),
        }

    def update_layer_debug_state(self, data):
        layer = data['layer']
        state = data['state']
        self.add_log_entry(f"{layer} updated debug state: {state}")
        return {
            'success': True,
            'message': f"Updated debug state for layer: {layer}",
        }

    def update_layer_messages(self, data):
        layer = data['layer']
        messages = data['messages']
        for key, data_type in self.data_types.items():
            if key in messages and messages[key]:
                for message in messages[key]:
                    self.data_dict[layer][key].append(data_type.build_ui_message(message))
        self.update_output_display()
        self.add_log_entry(f"{layer} updated messages")
        return {
            'success': True,
            'message': f"Updated messages for layer: {layer}",
        }

    def toggle_debug_state(self):
        self.debug_state = not self.debug_state
        self.add_log_entry(f"Setting debug state: {'enabled' if self.debug_state else 'disabled'}")
        self.post_to_debug('toggle-debug-state', {'state': self.debug_state})

    def run_active_layer_messages(self):
        self.add_log_entry(f"Running messages for layer: {self.active_layer_name}")
        data = self.compose_active_layer_messages_data()
        self.post_to_debug('run-layer', data)

    def compose_active_layer_messages_data(self):
        layer = self.active_layer_name
        messages = {}
        for key, data_type in self.data_types.items():
            messages[key] = []
            if key in self.data_dict[layer]:
                for m in self.data_dict[layer][key]:
                    messages[key].append(data_type.build_layer_message(layer, m))
        return {
            'layer': layer,
            'messages': messages,
        }

    def get_to_debug(self, path):
        httpx.get(f"{self.debug_endpoint_url}/{path}")

    def post_to_debug(self, path, data):
        httpx.post(f"{self.debug_endpoint_url}/{path}", json=data)

    def _init_key_bindings(self):
        @self.kb.add('q', filter=self.dialog_not_focused)
        def _(event):
            self.debug_endpoint.stop_endpoint()
            event.app.exit()

        for layer in self.layer_numbers:
            self.kb.add(layer, filter=self.dialog_not_focused)(self.layer_kb_callback(layer))

        @self.kb.add('c', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("control", "Add/edit CONTROL messages")

        @self.kb.add('d', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("data", "Add DATA/edit messages")

        @self.kb.add('r', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("request", "Add/edit REQUEST messages")

        @self.kb.add('s', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("response", "Add/edit RESPONSE messages")

        @self.kb.add('t', filter=self.dialog_not_focused)
        def _(event):
            self.open_dialog("telemetry", "Add/edit TELEMETRY messages")

        @self.kb.add('b', filter=self.dialog_not_focused)
        def _(event):
            self.toggle_debug_state()

        @self.kb.add('x', filter=self.dialog_not_focused)
        def _(event):
            self.run_active_layer_messages()

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

    def open_dialog(self, key, title):
        self.current_dialog_type = self.data_types[key]
        full_title = f"{self.active_layer_name}: {title}"
        existing_messages = bool(self.data_dict[self.active_layer_name][key])
        fields = self.current_dialog_type.build_fields()
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

    def edit_dialog(self, key, index, title):
        data = self.data_dict[self.active_layer_name][key][index]
        fields = self.current_dialog_type.build_fields(data)
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
        self.data_types[key].reset_values()
        self.current_dialog_type = None
        self.update_output_display()
        self.app.layout = self.layout
        self.dialog = None

    def clear_layer(self):
        self.data_dict[self.active_layer_name] = self.empty_data()
        self.set_active_layer(self.active_layer_number)
        self.app.layout = self.layout
        self.dialog = None
        self.add_log_entry(f"Cleared messages for layer: {self.active_layer_name}")

    def add(self, key):
        new_message = self.data_types[key].get_message_from_dialog()
        self.data_dict[self.active_layer_name][key].append(new_message)
        self.update_after_change(key)
        self.add_log_entry(f"Added '{key}' message for layer: {self.active_layer_name}")

    def edit(self, key, index):
        new_message = self.data_types[key].get_message_from_dialog()
        self.data_dict[self.active_layer_name][key][index] = new_message
        self.update_after_change(key)
        self.add_log_entry(f"Edited '{key}' message {index + 1} for layer: {self.active_layer_name}")

    def update_after_change(self, key):
        self.current_dialog_type = None
        self.update_output_display()
        self.app.layout = self.layout
        self.dialog = None

    def open_message_selector(self, action):
        key = self.current_dialog_type.key
        values = [(i, yaml.dump(msg, default_flow_style=False, sort_keys=True)) for i, msg in enumerate(self.data_dict[self.active_layer_name][key])]
        radio_list = RadioList(values)

        def handler():
            index = radio_list.current_value
            if action == "edit":
                self.edit_dialog(key, index, f"Edit {key.upper()} message")
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
        self.add_log_entry(f"Deleted '{key}' message {index + 1} for layer: {self.active_layer_name}")

    def current_timestamp(self):
        return datetime.now().strftime('%H:%M:%S')

    def update_log_display(self):
        return self.log_display

    def add_log_entry(self, entry):
        log_time = self.current_timestamp()
        self.log_display = f"{log_time}: {entry}\n{self.log_display}"

    def update_output_display(self):
        text = []
        text.append(f"# ACTIVE LAYER: {self.active_layer_name.upper()}")
        text.append(yaml.dump(self.active_layer, default_flow_style=False, sort_keys=True))
        text.append("# OTHER LAYERS:")
        for layer in self.layer_numbers:
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
        self.add_log_entry(f"Switched active layer: {self.active_layer_name}")

    def cancel(self):
        self.current_dialog_type.reset_values()
        self.current_dialog_type = None
        self.app.layout = self.layout
        self.dialog = None

    def run(self):
        log_display_window = HSplit([
            self.log_display_label,
            Window(content=self.log_display_control, height=self.help_message_height),
        ])
        top_bar = VSplit([
            Window(self.help_message, width=Dimension(max=self.help_message_width)),
            log_display_window,
        ])
        body = Frame(body=HSplit([
            top_bar,
            self.data_display,
        ]))
        root_container = VSplit([body])
        self.layout = Layout(root_container)
        self.app.layout = self.layout
        self.app.run()


if __name__ == "__main__":
    DebugAceTui().run()
