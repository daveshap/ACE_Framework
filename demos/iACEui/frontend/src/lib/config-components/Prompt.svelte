<script lang="ts">
    import {parseHexColors} from "$lib/utils/regexUtils";

    export let borderColor: string = 'border-cyan-900';
    export let title: string = 'Input';
    export let placeholder: string = 'Enter your prompt here.';
    export let size: string;
    export let fontSize: string = 'text-[22px]';
    export let position: string = 'top-0 left-0';

    export let inputValue = '';

    const color = parseHexColors(borderColor);
</script>

<div class={`flex flex-col justify-center items-center space-y-1 ${borderColor} ${position}`}>
    <div class={`h-[30px] text-center text-neutral-400 ${fontSize} font-['Fenix']`}>{title}</div>
    <textarea style="border-color: {color[0]}" class="textarea text-white text-base resize-y {size} {borderColor} border-2 font-['Fenix']" placeholder={placeholder} bind:value={inputValue}></textarea>
</div>