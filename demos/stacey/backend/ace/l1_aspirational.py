# ace/l1_aspirational.py

import ace.l1_aspirational_prompts as prompts
from .ace_layer import AceLayer


class L1AspirationalLayer(AceLayer):
    def __init__(self):
        super().__init__("1")

    def get_consitution(self):
        return prompts.constitution

