<script lang="ts">
    import DataControlBox from "$lib/interaction-components/DataControlBox.svelte";
    import ImageButton from "$lib/config-components/ImageButton.svelte";

    import AspirationImage from "$lib/images/aspiration_img.png";
    import GlobalStrategyImage from "$lib/images/global_strategy_img.png";
    import AgentModelImage from "$lib/images/agent_model_img.png";
    import ExecutiveFunctionImage from "$lib/images/executive_function_img_2.png";
    import CognitiveControlImage from "$lib/images/cognitive_control_img.png";
    import TaskProsecutionImage from "$lib/images/task_prosecution_img.png";

    import {layerNames} from "$lib/utils/layers";
    import Prompt from "$lib/config-components/Prompt.svelte";
    import type {LayerHistoryData} from "$lib/interaction-components/chatTypes";

    export let data: LayerHistoryData;
    export let layerName: string;

    let belowLayerName: string;
    let topLayerName: string;


    setPrevAndNextLayerNames();

    function setPrevAndNextLayerNames(): void {
        const index = layerNames.indexOf(layerName);
        const len = layerNames.length;

        topLayerName = layerNames[(index - 1 + len) % len];
        belowLayerName = layerNames[(index + 1) % len];
    }

    function getImageForLayerName(layerName: string): string {
        switch (layerName) {
            case "Aspirational Layer":
                return AspirationImage;
            case "Global Strategy Layer":
                return GlobalStrategyImage;
            case "Agent Model Layer":
                return AgentModelImage;
            case "Executive Layer":
                return ExecutiveFunctionImage;
            case "Cognitive Control Layer":
                return CognitiveControlImage;
            case "Task Prosecution Layer":
                return TaskProsecutionImage;
            default:
                return "";
        }
    }

    function getBorderColorForLayerName(layerName: string): string {
        switch (layerName) {
            case "Aspirational Layer":
                return "#BCA77F";
            case "Global Strategy Layer":
                return "#428379";
            case "Agent Model Layer":
                return "#d38ecf";
            case "Executive Layer":
                return "#97cedc";
            case "Cognitive Control Layer":
                return "#308E9C";
            case "Task Prosecution Layer":
                return "#8d3f1d";
            default:
                return "";
        }
    }


</script>

<div class="flex flex-col items-center space-y-[34px]">
    {#if layerName !== layerNames[0]}
        <ImageButton
                image={getImageForLayerName(topLayerName)}
                topCaption="top layer"
                borderColor={`border-[${getBorderColorForLayerName(topLayerName)}]`}
                clicked={(e) => console.log("Button clicked" + e)}
        />
    {/if}

    <div class="flex flex-row space-x-10 w-max justify-start">
        {#if data.dataInput !== ""}
        <DataControlBox
                type="control"
                title="control input"
                size="w-[320px] min-h-[160px]"
                inputValue={data.controlInput}
        />
        {/if}
        {#if data.dataOutput !== ""}
        <DataControlBox
                type="data"
                title="data output"
                size="w-[320px] min-h-[160px]"
                inputValue={data.dataOutput}
        />
        {/if}
    </div>

    <div class="flex flex-row items-center space-x-10">
        <span class="text-neutral-500 text-[32px] text-start font-['Fenix']">{layerName}</span>
        <ImageButton
                size="w-[200px] w-[200px]"
                image={getImageForLayerName(layerName)}
                borderColor={`border-[${getBorderColorForLayerName(layerName)}]`}
                clicked={(e) => console.log("Button clicked" + e)}
        />
        {#if data.reasoning !== ""}
        <Prompt
                textProps="text-neutral-500 text-[22px] text-start"
                title="reasoning"
                size="w-[320px] min-h-[160px]"
                borderColor={`border-[${getBorderColorForLayerName(layerName)}]`}
        />
        {/if}
    </div>

    <div class="flex flex-row space-x-10 w-max justify-start">

        {#if data.controlOutput !== ""}
        <DataControlBox
                type="control"
                title="control output"
                size="w-[320px] min-h-[160px]"
                inputValue={data.controlOutput}
        />
        {/if}
        {#if data.dataInput !== ""}
        <DataControlBox
                type="data"
                title="data input"
                size="w-[320px] min-h-[160px]"
                inputValue={data.dataInput}
        />
        {/if}

    </div>

    <!--    <div class="flex justify-center">-->
    {#if layerName !== layerNames[layerNames.length - 1]}
        <ImageButton
                image={getImageForLayerName(belowLayerName)}
                topCaption="bottom layer"
                borderColor={`border-[${getBorderColorForLayerName(belowLayerName)}]`}
                clicked={(e) => console.log("Button clicked" + e)}
        />
    {/if}

</div>

