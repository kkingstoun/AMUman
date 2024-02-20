<script lang="ts">
	import { isAuthenticated } from '../../stores/store';
	import { NavLi } from 'flowbite-svelte';
	function handleLogout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		isAuthenticated.set(false);
	}
</script>

<NavLi href="/" on:click={handleLogout}>Logout</NavLi>
