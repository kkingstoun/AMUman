import { writable } from 'svelte/store';
import { Api } from './Api';

export const isAuthenticated = writable<boolean>(true);

export const activePage = writable<string>('Running');

export const api = new Api<string>({ baseUrl: 'http://localhost:8000' }).api;


const sidebarOpen = writable(false);

const openSidebar = () => {
	sidebarOpen.update(() => true);
};

const closeSidebar = () => {
	sidebarOpen.update(() => false);
};

export { sidebarOpen, openSidebar, closeSidebar };