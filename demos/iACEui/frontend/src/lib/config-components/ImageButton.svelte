<script lang="ts">
    export let image: string;
    export let caption: string = "caption";
    export let borderColor: string = "border-stone-500";
    export let borderSize: string = "border-2";
    export let size: string = "w-[137px] h-32";

    export let clicked: (event: MouseEvent) => void;

</script>

<button type="button" class="btn flex-col justify-start inline-flex" on:click={clicked} >
    <div class="{size} rounded-[20px] {borderSize} {borderColor} justify-center items-center inline-flex overflow-hidden">
        <img class="{size}" src={image} alt=""/>
    </div>
    <div class="text-neutral-400 text-[10px] font-normal font-['Fenix']">{caption}</div>
</button>
