<script>
	import { Avatar, Dropdown, DropdownHeader, DropdownItem, DropdownDivider } from 'flowbite-svelte';
	import { username } from '$stores/Auth';
	import { accessToken, refreshToken } from '$stores/Auth';
	import { goto } from '$app/navigation';

	function handleLogout() {
		accessToken.set(null);
		refreshToken.set(null);
		goto('/login');
	}
</script>

<Avatar id="user-drop" class="cursor-pointer" dot={{ color: 'green' }}>
	{$username?.slice(0, 2)}
</Avatar>
<Dropdown triggeredBy="#user-drop">
	<DropdownHeader>
		<span class="block text-sm">{$username}</span>
	</DropdownHeader>
	<DropdownItem on:click={handleLogout}>Logout</DropdownItem>
</Dropdown>
