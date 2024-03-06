<script lang="ts">
	import { NavLi } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import { accessToken, refreshToken } from '$stores/Auth';

	function handleLogout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		accessToken.set(null);
		refreshToken.set(null);

		goto('/login');
	}
</script>

<NavLi href="/" on:click={handleLogout}>Logout</NavLi>
