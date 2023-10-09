import { get } from 'svelte/store';
import {currentLayerConfig, currentLayerName, updateBusState} from '$lib/stores/configStores';
import type { ExecuteQuery } from '$lib/config-components/configTypes';

export type BusState = {
	busType: string;
	input: string;
	reasoningResult: string;
	controlResult: string;
	dataResult: string;
};

export function createBusState(busType: string): BusState {
	return {
		busType: busType,
		input: '',
		reasoningResult: '',
		controlResult: '',
		dataResult: ''
	};
}

export function ExecuteBus(input: string, busType: string) {
	let config = get(currentLayerConfig);
	let layerName = get(currentLayerName);

	if (config == null || layerName == null) {
		let msg = `Config or layer name is null. config: ${config} | layerName: ${layerName}`;
		alert(msg);
		console.error(msg);
		return;
	}

	let executeQuery: ExecuteQuery = {
		layer_name: layerName,
		llm_model_parameters: config.llm_model_parameters,
		llm_messages: [],
		prompts: config.prompts,
		input: input,
		source_bus: busType
	};

	console.log('Executing query:', executeQuery);

	fetch('http://0.0.0.0:8000/layer/test', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(executeQuery)
	})
		.then((response) => {
			if (!response.ok) {
				console.error('There was a problem with the fetch operation:', response);
				return Promise.reject('Fetch operation failed');
			}
			return response.json();
		})
		.then((data) => {
			updateBusState(layerName!, busType, {
				input: input,
				busType: busType,
				reasoningResult: data.reasoning_result.content,
				controlResult: data.control_bus_action.content,
				dataResult: data.data_bus_action.content
			});
			console.log('Successfully executed query:', data);
		})
		.catch((error) => {
			console.error('There was an error with the fetch operation:', error);
		});
}
