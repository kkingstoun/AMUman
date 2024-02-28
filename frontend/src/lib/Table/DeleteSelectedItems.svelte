<script lang="ts">
	import { Button, Modal } from 'flowbite-svelte';
	import { ExclamationCircleOutline } from 'flowbite-svelte-icons';
	import { TrashBinOutline } from 'flowbite-svelte-icons';
	import { selectedItems } from '$stores/Tables';
	import { deleteSelectedItems } from '$api/Table';
	import type { ItemTypeString } from '$stores/Tables';

	let popupModal = false;
	export let item_type: ItemTypeString;
</script>

<Button color="red" size="sm" on:click={() => (popupModal = true)}>
	<TrashBinOutline />
</Button>

<Modal bind:open={popupModal} size="xs" autoclose>
	<div class="text-center">
		<ExclamationCircleOutline class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" />
		<h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
			Are you sure you want to delete {item_type}
			{$selectedItems[item_type]} ?
		</h3>
		<Button
			color="red"
			class="me-2"
			on:click={() => {
				deleteSelectedItems(item_type);
			}}
		>
			Yes, I'm sure
		</Button>
		<Button color="alternative">No, cancel</Button>
	</div>
</Modal>
