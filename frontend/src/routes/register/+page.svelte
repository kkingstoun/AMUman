<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import { api } from '$stores/Auth';
	import { newToast } from '$stores/Toast';

	import { goto } from '$app/navigation';

	let username = 'admin';
	let password = 'admin';
	let password_confirm = 'admin';
	let email = 'example@amu.edu.pl';

	function handleRegister() {
		if (password !== password_confirm) {
			newToast('Passwords do not match', 'red');
			password = '';
			password_confirm = '';
			return;
		}
		if (username.length < 3) {
			newToast('Username must be at least 3 characters long', 'red');
			return;
		}
		if (password.length < 5) {
			newToast('Password must be at least 5 characters long', 'red');
			return;
		}
		if (!email.endsWith('amu.edu.pl')) {
			newToast('Email must end with "amu.edu.pl"', 'red');
			return;
		}

		let user = {
			username: username,
			password: password,
			email: email,
			concurrent_jobs: 0,
			auth: {
				id: 1,
				password: 'string',
				username: 'string'
			}
		};
		api
			.usersCreate(user)
			.then(() => {
				goto('/postregister');
			})
			.catch((res) => {
				// make a toast for all fields in res.error
				for (let field in res.error) {
					newToast(res.error[field], 'red');
				}
			});
	}
</script>

<main
	class="main flex flex-col items-center justify-start h-screen w-full bg-gray-800 px-2 md:px-4 lg:px-6 pt-40"
>
	<div class="flex justify-center">
		<a href="/">
			<img
				alt="amuman logo"
				src="/images/logo.png"
				class="h-40 mx-auto object-cover rounded-full w-40"
			/>
		</a>
	</div>

	<div id="form" class="flex flex-col items-center justify-center mt-4 rounded-lg">
		<h1 class="text-3xl font-bold text-white">Welcome to Amuman</h1>
		<p class="text-white pb-4">Register a new account</p>
		<div class=" text-white p-4 rounded-lg shadow top-0 right-0 bg-gray-700 pt-4">
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
				<div>
					<label for="username">Email:</label>
					<input
						id="username"
						bind:value={email}
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
					<label for="password">Confirm Password:</label>
					<input
						id="password"
						bind:value={password_confirm}
						type="password"
						class="border rounded w-full p-2 bg-gray-700 text-white"
					/>
				</div>
				<div class="mt-2">
					<Button class="font-extrabold" on:click={handleRegister}>Register</Button>
				</div>
			</form>
		</div>
		<div class="p-3">
			Already have an account? <a href="/login" class="text-primary-600">Login</a>
		</div>
	</div>
</main>
