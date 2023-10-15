<script lang="ts">

    import ControlStateImage from "$lib/images/control_state_img.png";
    import DataStateImage from "$lib/images/data_state_img.jpeg";

    import ImageButton from "$lib/config-components/ImageButton.svelte";
    import Prompt from "$lib/config-components/Prompt.svelte";
    import Arrow from "$lib/interaction-components/messages/Arrow.svelte";

    export let type: 'data' | 'control' = 'data';
    export let title: string = '';
    export let placeholder: string = '';
    export let size: string;
    export let textProps: string = 'text-neutral-500 text-[22px] text-start';

    let colorControlBus = "border-[#9B5548]";
    let colorDataBus = "border-[#0F3D5C]";
    export let inputValue: string;

    let borderColor = type === 'data' ? colorDataBus : colorControlBus;
    let arrowColor = type === 'data' ? '#0F3D5C' : '#9B5548';
    let imageSrc = type === 'data' ? DataStateImage : ControlStateImage;

    let arrowOrientation: "up" | "down" = type === "data" ? "up" : "down";

</script>

<div class="flex flex-col items-center">
    {#if type === "data"}
        <Prompt
                size={size}
                borderColor={borderColor}
                placeholder={placeholder}
                title={title}
                textProps={textProps}
                bind:inputValue={inputValue}
        />
        <Arrow orientation={arrowOrientation} height={50} width={12} arrowColor={arrowColor}/>
        <ImageButton
                image={imageSrc}
                bottomCaption="open full view"
                borderColor={borderColor}
                clicked={(e) => console.log("Button clicked" + e)}
        />
    {/if}
    {#if type === "control"}
        <ImageButton
                image={imageSrc}
                topCaption="open full view"
                borderColor={borderColor}
                clicked={(e) => console.log("Button clicked" + e)}
        />

        <!-- Arrow -->
        <Arrow orientation={arrowOrientation} height={50} width={12} arrowColor={arrowColor}/>
        <Prompt
                size={size}
                borderColor={borderColor}
                placeholder={placeholder}
                title={title}
                textProps={textProps}
                bind:inputValue={inputValue}
        />
    {/if}
</div>
