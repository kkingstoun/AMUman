<script lang="ts">
	import 'tailwindcss/tailwind.css';

	import TopBar from './NavBar.svelte';
	import Login from '$lib/Login.svelte';
	import Footer from './Footer.svelte';
	import Sidebar from './Sidebar.svelte';
	import { isAuthenticated } from '$stores/store';
	import { SvelteToast } from '@zerodevx/svelte-toast';
</script>

<SvelteToast />
{#if $isAuthenticated}
	<TopBar />
	<div class="background overflow-hidden w-full lg:p-4">
		<div class="content flex flex-col justify-between overflow-hidden relative lg:rounded-2xl">
			<div class="flex items-start flex-1">
				<Sidebar />
				<div class="flex flex-col flex-1 pl-0 w-full lg:space-y-4 lg:w-[calc(100%-16rem)]">
					<main class="main flex-1 overflow-y-auto pb-36 pt-4 px-2 md:pb-8 md:px-4 lg:px-6">
						<slot />
					</main>
				</div>
			</div>
			<Footer />
		</div>
	</div>
{:else}
	<Login />
{/if}

<style>
	.background {
		/* background-image: url('./mac.webp'); */
		background-color: rgb(43, 43, 56);
		background-size: cover;
		background-position: center;
	}
	.content {
		background-color: rgba(16 18 27 / 40%);
		backdrop-filter: blur(24px);
	}
	.main {
		color: #f9fafb;
		background-color: rgba(16 18 27 / 40%);
		overflow: auto;
	}
	.main::-webkit-scrollbar {
		width: 6px;
		border-radius: 10px;
	}
	.main::-webkit-scrollbar-thumb {
		background: rgb(1 2 3 / 40%);
		border-radius: 10px;
	}
</style>
