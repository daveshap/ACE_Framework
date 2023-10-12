<script lang="ts">
    import LayerSettings from "$lib/config-components/LayerSettings.svelte";

    import AspirationImage from "$lib/images/aspiration_img.png";
    import GlobalStrategyImage from "$lib/images/global_strategy_img.png";
    import AgentModelImage from "$lib/images/agent_model_img.png";
    import ExecutiveFunctionImage from "$lib/images/executive_function_img_2.png";
    import CognitiveControlImage from "$lib/images/cognitive_control_img.png";
    import TaskProsecutionImage from "$lib/images/task_prosecution_img.png";
    import {get, writable} from 'svelte/store';
    import {Tab, TabGroup} from "@skeletonlabs/skeleton";
    import {currentLayerConfig, currentLayerName, getLayerConfig} from "$lib/stores/configStores";
    import {layerNames} from "$lib/utils/layers";
    import {layerNameToBgStyle} from "$lib/graphics";

    let colors = [
        "border-[#BCA77F]",
        "border-[#428379]",
        "border-[#d38ecf]",
        "border-[#97cedc]",
        "border-[#308E9C]",
        "border-[#8d3f1d]"
    ];

    const tabSet = writable(layerNames.findIndex(name => name === get(currentLayerName)));
    let sizeActive = "w-[150px] h-[150px]";
    let sizeInactive = "w-[80px] h-[80px]";

    let bgStyle = layerNameToBgStyle();

    tabSet.subscribe(value => {
        let layerName = layerNames[value];
        currentLayerName.set(layerName);
        let config = getLayerConfig(layerName);
        currentLayerConfig.set(config);

        bgStyle = layerNameToBgStyle();
    });
</script>

<div class="h-auto w-auto" style="{bgStyle}">
    <TabGroup justify="justify-center">
        <div class="w-auto h-[150px] flex items-center justify-center">
            <Tab bind:group={$tabSet} name="Aspirational Layer" value={0} active="">
                <div class="flex flex-row items-center justify-center space-x-3">
                    <img class={`${$tabSet === 0 ? sizeActive : sizeInactive} rounded-xl transition-size`}
                         src={AspirationImage} alt=""/>
                </div>
            </Tab>
            <Tab bind:group={$tabSet} name="Global Strategy Layer" value={1} active="">
                <div class="flex flex-row items-center justify-center space-x-3">
                    <img class={`${$tabSet === 1 ? sizeActive : sizeInactive} rounded-xl transition-size`}
                         src={GlobalStrategyImage} alt=""/>
                </div>
            </Tab>
            <Tab bind:group={$tabSet} name="Agent Model Layer" value={2} active="">
                <div class="flex flex-row items-center justify-center space-x-3">
                    <img class={`${$tabSet === 2 ? sizeActive : sizeInactive} rounded-xl transition-size`}
                         src={AgentModelImage} alt=""/>
                </div>
            </Tab>
            <Tab bind:group={$tabSet} name="Executive Layer" value={3} active="">
                <div class="flex flex-row items-center justify-center space-x-3">
                    <img class={`${$tabSet === 3 ? sizeActive : sizeInactive} rounded-xl transition-size`}
                         src={ExecutiveFunctionImage} alt=""/>
                </div>
            </Tab>
            <Tab bind:group={$tabSet} name="Cognitive Control Layer" value={4} active="">
                <div class="flex flex-row items-center justify-center space-x-3">
                    <img class={`${$tabSet === 4 ? sizeActive : sizeInactive} rounded-xl transition-size`}
                         src={CognitiveControlImage} alt=""/>
                </div>
            </Tab>
            <Tab bind:group={$tabSet} name="Task Prosecution Layer" value={5} active="">
                <div class="flex flex-row items-center justify-center space-x-3">
                    <img class={`${$tabSet === 5 ? sizeActive : sizeInactive} rounded-xl transition-size`}
                         src={TaskProsecutionImage} alt=""/>
                </div>
            </Tab>
        </div>

        <svelte:fragment slot="panel">
            {#if $tabSet === 0}
                <LayerSettings layerName="Aspirational Layer" layerBorderColor="{colors[0]}"/>
            {:else if $tabSet === 1}
                <LayerSettings layerName="Global Strategy Layer" layerBorderColor="{colors[1]}"/>
            {:else if $tabSet === 2}
                <LayerSettings layerName="Agent Model Layer" layerBorderColor="{colors[2]}"/>
            {:else if $tabSet === 3}
                <LayerSettings layerName="Executive Layer" layerBorderColor="{colors[3]}"/>
            {:else if $tabSet === 4}
                <LayerSettings layerName="Cognitive Control Layer" layerBorderColor="{colors[4]}"/>
            {:else if $tabSet === 5}
                <LayerSettings layerName="Task Prosecution Layer" layerBorderColor="{colors[5]}"/>
            {/if}
        </svelte:fragment>
    </TabGroup>

</div>

<style>
    .transition-size {
        transition: width 0.3s ease-in-out, height 0.3s ease-in-out;
    }

    :global(.aspirational-layer-bg) {
        background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #C9A86D 0%, #FDD182 10.96%, rgba(254, 226, 175, 0.25) 35.04%, rgba(254, 235, 200, 0.06) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;
    }

    :global(.global-strategy-layer-bg) {
        background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #58A19A 0%, #7CB3B5 10.96%, rgba(88, 161, 154, 0.3) 35.04%, rgba(88, 161, 154, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;
    }

    :global(.agent-model-layer-bg) {
        background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #E3A2E3 0%, #E9B2E9 10.96%, rgba(227, 162, 227, 0.3) 35.04%, rgba(227, 162, 227, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;
    }

    :global(.executive-layer-bg) {
        background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #A8E0E8 0%, #B2E5ED 10.96%, rgba(168, 224, 232, 0.3) 35.04%, rgba(168, 224, 232, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;
    }

    :global(.cognitive-control-layer-bg) {
        background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #4AB0B9 0%, #5FBCC5 10.96%, rgba(74, 176, 185, 0.3) 35.04%, rgba(74, 176, 185, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;
    }

    :global(.task-prosecution-layer-bg) {
        background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #A45534 0%, #B06642 10.96%, rgba(164, 85, 52, 0.3) 35.04%, rgba(164, 85, 52, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;
    }

</style>