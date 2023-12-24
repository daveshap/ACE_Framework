import os


def get_template_dir():
    return os.path.join(os.path.dirname(__file__), "prompts/templates")


def get_identities_dir():
    return os.path.join(os.path.dirname(__file__), "prompts/identities")
