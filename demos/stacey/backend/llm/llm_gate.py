
import json
from collections import deque
from threading import Timer
from typing import List, Any, Optional, Callable, Dict


class GPT:
    def __init__(self, api_key):
        self.api_key = api_key

    # noinspection PyUnusedLocal
    def create_chat_completion(self, model, prompt, inputs) -> str:
        # Simulating GPT-3.5 chat completion
        # In real-world applications, you'll call the OpenAI API here
        return f"GPT-3.5 processed: {prompt} with inputs {inputs}"


class LLMGate:
    def __init__(self,
                 inputs: List[str],
                 api_key: str,
                 model: str = "text-davinci-002",
                 timer: Optional[int] = None,
                 trigger_condition: Optional[Callable] = None,
                 memory_capacity: Optional[int] = None,
                 memory_labeling: Optional[Dict[str, Any]] = None,
                 category_label: Optional[str] = None,
                 operation: Optional[str] = None,
                 input_weights: Optional[Dict[str, float]] = None):
        self.inputs = inputs
        self.processor = GPT(api_key)
        self.model = model
        self.timer = timer
        self.trigger_condition = trigger_condition
        self.memory = deque(maxlen=memory_capacity) if memory_capacity else None
        self.memory_labeling = memory_labeling
        self.category_label = category_label
        self.operation = operation
        self.input_weights = input_weights
        self.operation_queue = deque()

        if self.timer:
            self._init_timer()

    def _init_timer(self):
        self.timer_thread = Timer(self.timer, self.process)
        self.timer_thread.start()

    def update_inputs(self, new_inputs: List[str]):
        self.inputs = new_inputs

    def update_operation(self, new_operation: str):
        self.operation = new_operation

    def add_to_memory(self, item: str, vector_storage: bool = False):
        if self.memory is not None:
            if vector_storage:
                item = json.dumps({"vector": item})
            self.memory.append(item)

    def process(self):
        if self.trigger_condition and not self.trigger_condition():
            return "Trigger condition not met"

        weighted_inputs = self._apply_weights()
        output = self.processor.create_chat_completion(self.model, self.operation, weighted_inputs)
        self.add_to_memory(output)
        return output

    def _apply_weights(self) -> List[str]:
        if not self.input_weights:
            return self.inputs

        weighted_inputs = []
        for inp in self.inputs:
            weight = self.input_weights.get(inp, 1)
            weighted_inputs.extend([inp] * int(weight))
        return weighted_inputs

    def add_operation_to_queue(self, operation: str):
        self.operation_queue.append(operation)

    def process_queue(self):
        while self.operation_queue:
            self.update_operation(self.operation_queue.popleft())
            self.process()

    def communicate(self, other_gate):
        if self.category_label == other_gate.category_label:
            pass  # Actual communication logic here

    def communicate_external(self, external_system):
        pass  # Actual communication logic here
