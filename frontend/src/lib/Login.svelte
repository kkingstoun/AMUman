<script lang="ts">
	import { isAuthenticated, api } from '../store';
	import { isTokenValid } from '../auth';
	import { successToast, errorToast } from './Toast';

	let username = 'admin';
	let password = 'admin';
	async function handleLogin() {
		api
			.tokenCreate({ username, password, access: '', refresh: '' })
			.then((res) => {
				if (res.data.access && isTokenValid(res.data.access)) {
					isAuthenticated.set(true);
					localStorage.setItem('access_token', res.data.access);
					localStorage.setItem('refresh_token', res.data.refresh);
					successToast('Login successful!');
				} else {
					throw new Error('Invalid token');
				}
			})
			.catch((res) => {
				const errorMessage = res.status === 401 ? 'Invalid credentials!' : 'Login failed!';
				errorToast(errorMessage);
				console.error(errorMessage, res);
			});
	}
</script>

<main class="main flex flex-col hscreen w-full h-screen pb-36 pt-4 px-2 md:pb-8 md:px-4 lg:px-6">
	<div class="flex justify-center">
		<a href="/">
			<img
				alt="amuman logo"
				src="/images/logo.png"
				class="h-40 mx-auto object-cover rounded-full w-40"
			/>
		</a>
	</div>
	<div class="flex flex-col items-center justify-center mt-4">
		<h1 class="text-3xl font-bold text-white">Welcome to Amuman</h1>
		<p class="text-white">Please login to continue</p>
		<div class=" text-white p-4 rounded shadow top-0 right-0">
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
						class="hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
						style="background: var(--accent-color)"
					>
						Login
					</button>
				</div>
			</form>
		</div>
	</div>
</main>
