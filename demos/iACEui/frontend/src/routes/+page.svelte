<script lang="ts">
    import {AppRail, AppRailTile, localStorageStore} from "@skeletonlabs/skeleton";
    import Layers from "$lib/config-components/Layers.svelte";
    import LayerHistoryViewCard from "$lib/interaction-components/LayerHistoryViewCard.svelte";
    import CompareSemanticsView from "$lib/interaction-components/CompareSemanticsView.svelte";
    import History from "$lib/interaction-components/History.svelte";

    let currentTile = localStorageStore("currentTile", 0);
</script>

<div class="flex flex-row justify-between">
    <AppRail>
        <AppRailTile bind:group={$currentTile} name="tile-1" value={0} title="tile-1">
            <span>Layers</span>
        </AppRailTile>
        <AppRailTile bind:group={$currentTile} name="tile-2" value={1} title="tile-2">
            <span>Messages</span>
        </AppRailTile>
        <AppRailTile bind:group={$currentTile} name="tile-3" value={2} title="tile-3">
            <span>Semantic gates</span>
        </AppRailTile>
    </AppRail>

    <div class="grid w-full">
        {#if $currentTile === 0}
            <Layers/>
        {/if}
        {#if $currentTile === 1}
            <History />
        {/if}
        {#if $currentTile === 2}
            <CompareSemanticsView/>
        {/if}
    </div>
</div>



