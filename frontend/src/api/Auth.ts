import { api, accessToken, refreshToken } from '$stores/Auth';
import { newToast } from '$lib/Utils';

import type { RequestParams } from './Api';
import { get } from 'svelte/store';
import { goto } from '$app/navigation';


export function getRequestParams(): RequestParams {
    const accessTokenString = get(accessToken);

    if (accessTokenString && !isTokenExpired(accessTokenString)) {
        return { headers: { Authorization: `Bearer ${accessTokenString}` } };
    }
    // If no access token, try to refresh it
    const refreshTokenString = get(refreshToken);
    if (refreshTokenString) {
        console.log('Refreshing token');
        if (isTokenExpired(refreshTokenString)) {
            newToast('Session expired', "red");
            goto('/login');
            return {};
        }
        api.tokenRefreshCreate({ refresh: refreshTokenString, access: '' }).then((res) => {
            if (res.data.access) {
                localStorage.setItem('access_token', res.data.access);
                accessToken.set(res.data.access);
            }
        }
        ).catch((res) => {
            console.error('Token refresh failed', res);
        });
        return {};
    }
    newToast('Not authenticated', "red");
    goto('/login');
    return {};
}


export async function handleLogin(username: string, password: string) {
    api
        .tokenCreate({ username, password, access: '', refresh: '' })
        .then((res) => {
            if (res.data.access && res.data.refresh) {
                localStorage.setItem('access_token', res.data.access);
                localStorage.setItem('refresh_token', res.data.refresh);
                accessToken.set(res.data.access);
                refreshToken.set(res.data.refresh);
                newToast('Login successful!', "green");
                goto('/jobs');

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

export function initTokens() {
    let localStorageRefreshToken = localStorage.getItem('refresh_token');
    if (localStorageRefreshToken) {
        refreshToken.set(localStorageRefreshToken);
        let localStorageAccessToken = localStorage.getItem('access_token');
        if (localStorageAccessToken) {
            accessToken.set(localStorageAccessToken);
        }
        goto('/jobs');
    } else {
        goto('/login');
    }
}
function tokenExpiry(token: string): number {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    const { exp } = JSON.parse(jsonPayload);
    return exp;
}
export function isTokenExpired(token: string): boolean {
    return tokenExpiry(token) < Date.now() / 1000;
}