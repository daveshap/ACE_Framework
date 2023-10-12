<script lang="ts">
    import Prompt from "$lib/config-components/Prompt.svelte";
    import SemanticPairView from "$lib/interaction-components/SemanticPairView.svelte";
    import {
        createSemanticPair,
        semanticGatesStore,
        semanticPairsStore
    } from "$lib/interaction-components/semanticGates";

    let newPairKey: string;

    let gateName: string;
    let gateDescription: string;

    function addPair() {
        createSemanticPair(newPairKey);
    }

    function addGate() {
        semanticGatesStore.update(gates => {
            gates.push({
                name: "New Gate",
                options: $semanticPairsStore.map(pair => pair),
                description: "A new gate",
            });
            return gates;
        });
    }

</script>

<div class="border-2 border-primary-400 rounded-2xl p-2 space-y-1 w-[600px]">
    <div class="flex flex-row space-x-3">
        <Prompt title="Name" size="h-[50px] w-[160px]" bind:inputValue={gateName}/>
        <Prompt title="Description" size="h-[100px] w-[180px]" bind:inputValue={gateDescription}/>
        <button class="btn variant-filled-primary w-min h-min" on:click={addGate}>Save</button>
    </div>

    <span class="text-primary-400 text-lg">Semantic Pairs</span>
    <div class="flex flex-row space-x-2">
        <Prompt size="h-[50px] w-[160px]" placeholder="Enter a key" bind:inputValue={newPairKey}/>
        <button class="btn variant-filled-primary" on:click={addPair}>➕</button>
    </div>
    <div class="flex flex-col space-y-2">
        {#each $semanticPairsStore as pair (pair.key)}
            <SemanticPairView key={pair.key}/>
        {/each}
    </div>
</div>
