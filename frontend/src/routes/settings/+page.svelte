<script>
	import { Toggle } from 'flowbite-svelte';
	let checked = false;
	function handleClick() {
		console.log(`Current toggle status: ${checked}`);
		// At this point, checked should correctly reflect the toggle's status,
		// but handleClick may not be the best place to monitor changes to 'checked'.
	}
</script>

<main class="p-5">
	<Toggle bind:checked on:click={handleClick} aria-checked={checked}>Autorun jobs</Toggle>
</main>
