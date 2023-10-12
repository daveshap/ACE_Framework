<script lang="ts">
    export let orientation: "up" | "down" = "down";
    export let height: number = 50;
    export let width: number = 12;
    export let arrowColor: string = "black";

    let transform: string = "";

    $: {
        transform = orientation === "up" ? "rotate(180deg)" : "";
    }
</script>

<svg
        xmlns="http://www.w3.org/2000/svg"
        {width}
        {height}
        viewBox="0 0 12 50"
        fill="none"
        style="transform: {transform};"
>
    <path
            d="M6 50L11.7735 40L0.226494 40L6 50ZM5 -7.66399e-08L5 41L7 41L7 7.66399e-08L5 -7.66399e-08Z"
            fill={arrowColor}
    />
</svg>
