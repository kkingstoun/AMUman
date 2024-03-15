<script lang="ts">
	import { NavLi } from 'flowbite-svelte';
	import { accessToken, refreshToken } from '$stores/Auth';

	function handleLogout() {
		accessToken.set(null);
		refreshToken.set(null);
	}
</script>

<NavLi href="/login" on:click={handleLogout}>Logout</NavLi>
