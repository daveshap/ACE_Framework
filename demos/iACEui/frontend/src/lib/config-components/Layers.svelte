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

    tabSet.subscribe(value => {
        let layerName = layerNames[value];
        currentLayerName.set(layerName);
        let config = getLayerConfig(layerName);
        currentLayerConfig.set(config);
    });
</script>

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
            <LayerSettings layerName="Aspirational Layer" layerBorderColor="{colors[0]}" />
        {:else if $tabSet === 1}
            <LayerSettings layerName="Global Strategy Layer" layerBorderColor="{colors[1]}" />
        {:else if $tabSet === 2}
            <LayerSettings layerName="Agent Model Layer" layerBorderColor="{colors[2]}" />
        {:else if $tabSet === 3}
            <LayerSettings layerName="Executive Layer" layerBorderColor="{colors[3]}" />
        {:else if $tabSet === 4}
            <LayerSettings layerName="Cognitive Control Layer" layerBorderColor="{colors[4]}" />
        {:else if $tabSet === 5}
            <LayerSettings layerName="Task Prosecution Layer" layerBorderColor="{colors[5]}" />
        {/if}
    </svelte:fragment>
</TabGroup>

<style>
    .transition-size {
        transition: width 0.3s ease-in-out, height 0.3s ease-in-out;
    }
</style>