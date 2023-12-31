<script lang="ts">
    import BusState from "$lib/config-components/BusState.svelte";
    import Prompt from "$lib/config-components/Prompt.svelte";
    import {onMount} from "svelte";

    import ControlStateImage from "$lib/images/control_state_img.png";
    import DataStateImage from "$lib/images/data_state_img.jpeg";
    import type {LayerConfig} from "$lib/config-components/configTypes";
    import {
        allConfigs,
        ancestralPrompt,
        currentLayerConfig,
        currentLayerName,
        getLayerConfig,
        updateLayerConfig
    } from "$lib/stores/configStores";
    import {get} from "svelte/store";
    import {
        fetchAllLayerConfigsAPI,
        fetchLayerConfigAPI, getAncestralPromptAPI, updateAncestralPromptAPI,
        updateLayerConfigAPI, updateWithCurrentLayerConfigAPI
    } from "$lib/config-components/configManagement";
    import APISettingsView from "$lib/config-components/APISettingsView.svelte";
    import {Accordion, AccordionItem, ProgressBar, ProgressRadial} from "@skeletonlabs/skeleton";

    export let layerName: string;
    export let layerBorderColor: string;

    let ancestralFetchInProgress: boolean = false;
    let configFetchInProgress: boolean = false;

    let colorControlBus = "border-[#9B5548]";
    let colorDataBus = "border-[#0F3D5C]";

    let config: LayerConfig = getLayerConfig(layerName);
    let identityPrompt: string = config.prompts.identity;
    let reasoningPrompt: string = config.prompts.reasoning;
    let controlBusPrompt: string = config.prompts.control_bus;
    let dataBusPrompt: string = config.prompts.data_bus;

    currentLayerConfig.subscribe((value) => {
        if (value == null)
            return;
        if (value.layer_name === layerName) {
            config = value;
            identityPrompt = config.prompts.identity;
            reasoningPrompt = config.prompts.reasoning;
            controlBusPrompt = config.prompts.control_bus;
            dataBusPrompt = config.prompts.data_bus;
        }
    });

    $: {
        config.prompts.identity = identityPrompt;
        config.prompts.reasoning = reasoningPrompt;
        config.prompts.control_bus = controlBusPrompt;
        config.prompts.data_bus = dataBusPrompt;

        updateLayerConfig(layerName, config);
    }
</script>

<div class="flex flex-col space-y-6">
    <!--    Layer Title -->
    <div class="w-auto h-auto flex-grow flex justify-center">
        <div class="w-[815px] h-[111px] p-5 border-b-2 {layerBorderColor} flex-col justify-center items-center gap-[15px] inline-flex">
            <div class="text-center text-neutral-400 text-[64px] font-normal font-['Fenix']">{layerName}</div>
        </div>
    </div>


    <div class="flex flex-row space-x-5">
        <Prompt size="w-[360px] min-h-[350px]" borderColor="{layerBorderColor}" placeholder="Identity Prompt"
                bind:inputValue={identityPrompt}
                title="Identity Prompt" textProps="text-[26px]"/>
        <Prompt size="w-[360px] min-h-[350px]" borderColor="{layerBorderColor}" placeholder="Reasoning Prompt"
                title="Reasoning Prompt" textProps="text-[26px]"
                bind:inputValue={reasoningPrompt}/>

        <Prompt size="w-[360px] min-h-[350px]" borderColor="{colorControlBus}" placeholder="Control Bus Prompt"
                title="Control Bus Prompt" textProps="text-[26px]"
                bind:inputValue={controlBusPrompt}/>
        <Prompt size="w-[360px] min-h-[350px]" borderColor="{colorDataBus}" placeholder="Data Bus Prompt"
                bind:inputValue={dataBusPrompt}
                title="Data Bus Prompt" textProps="text-[26px]"/>
    </div>

    <div class="flex flex-row space-x-3">
        <Prompt size="w-[360px] min-h-[350px]" borderColor="border-[#BCA77F]" placeholder="Ancestral Prompt"
                bind:inputValue={$ancestralPrompt}
                title="Ancestral Prompt" textProps="text-[30px] font-bold"/>
        <APISettingsView position="relative" borderColor={layerBorderColor}/>
        <div class="flex flex-col space-y-2 min-w-[300px]">
            <!--            Save -->
            <Accordion>
                <AccordionItem open>
                    <svelte:fragment slot="lead"></svelte:fragment>
                    <svelte:fragment slot="summary">Save</svelte:fragment>
                    <svelte:fragment slot="content">
                        <div class="btn-group variant-filled-primary">
                            <button on:click={() => updateWithCurrentLayerConfigAPI()}>Layer</button>
                            <button on:click={() => updateAncestralPromptAPI()}>Ancestral</button>
                        </div>
                    </svelte:fragment>
                </AccordionItem>
            </Accordion>
            <!--            Load -->
            <Accordion>
                <AccordionItem open>
                    <svelte:fragment slot="lead"></svelte:fragment>
                    <svelte:fragment slot="summary">Fetch</svelte:fragment>
                    <svelte:fragment slot="content">
                        <div class="flex flex-row items-center space-x-3">
                            <div class="btn-group variant-filled-primary">
                                <button on:click={() => {
                                fetchLayerConfigAPI(layerName, () => { configFetchInProgress = false; });
                                configFetchInProgress = true;
                            }}>Current
                                </button>
                                <button on:click={() => {
                                fetchAllLayerConfigsAPI(() => { configFetchInProgress = false; });
                                configFetchInProgress = true;
                            }}>All
                                </button>
                            </div>
                            {#if configFetchInProgress}
                                <ProgressRadial width={"w-6"} value={undefined}/>
                            {/if}
                        </div>
                        <div class="flex flex-row items-center space-x-3">
                            <button class="btn variant-filled-primary" on:click={() => {
                            getAncestralPromptAPI(() => { ancestralFetchInProgress = false; });
                            ancestralFetchInProgress = true; }}>Ancestral
                            </button>
                            {#if ancestralFetchInProgress}
                                <ProgressRadial width={"w-6"} value={undefined}/>
                            {/if}
                            <div/>
                        </div>
                    </svelte:fragment>

                </AccordionItem>
            </Accordion>
        </div>
    </div>


    <!--    Bus States -->
    <div class="flex flex-row space-x-4">
        <BusState busType="Control" image={ControlStateImage} borderColor="{colorControlBus}"/>
        <BusState busType="Data" image={DataStateImage} borderColor="{colorDataBus}"/>
    </div>
</div>
