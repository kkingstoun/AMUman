<script lang="ts">
	import { sidebarOpen } from '../store';
	import { page } from '$app/stores';
	import UxIcon from './icons/UxIcon.svelte';
	import ArIcon from './icons/ArIcon.svelte';
	import VideosIcon from './icons/VideosIcon.svelte';
	import AllAppsIcon from './icons/AllAppsIcon.svelte';
	import UpdatesIcon from './icons/UpdatesIcon.svelte';
	import PhotographyIcon from './icons/PhotographyIcon.svelte';
	import IllustrationIcon from './icons/IllustrationIcon.svelte';
	import GraphicDesignIcon from './icons/GraphicDesignIcon.svelte';
	import DocumentationIcon from './icons/DocumentationIcon.svelte';

	const data = [
		{
			section: 'Apps',
			content: [
				{
					title: 'All Apps',
					icon: AllAppsIcon,
					link: '/'
				},
				{
					title: 'Updates',
					icon: UpdatesIcon,
					link: '/admin/updates'
				}
			]
		},
		{
			section: 'Categories',
			content: [
				{
					title: 'Photography',
					icon: PhotographyIcon,
					link: '/admin/photography'
				},
				{
					title: 'Graphic Design',
					icon: GraphicDesignIcon,
					link: '/admin/graphic-design'
				},
				{
					title: 'Videos',
					icon: VideosIcon,
					link: '/admin/videos'
				},
				{
					title: 'Illustrations',
					icon: IllustrationIcon,
					link: '/admin/illustration'
				},
				{
					title: 'UI/UX',
					icon: UxIcon,
					link: '/admin/ux'
				},
				{
					title: '3D/AR',
					icon: ArIcon,
					link: '/admin/ar'
				}
			]
		},
		{
			section: 'Guides',
			content: [
				{
					title: 'Documentation',
					icon: DocumentationIcon,
					link: '/admin/documentation'
				}
			]
		}
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
		<ul class="mt-6 md:pl-6">
			<li>
				{#each data as { section, content } (section)}
					<div class="mb-10">
						<div class="font-medium mb-4 pl-5 text-gray-500 text-lg lg:pl-6">{section}</div>
						{#each content as item (item.title)}
							<a
								href={item.link}
								class={`flex items-center justify-start my-1 p-3 text-white w-full ${
									item.link === $page.url.pathname &&
									'border-white lg:border-red-300 border-l-4 lg:border-l-0 lg:border-r-4'
								}`}
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
