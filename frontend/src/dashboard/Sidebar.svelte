<script>
	import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper } from 'flowbite-svelte';
	import { GridSolid } from 'flowbite-svelte-icons';
	import { activePage } from '$stores/store';

	const data = [
		{
			section: 'Jobs',
			content: [
				{ title: 'All', link: '/jobs' },
				{ title: 'Running', link: '/jobs/running' },
				{ title: 'Queued', link: '/jobs/queued' },
				{ title: 'Finished', link: '/jobs/finished' },
				{ title: 'New', link: '/jobs/new' }
			]
		},
		{
			section: 'Others',
			content: [
				{ title: 'Nodes', link: '/nodes' },
				{ title: 'GPUs', link: '/gpus' }
			]
		},
		{ section: 'Settings', content: [{ title: 'Settings', link: '/settings' }] }
	];
</script>

<Sidebar class="w-48">
	<SidebarWrapper>
		{#each data as { section, content } (section)}
			<div class="pt-4">
				{section}
			</div>
			<SidebarGroup border class="pl-3">
				{#each content as item (item.title)}
					<SidebarItem
						label={item.title}
						href={item.link}
						on:click={() => {
							$activePage = item.title;
						}}
					>
						<svelte:fragment slot="icon">
							<GridSolid
								class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900"
							/>
						</svelte:fragment>
					</SidebarItem>
				{/each}
			</SidebarGroup>
		{/each}
	</SidebarWrapper>
</Sidebar>
