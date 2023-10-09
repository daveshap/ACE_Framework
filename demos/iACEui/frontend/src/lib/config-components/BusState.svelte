<script lang="ts">
    import InputField from "$lib/config-components/Prompt.svelte";
    import APISettingsView from "$lib/config-components/APISettingsView.svelte";
    import ImageButton from "$lib/config-components/ImageButton.svelte";
    import {onMount} from "svelte";
    import {ExecuteBus} from "$lib/config-components/execution";
    import type {BusState} from "$lib/config-components/execution";
    import {busStates, currentLayerName, getBusState, updateBusState} from "$lib/stores/configStores";
    import {get} from "svelte/store";

    export let busType: string;
    export let image: string;
    export let borderColor: string;

    let layerName: string = $currentLayerName!;
    let busState: BusState = getBusState(busType);

    let inputStateValue: string = busState.input;
    let reasoningStateValue: string = busState.reasoningResult;
    let controlBusMessage: string = busState.controlResult;
    let dataBusMessage: string = busState.dataResult;

    busStates.subscribe((value) => {
        let b = value[layerName][busType];
        inputStateValue = b.input;
        reasoningStateValue = b.reasoningResult;
        controlBusMessage = b.controlResult;
        dataBusMessage = b.dataResult;
    });

    $: {
        busState.input = inputStateValue;
        busState.reasoningResult = reasoningStateValue;
        busState.controlResult = controlBusMessage;
        busState.dataResult = dataBusMessage;

        updateBusState(layerName, busType, busState);
    }

</script>

<div class="card w-[750px] h-auto p-4 flex flex-col items-center {borderColor} border-2 rounded-[20px]">
    <!--    Title -->
    <div class="flex pb-1 mb-1 items-center justify-center text-center relative">
        <span class="text-center text-neutral-400 text-3xl font-normal font-['Fenix'] inline-block relative px-2">
            {busType} Bus State
            <span class="absolute inset-x-0 bottom-0 border-b {borderColor}"></span>
        </span>
    </div>

    <div class="flex flex-row">
        <div class="flex flex-col space-y-5">

            <div class="flex flex-row h-auto">
                <InputField bind:inputValue={inputStateValue} borderColor="{borderColor}" size="w-[260px] min-h-[300px]"
                            title="Input"/>
                <div class="flex flex-col items-center">
                    <ImageButton image={image} borderColor="{borderColor}" caption={"open full view"}
                                 clicked={() => console.log("test full view open !")}/>
                    <div class="btn-group-vertical button-primary {borderColor} border-[3px] rounded-[10px] w-32">
                        <button on:click={() => { ExecuteBus(inputStateValue, busType)} }>Execute</button>
                        <button>History</button>
                    </div>
                </div>
            </div>


        </div>

        <div class="ReasoningAction flex flex-col space-y-10">
            <InputField bind:inputValue={reasoningStateValue} borderColor="{borderColor}" size="w-[260px] min-h-[200px]"
                        title="Reasoning"/>
            <InputField bind:inputValue={controlBusMessage} borderColor="{borderColor}" size="w-[260px] min-h-[200px]"
                        title="Control Bus Message"/>
            <InputField bind:inputValue={dataBusMessage} borderColor="{borderColor}" size="w-[260px] min-h-[200px]"
                        title="Data Bus Message"/>
        </div>
    </div>
</div>
