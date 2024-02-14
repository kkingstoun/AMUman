<script lang="ts">
	import { sidebarOpen } from '../store';
	import AllAppsIcon from './icons/AllAppsIcon.svelte';

	const data = [
		{
			section: 'Jobs',
			content: [
				{
					title: 'All',
					icon: AllAppsIcon,
					link: '/jobs'
				},
				{
					title: 'Running',
					icon: AllAppsIcon,
					link: '/jobs/active'
				},
				{
					title: 'Queued',
					icon: AllAppsIcon,
					link: '/jobs/queued'
				},
				{
					title: 'Finished',
					icon: AllAppsIcon,
					link: '/jobs/finished'
				},
			]
		},
		{
			section: 'Others',
			content: [
				{
					title: 'Nodes',
					icon: AllAppsIcon,
					link: '/nodes'
				},
				{
					title: 'GPUs',
					icon: AllAppsIcon,
					link: '/gpus'
				},
			]
		},
	];
	type MobileOrientationKey = 'start' | 'end';
	const style = {
		mobileOrientation: {
			start: 'left-0',
			end: 'right-0'
		} as Record<MobileOrientationKey, string>
	};

	export let mobileOrientation: MobileOrientationKey = 'start';
</script>

<aside
	class={`top-0 scrollbar bg-gray-900 h-screen overflow-y-auto
      lg:bg-transparent lg:block lg:relative lg:w-64 lg:z-auto 
      ${style.mobileOrientation[mobileOrientation]}
      ${$sidebarOpen ? 'absolute w-8/12 z-40 sm:w-5/12' : 'hidden'}
   `}
>
	<div class="pb-32 lg:pb-6">
        <div class="flex justify-center">
			<a href="/">
				<img
				alt="amuman logo"
				src="/images/logo.png"
				class="h-40 mx-auto object-cover rounded-full w-40"
				/>
			</a>
        </div>
		<ul class="mt-6 md:pl-6">
			<li>
				{#each data as { section, content } (section)}
					<div class="mb-10">
						<div class="font-medium mb-4 pl-5 text-gray-500 text-lg lg:pl-6">{section}</div>
						{#each content as item (item.title)}
							<a
								href={item.link}
								class="flex items-center justify-start my-1 p-3 text-white w-full"
							>
								<span><svelte:component this={item.icon} /></span>
								<span class="mx-4 text-sm">{item.title}</span>
							</a>
						{/each}
					</div>
				{/each}
			</li>
		</ul>
	</div>
</aside>

<style>
	.scrollbar::-webkit-scrollbar {
		width: 0;
		background: transparent; /* hide Sidebar scrollbar on Chrome, Opera and other webkit Browsers*/
	}
	.scrollbar {
		-ms-overflow-style: none;
	}
</style>
