<script lang="ts">
	import { NavLi } from 'flowbite-svelte';
	import { accessToken, refreshToken } from '$stores/Auth';

	function handleLogout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		accessToken.set(null);
		refreshToken.set(null);
	}
</script>

<NavLi href="/login" on:click={handleLogout}>Logout</NavLi>
