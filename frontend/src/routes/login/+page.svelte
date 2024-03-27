<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import { handleLogin } from '$api/Auth';
	import { username } from '$stores/Auth';
	let password = 'admin';
</script>

<main
	class="main flex flex-col items-center justify-start h-screen w-full bg-gray-800 px-2 md:px-4 lg:px-6 pt-40"
>
	<div class="flex justify-center">
		<img
			alt="amuman logo"
			src="/images/logo.png"
			class="h-40 mx-auto object-cover rounded-full w-40"
		/>
	</div>

	<div id="form" class="flex flex-col items-center justify-center mt-4 rounded-lg">
		<h1 class="text-3xl font-bold text-white">Welcome to Amuman</h1>
		<p class="text-white pb-4">Please login to continue</p>
		<div class=" text-white p-4 rounded-lg shadow top-0 right-0 bg-gray-700 pt-4">
			<form>
				<div>
					<label for="username">Username:</label>
					<input
						id="username"
						bind:value={$username}
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
					<Button class="font-extrabold" on:click={() => handleLogin($username, password)}
						>Login</Button
					>
				</div>
			</form>
		</div>
		<div class="p-3">
			Don't have an account? <a href="/register" class="text-primary-600">Register</a>
		</div>
	</div>
</main>
