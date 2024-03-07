<script>
	import { Toggle } from 'flowbite-svelte';
	import NavBar from '$lib/Navbar/NavBar.svelte';
	let checked = false;
	function handleClick() {
		console.log(`Current toggle status: ${checked}`);
		// At this point, checked should correctly reflect the toggle's status,
		// but handleClick may not be the best place to monitor changes to 'checked'.
	}
</script>

<NavBar />
<main class="p-5">
	<Toggle bind:checked on:click={handleClick} aria-checked={checked}>Autorun jobs</Toggle>
</main>
