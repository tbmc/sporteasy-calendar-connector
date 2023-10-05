<script>
  import { t } from 'svelte-i18n';

  import { dataToRequestParam } from './dataToRequestParam';
  import { fetchTeamsGet, fetchTeamsIsLoading, dataParams } from './store';

  import Loader from './Loader.svelte';

  let usernameTranslation = $t('generateUrl.form.username');
  let passwordTranslation = $t('generateUrl.form.password');
  let teamIdTranslation = $t('generateUrl.form.teamId');

  let username = '';
  let password = '';
  let teamId = '';

  function listTeams() {
    clickedOnce = true;
    if (username !== '' && password !== '') fetchTeamsGet(username, password);
  }

  function generateUrl() {
    if (username !== '' && password !== '') {
      const data = dataToRequestParam(username, password, teamId);
      dataParams.set(data);
    }
  }

  function reset() {
    username = '';
    password = '';
    teamId = '';

    clickedOnce = true;
  }

  let clickedOnce = false;
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
          aria-invalid={clickedOnce && username === ''}
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
          aria-invalid={clickedOnce && password === ''}
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
      <a href="#" role="button" class="secondary outline reset" on:click={reset}
        >{$t('generateUrl.form.buttonReset')}</a
      >
      <a href="#" role="button" class="secondary list-teams" on:click={listTeams}>
        {#if $fetchTeamsIsLoading}
          <Loader />
        {:else}
          {$t('generateUrl.form.buttonListTeams')}
        {/if}
      </a>
      <a href="#" role="button" class="generate" on:click={generateUrl}>
        {$t('generateUrl.form.buttonGenerate')}
      </a>
      <div />
    </div>
  </footer>
</article>
