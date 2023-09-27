{

  "Prompts": {

    "System": {
      "vars": [],
      "template": "You are an ACE Framework orchestration module responsible for coordinating the layers to achieve aligned cognition."
    },

    "OrchestrateLayers": {
      "vars": ["layer_sequences", "layer_data"],
      "template": "Orchestrate the layers based on provided configs. Return a structured YAML output detailing the orchestration workflow.",

      "examples": [
        "orchestration_log:",
        "  - step: 1",
        "    layer: Aspirational",
        "    prompt: Initialize",
        "    params: ",
        "      constitution: \"ethical constitution content\"",
        "      objectives: \"top level objectives\"",
        "",
        "  - step: 2",
        "    layer: GlobalStrategy ",
        "    prompt: IngestSensors",
        "    params:",
        "      sensor_data: \"streaming sensor feeds\"",
        "",
        "  # etc..."
      ]
    }

  }

}