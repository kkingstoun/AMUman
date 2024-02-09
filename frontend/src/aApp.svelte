<script lang="ts">
  import Navbar from "./lib/NavBar.svelte";
  import JobList from "./lib/JobList.svelte";
  import Auth from "./lib/Auth.svelte";
  import Router from "svelte-spa-router";
  import { push, pop, replace } from "svelte-spa-router";

  import Home from "./routes/Home.svelte";
  import Tasks from "./routes/Tasks.svelte";

  // Define your routes
  const routes = {
    "/": Home,
    "/tasks": Tasks,
  };
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
  />
</svelte:head>

<main>
  <Router {routes} />
  <Navbar />
  <h1>
    <a href="#/tasks">Thus Spoke Zarathustra</a>
  </h1>
  <button on:click={() => push("/tasks")}>Go somewhere</button>

  <div class="container relative" style="margin-top: 5rem;">
    <div id="content" class="container">
      <div class="row">
        <div class="col-lg-12">
          <p class="page-title lead"></p>
          <JobList />
        </div>
      </div>
    </div>
  </div>
  <Auth />
</main>

<style>
  :global(body) {
    margin: 0px;
    border: 0px;
    padding: 0px;
    color: #f8f8f2; /* Dracula foreground color */
    font-size: large;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 400;
    padding-bottom: 90%;
    background-color: #282a36; /* Dracula background color */
    background-attachment: fixed;
  }

  main {
    background-color: #282a36; /* Dracula background color */
    padding: 1rem;
    min-height: 100vh;
  }
</style>
