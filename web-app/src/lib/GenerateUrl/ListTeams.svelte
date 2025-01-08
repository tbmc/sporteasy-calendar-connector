<script lang="ts">
  import { t } from 'svelte-i18n';

  import { fetchTeamsData, fetchTeamsLoadedOnce } from './store.js';
  import type { Action } from 'svelte/action';

  $: data = $fetchTeamsData.map((t) => ({
    id: t[0],
    name: t[1],
    url: t[2]
  }));

  const onLoad: Action = (element) => {
    window.scrollTo(0, document.body.scrollHeight);
  };
</script>

{#if $fetchTeamsLoadedOnce}
  <article>
    <header>
      {$t('generateUrl.listTeams.title')}
    </header>

    <div use:onLoad>
      <table>
        <thead>
          <tr>
            <th>{$t('generateUrl.listTeams.name')}</th>
            <th>{$t('generateUrl.listTeams.id')}</th>
            <th>{$t('generateUrl.listTeams.link')}</th>
          </tr>
        </thead>
        <tbody>
          {#each data as teamLine (teamLine.id)}
            <tr>
              <td>{teamLine.name}</td>
              <td>{teamLine.id}</td>
              <td><a href={teamLine.url}>{$t('generateUrl.listTeams.link')}</a></td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </article>
{/if}

<style>
  header {
    color: white;
    background-color: var(--primary-background);
  }
</style>
