import { isAuthenticated, api, accessToken } from '$stores/Auth';
import { newToast } from '$lib/Utils';

import type { RequestParams } from './Api';
import { get } from 'svelte/store';


// Utility to get the stored or local storage access token
function getStoredAccessToken(): string | null {
    const storeAccessToken = get(accessToken);
    if (storeAccessToken) return storeAccessToken;

    const localStorageAccessToken = localStorage.getItem('access_token');
    if (localStorageAccessToken) {
        accessToken.set(localStorageAccessToken); // Sync store with local storage
        return localStorageAccessToken;
    }

    return null; // No token found
}

export function getRequestParams(): RequestParams {
    const storedAccessToken = getStoredAccessToken();

    if (!storedAccessToken) {
        isAuthenticated.set(false);
        newToast('Not authenticated', "red");
        return {};
    }

    if (!isTokenValid(storedAccessToken)) {
        console.log('Token expired');
        refreshToken();
        // If refreshToken updates accessToken, fetch it again
        const updatedAccessToken = get(accessToken);
        return { headers: { Authorization: `Bearer ${updatedAccessToken}` } };
    }

    return { headers: { Authorization: `Bearer ${storedAccessToken}` } };
}


export async function handleLogin(username: string, password: string) {

    api
        .tokenCreate({ username, password, access: '', refresh: '' })
        .then((res) => {
            if (res.data.access && isTokenValid(res.data.access)) {
                isAuthenticated.set(true);
                localStorage.setItem('access_token', res.data.access);
                localStorage.setItem('refresh_token', res.data.refresh);
                newToast('Login successful!', "green");

            } else {
                throw new Error('Invalid token');
            }
        })
        .catch((res) => {
            const errorMessage = res.status === 401 ? 'Invalid credentials!' : 'Login failed!';
            newToast(errorMessage, "red");
            console.error(errorMessage, res);
        });
}

export async function refreshToken() {
    const refresTokenLocalStorage = localStorage.getItem('refresh_token');
    if (refresTokenLocalStorage) {
        if (isTokenValid(refresTokenLocalStorage)) {
            api.tokenRefreshCreate({ refresh: refresTokenLocalStorage, access: '' }).then((res) => {
                if (res.data.access) {
                    localStorage.setItem('access_token', res.data.access);
                    accessToken.set(res.data.access);
                }
            }
            );
            return;
        }
    }
    isAuthenticated.set(false);
}

export function isTokenValid(token: string): boolean {
    try {
        // Split the token into its parts
        const base64Url = token.split('.')[1]; // Access the payload part of the token
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Replace URL-safe base64 encoding characters
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
            // Decode base64 and URI-encoding
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        // Parse the payload as JSON and access the exp property
        const { exp } = JSON.parse(jsonPayload);

        if (!exp) {
            // If there's no exp field, assume the token is invalid
            return false;
        }
        const now = Math.floor(Date.now() / 1000); // Get current time in Unix timestamp
        return now < exp; // Check if the current time is before the expiration time
    } catch (e) {
        // If an error occurs (e.g., invalid token format), assume the token is invalid
        return false;
    }
}