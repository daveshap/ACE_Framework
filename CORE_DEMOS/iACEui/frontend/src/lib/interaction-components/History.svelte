<script lang="ts">
    import LayerHistoryViewCard from "$lib/interaction-components/LayerHistoryViewCard.svelte";
    import type {LayerHistoryData} from "$lib/interaction-components/chatTypes";
    import {Accordion, localStorageStore} from "@skeletonlabs/skeleton";
    import Prompt from "$lib/config-components/Prompt.svelte";
    import {ExecuteBus} from "$lib/config-components/execution";
    import {
        compareSemantics,
        findSemanticGate,
        findSemanticPair,
        semanticGatesStore
    } from "$lib/interaction-components/semanticGates";
    import {layerNames} from "$lib/utils/layers";


    let inputPrompt = localStorageStore("inputPrompt", "");

    let layer: string = "Global Strategy Layer";
    let historyData: LayerHistoryData[];

    let currentLayerData: LayerHistoryData;

    let inProgress = false;

    let controlBusDecision: boolean;
    let dataBusDecision: boolean;

    let controlRejectionEmbedding = findSemanticPair("control bus rejection")!.embedding;
    let dataRejectionEmbedding = findSemanticPair("data bus rejection")!.embedding;
    let controlAcceptanceEmbedding = findSemanticPair("control bus accept")!.embedding;
    let dataAcceptanceEmbedding = findSemanticPair("data bus accept")!.embedding;

    async function mapDecision(input: string)
    {
        // use compareSemantics to compare input with each of the four embeddings
        // return the decision that is most similar to the input
        let controlRejectionSimilarity = await compareSemantics(input, controlRejectionEmbedding);
        let dataRejectionSimilarity = await compareSemantics(input, dataRejectionEmbedding);
        let controlAcceptanceSimilarity = await compareSemantics(input, controlAcceptanceEmbedding);
        let dataAcceptanceSimilarity = await compareSemantics(input, dataAcceptanceEmbedding);

        let maxSimilarity = Math.max(controlRejectionSimilarity, dataRejectionSimilarity, controlAcceptanceSimilarity, dataAcceptanceSimilarity);

    }

</script>

<div class="flex justify-center w-full pt-2">

    <div class="flex flex-row items-start space-x-2">
        <Prompt
                textProps="text-neutral-500 text-[22px] text-center"
                placeholder="Enter your prompt here"
                size="w-[420px] min-h-[228px]"
                borderColor={`border-neutral-500`}
                bind:inputValue={$inputPrompt}
        />
        <button class="btn variant-filled-surface" disabled={inProgress} on:click={() => {

             ExecuteBus(layerNames[0], $inputPrompt, "Control", (data) => {

                if (currentLayerData == null)
                {
                    historyData = [];
                }
                else
                {
                    historyData.push(currentLayerData);
                }
                currentLayerData = {
                   id: historyData.length,
                   controlInput: data.input,
                   reasoning: data.reasoningResult,

                   controlOutput: data.controlResult,
                   dataOutput: data.dataResult,

                   dataInput: "",
                };

               inProgress = false;
            });


            inProgress = true;
        }}>Submit
        </button>

        <button class="btn variant-filled-primary" on:click={() => {
            if (!currentLayerData.dataOutput.includes("none"))
            {
                ExecuteBus(layerNames[1], currentLayerData.dataInput, "Data", (data) => {
                    currentLayerData.dataOutput = data.dataResult;
                });
            }

        }}>Proceed</button>

    </div>

    {#if currentLayerData}
        <LayerHistoryViewCard layerName="{layer}" data={currentLayerData}/>
    {/if}
    <!--{#each historyData as data}-->
    <!--        <LayerHistoryViewCard layerName="{layer}" data={data}/>-->
    <!--    {/each}-->
</div>
