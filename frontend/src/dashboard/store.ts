import { writable } from 'svelte/store';

const sidebarOpen = writable(true);

const openSidebar = () => {
	sidebarOpen.update(() => true);
};

const closeSidebar = () => {
	sidebarOpen.update(() => false);
};

export { sidebarOpen, openSidebar, closeSidebar };
