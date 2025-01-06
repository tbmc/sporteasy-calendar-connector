<script lang="ts">
  import { t } from 'svelte-i18n';

  import { dataToRequestParam } from '$lib/GenerateUrl/dataToRequestParam.js';
  import {
    dataParamsStore,
    disableSaveLoginStore,
    fetchTeamsGet,
    fetchTeamsIsLoading
  } from '$lib/GenerateUrl/store.js';
  import TwoTextComponent from '$lib/UI/TwoTextComponent.svelte';
  import AlertWarning from '$lib/Components/AlertWarning.svelte';
  import AlertInfo from '$lib/Components/AlertInfo.svelte';
  import Github from '$lib/images/github.svelte';

  let usernameTranslation = $t('generateUrl.form.username');
  let passwordTranslation = $t('generateUrl.form.password');
  let teamIdTranslation = $t('generateUrl.form.teamId');

  let username = '';
  let password = '';
  let teamId = '';

  let invalidUsername: boolean | null = null;
  let invalidPassword: boolean | null = null;

  let disableSaveLogin = false;

  function clicked() {
    invalidUsername = username === '';
    invalidPassword = password === '';
  }

  function listTeams() {
    if (username !== '' && password !== '') fetchTeamsGet(username, password);

    clicked();
  }

  let twoText: TwoTextComponent;

  function generateUrl() {
    if (username !== '' && password !== '') {
      const data = dataToRequestParam(username, password, teamId);
      dataParamsStore.set(data);
      disableSaveLoginStore.set(disableSaveLogin);
      twoText.animate();

      setTimeout(() => {
        window.scrollTo(0, document.body.scrollHeight);
      }, 500);
    }

    clicked();
  }

  function reset() {
    username = '';
    password = '';
    teamId = '';

    clicked();
  }
</script>

<article>
  <header>
    {$t('generateUrl.header')}
  </header>

  <div>
    <div>
      <!-- Warnings -->
      <AlertWarning>
        <span style="font-size: 2em; color: red; font-family: sans-serif">⚠</span>
        {$t('generateUrl.warning.logins')}
      </AlertWarning>
      <p>
        {$t('generateUrl.warning.repository')}
        <a href="https://github.com/tbmc/sporteasy-calendar-connector">
          <span class="logo-github">
            <Github />
          </span>
          Github repo
        </a>
      </p>
      <p>{$t('generateUrl.warning.credentialsRequired')}</p>
    </div>
    <div>
      <!-- Username -->
      <label for="username">
        {usernameTranslation}
        <input
          type="text"
          id="username"
          name="username"
          placeholder={usernameTranslation}
          required
          bind:value={username}
          aria-invalid={invalidUsername}
        />
      </label>

      <!-- Password -->
      <label for="password">
        {passwordTranslation}
        <input
          type="password"
          id="password"
          name="password"
          placeholder={passwordTranslation}
          required
          bind:value={password}
          aria-invalid={invalidPassword}
        />
      </label>

      <!-- Team id -->
      <label for="teamId">
        {teamIdTranslation}
        <input type="text" name="teamId" placeholder={teamIdTranslation} bind:value={teamId} />
      </label>

      <!-- Disable save login -->
      <fieldset>
        <label>
          <input
            name="disableSaveLogin"
            type="checkbox"
            role="switch"
            bind:checked={disableSaveLogin}
          />
          {$t('generateUrl.form.disableSaveLogin')}
        </label>
        <AlertInfo>
          {$t('generateUrl.form.disableSaveLoginExtra')}
        </AlertInfo>
      </fieldset>
    </div>
  </div>

  <footer>
    <div class="grid">
      <div />
      <button class="secondary outline reset" on:click={reset}
        >{$t('generateUrl.form.buttonReset')}</button
      >
      <button class="secondary list-teams" on:click={listTeams} aria-busy={$fetchTeamsIsLoading}>
        {$t('generateUrl.form.buttonListTeams')}
      </button>
      <button class="generate" on:click={generateUrl}>
        <TwoTextComponent
          bind:this={twoText}
          originalText={$t('generateUrl.form.buttonGenerate')}
          otherText="✓"
        />
      </button>
      <div />
    </div>
  </footer>
</article>

<style>
  header {
    color: white;
    background-color: var(--primary-background);
  }

  footer button.generate {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
  }

  .logo-github {
    width: 1.2em;
    display: inline-block;
    color: var(--primary-color);
  }
</style>
