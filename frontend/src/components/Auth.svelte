<script lang="ts">
	import { login } from '../api'; // Adjust the path as necessary
	import { toast } from '@zerodevx/svelte-toast';

	let username = 'admin';
	let password = 'admin';
	let showPopup = false;
	let popup: HTMLDivElement;

	async function handleLogin() {
		try {
			await login(username, password);
			toast.push('Login successful!');
		} catch (error) {
			toast.push('Login failed!');
		}
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<span
	class="block pl-5 relative"
	on:click={(e) => {
		e.stopPropagation();
		showPopup = !showPopup;
	}}
>
	{username}
	{#if showPopup}
		<div
			bind:this={popup}
			class="absolute bg-gray-800 text-white border p-4 rounded shadow top-0 right-0"
		>
			<form>
				<div>
					<label for="username">Username:</label>
					<input
						id="username"
						bind:value={username}
						type="text"
						class="border rounded w-full p-2 bg-gray-700 text-white"
					/>
				</div>
				<div class="mt-2">
					<label for="password">Password:</label>
					<input
						id="password"
						bind:value={password}
						type="password"
						class="border rounded w-full p-2 bg-gray-700 text-white"
					/>
				</div>
				<div class="mt-2">
					<button
						type="button"
						on:click={handleLogin}
						class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
					>
						Login
					</button>
				</div>
			</form>
		</div>
	{/if}
</span>
