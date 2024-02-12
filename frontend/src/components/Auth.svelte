<script>
    import { login } from "../api"; // Adjust the path as necessary
    let username = "admin";
    let password = "admin";
    async function handleLogin() {
        await login(username, password);
    }
</script>

<form on:submit|preventDefault={handleLogin}>
    <input type="username" bind:value={username} placeholder="username" />
    <input type="password" bind:value={password} placeholder="Password" />
    <button type="submit">Login</button>
</form>
