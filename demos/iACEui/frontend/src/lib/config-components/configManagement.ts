import {
	defaultLayerPrompts,
	defaultLLMParams,
} from '$lib/config-components/configTypes';

import type { LayerConfig } from '$lib/config-components/configTypes';
import {
	allConfigs,
	ancestralPrompt,
	currentLayerConfig,
	getLayerConfig,
	updateLayerConfig
} from "$lib/stores/configStores";
import {get} from "svelte/store";
import {layerNames} from "$lib/utils/layers";

export function updateWithCurrentLayerConfigAPI() {
    let config = get(currentLayerConfig);
    if (config == null) {
        alert("Config is null");
        return;
    }
    updateLayerConfigAPI(config);

}

export function updateAncestralPromptAPI() {
	let prompt = get(ancestralPrompt);

	fetch(`http://0.0.0.0:8000/prompt/ancestral`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			prompt: prompt,
			is_active: true
		})
	}).then(r => {
		if (!r.ok) {
			console.error("There was a problem with the fetch operation:", r);
			return Promise.reject("Fetch operation failed");
		}
		return r.json();
	});
}

export function getAncestralPromptAPI(callback: () => void) {
	fetch(`http://0.0.0.0:8000/prompt/ancestral/active`, {
		method: 'GET',
		headers: {
			Accept: 'application/json'
		}
	}).then((response) => {

		if (!response.ok) {
			console.warn('There was a problem with the fetch operation:', response);
			return Promise.reject('Fetch operation failed');
		}
		return response.json();
	}).then((data) => {
		console.log('Received Ancestral Prompt Data:', data);
		ancestralPrompt.set(data.prompt);
		callback();
	});
}

export function updateLayerConfigAPI(config: LayerConfig) {
    console.log("Updating layer config:", config);

    fetch(`http://0.0.0.0:8000/layer/config`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config),
    })
        .then((response) => {
            if (!response.ok) {
                console.error("There was a problem with the config saving operation:", response);
                return Promise.reject("Fetch operation failed");
            }
            return response.json();
        })
        .then((data) => {
            console.log("Saved config:", data);
        })
        .catch((error) => {
            console.error("There was an error with the config saving operation:", error);
        });
}

export function fetchAllLayerConfigsAPI(callback: () => void) {
	let done = 0;

	for (const layerName of layerNames) {
		fetchLayerConfigAPI(layerName, () => {
			done++;
			if (done == layerNames.length) {
				callback();
			}
		});
	}
}

export function fetchLayerConfigAPI(layerName: string, callback: () => void) {
	fetch(`http://0.0.0.0:8000/layer/config/${encodeURIComponent(layerName)}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json'
		}
	}).then((response) => {
			if (!response.ok) {
				console.warn('There was a problem with the fetch operation:', response);
				return Promise.reject('Fetch operation failed');
			}
			return response.json();
		})
		.then((data) => {
			console.log('Received data:', data);
			updateLayerConfig(layerName, data);
			callback();
		})
		.catch((error) => {
			console.error('There was an error with the fetch operation:', error);
			const config = getLayerConfig(layerName);
            updateLayerConfigAPI(config);
			callback();
		});
}

export function createDefaultConfig(layerName: string) : LayerConfig {
    return {
			layer_name: layerName,
			config_id: null,
			llm_model_parameters: defaultLLMParams,
			prompts: defaultLayerPrompts
		};
}