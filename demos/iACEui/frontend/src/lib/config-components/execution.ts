import { get } from 'svelte/store';
import {currentLayerConfig, currentLayerName, getLayerConfig, updateBusState} from '$lib/stores/configStores';
import type { ExecuteQuery } from '$lib/config-components/configTypes';
import type {ExecuteBusResponse} from "$lib/interaction-components/chatTypes";



export type LayerMessage = {
	id: string;
	destinationBus: string;
	reasoning: string;
	message: string;
	timestamp: string;
}

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

export function ExecuteBus(layerName: string, input: string, busType: string, callback: (data: BusState) => void) {
	const config = getLayerConfig(layerName);

	if (config == null || layerName == null) {
		const msg = `Config or layer name is null. config: ${config} | layerName: ${layerName}`;
		alert(msg);
		console.error(msg);
		return;
	}

	const executeQuery: ExecuteQuery = {
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
		.then<ExecuteBusResponse>((response) => {
			if (!response.ok) {
				console.error('There was a problem with the fetch operation:', response);
				return Promise.reject('Fetch operation failed');
			}
			return response.json();
		})
		.then((data) => {
			callback({
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

// set mission /mission { "mission": "..." }
export function setMission(mission: string) {
	fetch(`http://0.0.0.0:8000/mission`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ mission: mission })
	})
		.then((response) => {
			if (!response.ok) {
				console.error('There was a problem with the fetch operation:', response);
				return Promise.reject('Fetch operation failed');
			}
			return response.json();
		});
}