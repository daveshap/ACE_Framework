import OpenAI from "openai";
import {localStorageStore} from "@skeletonlabs/skeleton";
import * as math from 'mathjs';
import {get} from "svelte/store";

const openai = new OpenAI({apiKey: "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", dangerouslyAllowBrowser: true});

export const semanticPairsStore = localStorageStore<SemanticPair[]>("semanticPairs", []);
export const semanticGatesStore = localStorageStore<SemanticGate[]>("semanticGates", []);

// update semantic pair in semantic pairs
export function updateSemanticPair(key: string, newSemanticPair: SemanticPair) {
    semanticPairsStore.update((pairs) => {
        const newPairs = [...pairs];
        const index = newPairs.findIndex((pair) => pair?.key === key);
        newPairs[index] = newSemanticPair;

        return newPairs;
    });
}

export function findSemanticPair(key: string): SemanticPair | undefined {
    return get(semanticPairsStore)?.find((pair) => pair?.key === key);
}

export function findSemanticGate(name: string): SemanticGate | undefined {
    return get(semanticGatesStore)?.find((gate) => gate.name === name);
}

// create semantic pair with key
export function createSemanticPair(key: string): SemanticPair {
    const params: SemanticPair = {
        key: key,
        text: "",
        embedding: [],
        binding: "",
    };
    semanticPairsStore.update(pairs => {
        pairs.push(params);
        return pairs;
    });

    return params;

}

export type SemanticPair = {
    key: string,
    text: string,
    embedding: number[],
    binding: string,
}

export type SemanticGate = {
    name: string,
    description: string,
    options: SemanticPair[],
}

export const putMessageToControlBus = localStorageStore<number[]>("putMessageToControlBus", []);
export const putMessageToDataBus = localStorageStore<number[]>("putMessageToDataBus", []);
export const doNotPutMessageToControlBus = localStorageStore<number[]>("doNotPutMessageToControlBus", []);
export const doNotPutMessageToDataBus = localStorageStore<number[]>("doNotPutMessageToDataBus", []);

export async function createEmbedding(input: string): Promise<number[]> {
    const embedding = await openai.embeddings.create({
        model: "text-embedding-ada-002",
        input: input,
    });

    console.log(embedding);
    return embedding.data[0].embedding;
}

export function averageEmbeddings(embeddings: number[][]): number[] {

    const sum = embeddings.reduce((acc, embedding) => {
        return math.add(acc, embedding) as number[];
    }, math.zeros(length) as number[]);

    return math.divide(sum, embeddings.length) as number[];
}

export async function compareSemantics(a: number[] | string, b: number[] | string) {

    const aEmbedding: number[] = a instanceof Array ? a : await createEmbedding(a);
    const bEmbedding: number[] = b instanceof Array ? b : await createEmbedding(b);

    let dotProduct = 0;
    let aMagnitude = 0;
    let bMagnitude = 0;

    for (let i = 0; i < a.length; i++) {

        dotProduct += aEmbedding[i] * bEmbedding[i];
        aMagnitude += aEmbedding[i] * aEmbedding[i];
        bMagnitude += bEmbedding[i] * bEmbedding[i];
    }

    aMagnitude = Math.sqrt(aMagnitude);
    bMagnitude = Math.sqrt(bMagnitude);

    return dotProduct / (aMagnitude * bMagnitude);
}
