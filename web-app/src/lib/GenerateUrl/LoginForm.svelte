<script lang="ts">
  import { t } from 'svelte-i18n';
  
  import {dataToRequestParam} from "$lib/GenerateUrl/dataToRequestParam.js";
  import {dataParams, fetchTeamsGet, fetchTeamsIsLoading} from "$lib/GenerateUrl/store.js";
  
  let usernameTranslation = $t('generateUrl.form.username');
  let passwordTranslation = $t('generateUrl.form.password');
  let teamIdTranslation = $t('generateUrl.form.teamId');

  let username = '';
  let password = '';
  let teamId = '';
  
  let invalidUsername: boolean | null = null;
  let invalidPassword: boolean | null = null;

  function clicked() {
    invalidUsername = username === '';
    invalidPassword = password === '';
  }
  
  function listTeams() {
    if (username !== '' && password !== '') fetchTeamsGet(username, password);
    
    clicked();
  }

  function generateUrl() {
    if (username !== '' && password !== '') {
      const data = dataToRequestParam(username, password, teamId);
      dataParams.set(data);
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
      <p>
        <span style="font-size: 2em; color: red; font-family: sans-serif">⚠</span>
        {$t('generateUrl.warning.logins')}
      </p>
      <p>
        {$t('generateUrl.warning.repository')}
        <a href="https://github.com/tbmc/sporteasy-calendar-connector">Github repo</a>
      </p>
      <p>{$t('generateUrl.warning.credentialsRequired')}</p>
    </div>
    <div>
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
      <label for="teamId">
        {teamIdTranslation}
        <input type="text" name="teamId" placeholder={teamIdTranslation} bind:value={teamId} />
      </label>
    </div>
  </div>

  <footer>
    <div class="grid">
      <div />
      <button class="secondary outline reset" on:click={reset}>{$t('generateUrl.form.buttonReset')}</button>
      <button class="secondary list-teams" on:click={listTeams} aria-busy={$fetchTeamsIsLoading}>
        {$t('generateUrl.form.buttonListTeams')}
      </button>
      <button class="generate" on:click={generateUrl}>
        {$t('generateUrl.form.buttonGenerate')}
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
</style>
