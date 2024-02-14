
let api = "http://localhost:8000";
export async function getJobs(status: string): Promise<any> {
    try {
        const data = await authFetch("/api/jobs/" + status);
        return data;
    } catch (error) {
        console.error("Failed to fetch job data:", error);
    }
}

export async function authFetch(path: string, options: RequestInit = {}): Promise<Response> {
    const attemptFetch = async (access_token: string | null): Promise<Response> => {
        const headers = new Headers((options as { headers?: HeadersInit }).headers || {});
        if (access_token) {
            headers.set('Authorization', `Bearer ${access_token}`); // Use set instead of append to overwrite if necessary
        }

        const fetchOptions = {
            method: 'GET', // Default to GET requests
            headers: headers,
            ...options, // Spread in any other options to override defaults
        };

        const response = await fetch(api + path, fetchOptions);
        return response;
    };

    let access_token = localStorage.getItem('access_token');
    let response = await attemptFetch(access_token);

    if (response.status === 401) {
        const refreshed = await refreshToken();
        if (refreshed) {
            access_token = localStorage.getItem('access_token'); // Get the new token
            response = await attemptFetch(access_token); // Retry the fetch with the new token
        }
    }

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json(); // Assuming the server response is in JSON format
}

async function refreshToken(): Promise<boolean> {
    try {
        // Implement your token refresh logic here
        // This example uses a fictional API endpoint '/api/token/refresh'
        const refreshResponse = await fetch(api + '/api/token/refresh/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: localStorage.getItem('refresh_token') }), // Use your actual refresh token key
        });

        if (!refreshResponse.ok) {
            console.log('Failed to refresh token:', refreshResponse.status, refreshResponse.statusText);
            throw new Error('Failed to refresh token');
        }

        const data = await refreshResponse.json();
        localStorage.setItem('token', data.access); // Update with new token
        return true;
    } catch (error) {
        console.error('Refresh token error:', error);
        return false;
    }
}

export async function login(username: string, password: string) {
    const response = await fetch(api + "/api/token/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        console.log("Login successful:", data);
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
    } else {
        console.error("Login failed");
    }
}