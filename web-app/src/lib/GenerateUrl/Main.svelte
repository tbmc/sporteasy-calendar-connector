<script lang="ts">
  import LoginForm from './LoginForm.svelte';
  import ListTeams from './ListTeams.svelte';
  import ShowUrl from './ShowUrl.svelte';
</script>

<svelte:head>
  <title>SportEasy Calendar Converter</title>
</svelte:head>

<main class="container">
  <LoginForm />
  <ListTeams />
  <ShowUrl />
</main>
