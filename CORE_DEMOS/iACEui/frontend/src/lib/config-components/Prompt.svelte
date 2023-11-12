<script lang="ts">
    import {parseHexColors} from "$lib/utils/regexUtils";

    export let borderColor: string = 'border-cyan-900';
    export let title: string = '';
    export let placeholder: string = '';
    export let size: string;
    export let textProps: string = 'text-[22px] text-neutral-400 text-center';
    export let position: string = 'top-0 left-0';

    export let inputValue = '';

    const color = parseHexColors(borderColor);
</script>

<div class={`flex flex-col space-y-1 ${borderColor} ${position}`}>
<!--    if title is not empty-->
    {#if title}
    <div class={`h-[30px] ${textProps} font-['Fenix']`}>{title}</div>
    {/if}
    <textarea style="border-color: {color[0]}" class="textarea text-white text-base resize-y {size} {borderColor} border-2 font-['Fenix']" placeholder={placeholder} bind:value={inputValue}></textarea>
</div>