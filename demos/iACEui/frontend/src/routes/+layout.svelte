<script lang="ts">
	import '../app.postcss';
	import { AppShell } from '@skeletonlabs/skeleton';
</script>

<link href="https://fonts.googleapis.com/css2?family=Fenix" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Goldman" rel="stylesheet">

<!-- App Shell -->
<AppShell regionPage="relative" slotPageHeader="sticky top-0 z-10" class="bg-[#1E1E1E]">
<!--	+page is inside ./Layers -->
	<slot />
</AppShell>
