<script lang="ts">
    export let image: string;
    export let topCaption: string = "";
    export let bottomCaption: string = "";
    export let borderColor: string = "border-stone-500";
    export let borderSize: string = "border-2";
    export let textSize: string = "text-[10px]";
    export let size: string = "w-[137px] h-32";

    export let clicked: (event: MouseEvent) => void;

</script>
<div class="flex flex-col">
    {#if topCaption}
        <div class="text-neutral-400 {textSize} font-normal font-['Fenix']">{topCaption}</div>
    {/if}
    <button type="button"
            class="btn {size} rounded-[20px] {borderSize} {borderColor} justify-center items-center inline-flex overflow-hidden p-0 space-y-0"
            on:click={clicked}>
        <img class="{size}" src={image} alt=""/>
    </button>
    {#if bottomCaption}
        <div class="text-neutral-400 {textSize} font-normal font-['Fenix']">{bottomCaption}</div>
    {/if}
</div>

