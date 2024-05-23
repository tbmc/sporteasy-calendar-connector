<script lang="ts">
  import { t } from 'svelte-i18n';

  import { dataParamsStore, disableSaveLoginStore, getOrigin } from './store.js';
  import TwoTextComponent from '$lib/UI/TwoTextComponent.svelte';
  import ColoredUrl from '$lib/GenerateUrl/ColoredUrl.svelte';

  const origin = getOrigin();
  $: url = `${origin}/api?${$disableSaveLoginStore ? 'disable_save_login=true&' : ''}data=${$dataParamsStore}`;

  let twoText: TwoTextComponent;

  function onCopyClick() {
    navigator.clipboard.writeText(url);
    twoText.animate();
  }
</script>

{#if $dataParamsStore !== ''}
  <article>
    <header>
      {$t('generateUrl.urlGenerated')}
    </header>

    <div class="custom-container">
      <code>
        <a href={url}>
          <ColoredUrl
            origin={origin}
            disableSaveLogin={$disableSaveLoginStore}
            data={$dataParamsStore}
          />
        </a>
      </code>
      <div class="sub-container">
        <button on:click={onCopyClick}>
          <TwoTextComponent bind:this={twoText} originalText={$t('copy')} otherText={'✓'} />
        </button>
      </div>
    </div>
  </article>
{/if}

<style>
  header {
    color: white;
    background-color: var(--primary-background);
  }

  .custom-container {
    display: grid;
    grid-template-columns: auto auto;
  }

  .sub-container {
    margin-left: 2vw;
    position: relative;
    min-width: 130px;
  }

  .sub-container button {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }

  code {
    display: grid;
    align-items: center;
    overflow-wrap: anywhere;
    min-height: 60px;
  }
</style>
