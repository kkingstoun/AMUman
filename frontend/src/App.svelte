<script lang="ts">
  let activeTasks = [];
  let finishedTasks = [];
  import Navbar from "./lib/NavBar.svelte";
  import JobList from "./lib/JobList.svelte";
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
  />
</svelte:head>

<main>
  <Navbar />
  <div class="container relative" style="margin-top: 5rem;">
    <div id="content" class="container">
      <div class="row">
        <div class="col-lg-12">
          <p class="page-title lead"></p>
          <!-- <JobList /> -->
          <section>
            <h2>Finished tasks:</h2>
            <table>
              <thead>
                <tr>
                  <th>N.</th>
                  <th>ID</th>
                  <th>PATH</th>
                  <th>NODE NAME</th>
                  <th>PORT</th>
                  <th>SUBMIT TIME</th>
                </tr>
              </thead>
              <tbody>
                {#each finishedTasks as task}
                  <tr>
                    <td>{task.number}</td>
                    <td>{task.id}</td>
                    <td>{task.path}</td>
                    <td>{task.nodeName}</td>
                    <td>{task.port}</td>
                    <td>{task.submitTime}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </section>
        </div>
      </div>
    </div>
  </div>
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
  section > h2 {
    margin-top: 1rem;
    color: #f8f8f2; /* Dracula foreground color */
  }

  main {
    background-color: #282a36; /* Dracula background color */
    padding: 1rem;
    min-height: 100vh;
  }
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th,
  td {
    border: 1px solid #44475a; /* Dracula comment color */
    text-align: left;
    padding: 8px;
    color: #f8f8f2; /* Dracula foreground color */
  }

  th {
    background-color: #6272a4; /* Dracula selection color */
    color: white;
  }
</style>
