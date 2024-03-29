<script lang="ts">
  import { t } from 'svelte-i18n';

  import { fetchTeamsData, fetchTeamsLoadedOnce } from './store.js';

  $: data = $fetchTeamsData.map((t) => ({
    id: t[0],
    name: t[1]
  }));
</script>

{#if $fetchTeamsLoadedOnce}
  <article>
    <header>
      {$t('generateUrl.listTeams.title')}
    </header>

    <div>
      <table>
        <thead>
          <tr>
            <th>{$t('generateUrl.listTeams.name')}</th>
            <th>{$t('generateUrl.listTeams.id')}</th>
          </tr>
        </thead>
        <tbody>
          {#each data as teamLine (teamLine.id)}
            <tr>
              <td>{teamLine.name}</td>
              <td>{teamLine.id}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </article>
{/if}
