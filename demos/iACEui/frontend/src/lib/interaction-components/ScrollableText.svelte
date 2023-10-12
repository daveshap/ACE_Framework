<script lang="ts">
    export let color: string = 'bg-gray-100';
    export let maxWidth: string = 'w-full'; // Default to full width if no max width is provided
    export let text: string = 'This is a very long text that needs to be scrollable horizontally...';
</script>

<style>
    .scrollable-text {
        white-space: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
</style>

<div class="scrollable-text {maxWidth} {color} p-4">
    {text}
</div>