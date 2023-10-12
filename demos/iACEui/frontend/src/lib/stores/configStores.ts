import { get } from 'svelte/store';
import { localStorageStore } from '@skeletonlabs/skeleton';
import type {LayerConfig, LLMParams} from '$lib/config-components/configTypes';
import type { BusState } from '$lib/config-components/execution';
import { createBusState } from '$lib/config-components/execution';
import { createDefaultConfig } from '$lib/config-components/configManagement';

export const busStates = localStorageStore<{ [key: string]: { [key: string]: BusState } }>(
	'busState',
	{}
);

export const allConfigs = localStorageStore<{[key: string]: LayerConfig}>('allConfigs', {});
export const currentLayerConfig = localStorageStore<LayerConfig | null>('currentLayerConfig', null);
export const currentLayerName = localStorageStore<string | null>('currentLayerName', "Aspirational Layer");

export const ancestralPrompt = localStorageStore<string>('ancestralPrompt', "");

export function updateBusState(layerName: string, busType: string, newBusState: BusState) {
    busStates.update((currentStates) => {
        // Deep copy
        const newStates = JSON.parse(JSON.stringify(currentStates));

        if (!newStates[layerName])
            newStates[layerName] = {};

        newStates[layerName][busType] = newBusState;
        return newStates;
    });
}

export function updateLayerConfig(layerName: string, newLayerConfig: LayerConfig) {
    allConfigs.update((currentConfigs: { [key: string]: LayerConfig }) => {
        // Deep copy
        const newConfigs = JSON.parse(JSON.stringify(currentConfigs));

        newConfigs[layerName] = newLayerConfig;

        if (layerName == get(currentLayerName))
            currentLayerConfig.set(newLayerConfig);

        return newConfigs;
    });
}

// update llm model parameters in layer config
export function updateLLMModelParameters(layerName: string, newLLMModelParameters: LLMParams) {
    allConfigs.update((currentConfigs: { [key: string]: LayerConfig }) => {
        // Deep copy
        const newConfigs = JSON.parse(JSON.stringify(currentConfigs));

        newConfigs[layerName].llm_model_parameters = newLLMModelParameters;

        if (layerName == get(currentLayerName)) {
            currentLayerConfig.set(newConfigs[layerName]);
        }

        return newConfigs;
    });
}

export function getBusState(busType: string): BusState {
	// Use the `get` function from svelte/store to get the current value of the store
	const currentStates = get(busStates);
	const layerName = get(currentLayerName);

    if (layerName == null) {
        throw new Error("Layer name is null");
    }

	if (currentStates[layerName] == null)
        currentStates[layerName] = {};
	if (currentStates[layerName][busType] == null)
		currentStates[layerName][busType] = createBusState(busType);

    return currentStates[layerName][busType];
}

// get current layer config
export function getCurrentLayerConfig(): LayerConfig {
    const layerName = get(currentLayerName);
    if (layerName == null) {
        throw new Error("Layer name is null");
    }
    return getLayerConfig(layerName);
}

export function getLayerConfig(layerName: string): LayerConfig {
    // Use the `get` function from svelte/store to get the current value of the store
    const configs = get(allConfigs);

    // Retrieve the LayerConfig for the given layerName name
    let layerConfig = configs[layerName];
    if (layerConfig == null) {
        layerConfig = createDefaultConfig(layerName);
        configs[layerName] = layerConfig;
    }
    return layerConfig;
}
