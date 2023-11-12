export const defaultLLMParams: LLMParams = {
	model: "gpt-4-0613",
	temperature: 0,
	max_tokens: 512,
	top_p: 1,
	frequency_penalty: 0,
	presence_penalty: 0,
};

export const defaultLayerPrompts: LayerPrompts = {
	identity: "",
	reasoning: "",
	data_bus: "",
	control_bus: "",
};

export type LLMParams = {
	model: string;
	temperature: number;
	max_tokens: number;
	top_p: number;
	frequency_penalty: number;
	presence_penalty: number;
}

export type LayerConfig = {
	layer_name: string;
	config_id: string | null;
	prompts: LayerPrompts;
	llm_model_parameters: LLMParams;
}

export type LayerPrompts = {
	identity: string;
	reasoning: string;
	data_bus: string;
	control_bus: string;
}

export type ExecuteQuery = {
	layer_name: string,
	input: string,
	source_bus: string,
	prompts: LayerPrompts;
	llm_messages: Array<{
		role: string;
		content: string;
	}>;
	llm_model_parameters: LLMParams;
}
