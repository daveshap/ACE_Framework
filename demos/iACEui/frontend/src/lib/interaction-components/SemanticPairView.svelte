<script lang="ts">

    import Prompt from "$lib/config-components/Prompt.svelte";
    import type {SemanticPair} from "$lib/interaction-components/semanticGates";
    import {clipboard} from '@skeletonlabs/skeleton';
    import {
        createEmbedding,
        createSemanticPair,
        findSemanticPair, semanticPairsStore,
        updateSemanticPair
    } from "$lib/interaction-components/semanticGates";
    import ScrollableText from "$lib/interaction-components/ScrollableText.svelte";

    export let key: string;

    let params: SemanticPair = findSemanticPair(key) ?? createSemanticPair(key);

    let inputText: string = params.text;
    let binding: string = params.binding;
    let embedding = params.embedding;
    let embeddingString: string = JSON.stringify(embedding);

    console.log(params);

    function embed() {
        createEmbedding(params.text).then(e => embedding = e);
    }

    $: {
        params.text = inputText;
        params.binding = binding;
        params.embedding = embedding;

        embeddingString = JSON.stringify(embedding);
        updateSemanticPair(params.key, params);
    }

</script>

<div class="flex flex-col space-y-3 border-2 border-green-700 rounded-2xl p-4 max-w-md">
    <div class="flex flex-row justify-between">
        <div class={`h-[30px] text-center text-neutral-400 text-2xl font-['Fenix']`}>{params.key}</div>
        <button class="btn-icon variant-filled-secondary" on:click={() => {
             semanticPairsStore.update(items =>{
                 return items.filter(item => {
                 console.log(item.key, params.key);
                 const del = item.key !== params.key;
                    if (!del) {
                        console.log("deleting", item.key);
                    }
                    return del;
                 });
             });
             console.log($semanticPairsStore);
        }}>🗑️
        </button>
    </div>

    <div class="flex flex-row space-x-3">
        <Prompt size="h-20 w-200" borderColor="border-primary-500" bind:inputValue={inputText}
                placeholder="Semantic pattern:"/>
        <Prompt size="h-20 w-200" borderColor="border-primary-500" bind:inputValue={binding} placeholder="Binding:"/>
    </div>
    <div class="flex flex-row space-x-3 max-h-16">
        <button class="btn variant-filled-secondary" on:click={embed}>Embedding {params.embedding.length === 0 ? "🔄" : "👌"}</button>
        <button class="btn variant-filled-secondary w-max" use:clipboard={embeddingString}>📋</button>
        <ScrollableText text={embeddingString} maxWidth="w-1/2" color="text-neutral-400"/>
    </div>
</div>
