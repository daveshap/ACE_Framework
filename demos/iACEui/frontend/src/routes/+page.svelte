<script lang="ts">
    import {AppRail, AppRailAnchor, AppRailTile} from "@skeletonlabs/skeleton";
    import Layers from "$lib/config-components/Layers.svelte";

    let currentTile: number = 0;
</script>

<div class="flex flex-row justify-between">
    <AppRail>
        <AppRailTile bind:group={currentTile} name="tile-1" value={0} title="tile-1">
            <span>Layers</span>
        </AppRailTile>
        <AppRailTile bind:group={currentTile} name="tile-2" value={1} title="tile-2">
            <span>Logs</span>
        </AppRailTile>
        <AppRailTile bind:group={currentTile} name="tile-3" value={2} title="tile-3">
            <span>Chat</span>
        </AppRailTile>
    </AppRail>

    <div class="grid place-content-center place-items-center">
        {#if currentTile === 0}
            <Layers />
        {/if}
        {#if currentTile === 1}
            <h1>Tile 2</h1>
        {/if}
    </div>
</div>



