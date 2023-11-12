<script lang="ts">

import Prompt from "$lib/config-components/Prompt.svelte";
import {compareSemantics,  semanticGatesStore} from "$lib/interaction-components/semanticGates";
import type {SemanticGate} from "$lib/interaction-components/semanticGates";
import {get} from "svelte/store";
import {Autocomplete } from "@skeletonlabs/skeleton";
import type {AutocompleteOption } from "@skeletonlabs/skeleton";
import SemanticGateView from "$lib/interaction-components/SemanticGateView.svelte";

let a = "";
let b = "";
let similarity: number;

let allGates: SemanticGate[] = get(semanticGatesStore);
let chosenGates: SemanticGate[] = [];

let autocompleteOptions: AutocompleteOption<string>[] = allGates.map((gate) => {
    return {
        label: gate.name,
        value: gate.name
    }
});

function onSelection(event: CustomEvent<AutocompleteOption<string>>): void {
    if (event.detail.value === "create") {
        semanticGatesStore.update((values) => {

            return values;
        });
        return;
    }
    let selected = allGates.find((gate) => gate.name === event.detail.value);
    if (!selected) {
        return;
    }
    chosenGates.push(selected);
}


</script>


<SemanticGateView />

<div class="Comparison flex flex-col justify-center items-center">
    <div class="">Comparison</div>
    <div class="flex flex-row">
        <Prompt title="A" size="min-h-[200px] min-w-[100px]" textProps="1.5rem" bind:inputValue={a} placeholder={"Compare me with B"} />
        <Prompt title="B" size="min-h-[200px] min-w-[100px]" textProps="1.5rem" bind:inputValue={b} placeholder={"Compare me with A"} />
    </div>
    Similarity: {similarity}
    <button class="btn btn-variant-filled" on:click={() => {
        compareSemantics(a, b).then((sim) => {
            similarity = sim;
        });
    }}>
        Compare
    </button>
</div>