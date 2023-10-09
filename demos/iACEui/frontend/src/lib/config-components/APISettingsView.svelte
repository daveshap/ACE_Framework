<script lang="ts">
    import {RangeSlider} from '@skeletonlabs/skeleton';
    import {Accordion, AccordionItem} from '@skeletonlabs/skeleton';
    import type {LLMParams} from "$lib/config-components/configTypes";

    import {
        currentLayerConfig,
        currentLayerName,
        getCurrentLayerConfig,
        updateLLMModelParameters
    } from "$lib/stores/configStores";

    export let position: string = "absolute 50% 50%";
    export let borderColor: string = "border-primary-500";

    let layerName = $currentLayerName!;

    let params: LLMParams;
    let model: string;
    let temperature: number;
    let maxTokens: number;
    let topP: number;
    let presencePenalty: number;
    let frequencyPenalty: number;

    currentLayerConfig.subscribe((value) => {
        if (value?.layer_name == null || layerName !== value.layer_name) {
            return;
        }

        let p = getCurrentLayerConfig().llm_model_parameters;
        if (p.model == params?.model && p.temperature == params?.temperature && p.max_tokens == params?.max_tokens && p.top_p == params?.top_p && p.presence_penalty == params?.presence_penalty && p.frequency_penalty == params?.frequency_penalty) {
            return;
        }
        params = p;
        model = params.model;
        temperature = params.temperature;
        maxTokens = params.max_tokens;
        topP = params.top_p;
        presencePenalty = params.presence_penalty;
        frequencyPenalty = params.frequency_penalty;
        // params = value.llm_model_parameters;
        // model = params.model;
        // temperature = params.temperature;
        // maxTokens = params.max_tokens;
        // topP = params.top_p;
        // presencePenalty = params.presence_penalty;
        // frequencyPenalty = params.frequency_penalty;
    });

    $: {
        params.model = model;
        params.temperature = temperature;
        params.max_tokens = maxTokens;
        params.top_p = topP;
        params.presence_penalty = presencePenalty;
        params.frequency_penalty = frequencyPenalty;

        updateLLMModelParameters(layerName, params);
    }

</script>

<div class=" p-3 space-y-3 {position} border-2 rounded-[20px] {borderColor} font-['Goldman'] w-[250px]">
    <label class="label">
        <span>Model</span>
        <select class="select" bind:value={model}>
            <option value="gpt-4-0613">gpt-4</option>
            <option value="gpt-3.5-turbo-16k-0613">gpt-3.5-turbo</option>
            <option value="gpt-3.5-turbo-instruct">gpt-3.5-turbo-instruct</option>
            <option value="gpt-3.5-turbo-0613">gpt-3.5-turbo</option>
        </select>
    </label>

    <!--    background to range slider-->

    <RangeSlider class="" name="range-slider" bind:value={temperature} max={1.0} step={0.1}>
        <div class="flex justify-between items-center">
            <div class="font-">Temperature</div>
            <div class="text-xs">{temperature}</div>
        </div>
    </RangeSlider>

    <!--    max tokens range slider-->

    <RangeSlider class="" name="range-slider" bind:value={maxTokens} max={2048} step={16}>
        <div class="flex justify-between items-center">
            <div class="font-">Max Tokens</div>
            <div class="text-xs">{maxTokens}</div>
        </div>
    </RangeSlider>

    <Accordion>
        <AccordionItem>
            <svelte:fragment slot="summary">
                <div class="text-gray-300">Extra settings</div>
            </svelte:fragment>
            <svelte:fragment slot="content">
                <RangeSlider class="" name="range-slider" bind:value={presencePenalty} max={2.0} step={0.1}>
                    <div class="flex justify-between items-center">
                        <div class="font-">Presence Penalty</div>
                        <div class="text-xs">{presencePenalty}</div>
                    </div>
                </RangeSlider>

                <RangeSlider class="" name="range-slider" bind:value={frequencyPenalty} max={2.0} step={0.1}>
                    <div class="flex justify-between items-center">
                        <div class="font-">Frequency Penalty</div>
                        <div class="text-xs">{frequencyPenalty}</div>
                    </div>
                </RangeSlider>

                <RangeSlider class="" name="range-slider" bind:value={topP} max={1.0} step={0.1}>
                    <div class="flex justify-between items-center">
                        <div class="font-">Top-p</div>
                        <div class="text-xs">{topP}</div>
                    </div>
                </RangeSlider>
            </svelte:fragment>
        </AccordionItem>

    </Accordion>

</div>
