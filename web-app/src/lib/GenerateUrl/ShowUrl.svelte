<script lang="ts">
  import { t } from 'svelte-i18n';

  import {dataParams, getOrigin} from './store.js';

  const origin = getOrigin();
  $: url = `${origin}?data=${$dataParams}`;
</script>

{#if $dataParams !== ''}
  <article>
    <header>
      {$t('generateUrl.urlGenerated')}
    </header>

    <div>
      <a href={url}>{url}</a>
    </div>
  </article>
{/if}

<style>
  header {
    color: white;
    background-color: var(--primary-background);
  }
</style>
