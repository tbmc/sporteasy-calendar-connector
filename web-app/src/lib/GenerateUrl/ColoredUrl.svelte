<script lang="ts">
  export let origin: string;
  export let disableSaveLogin: boolean;
  export let data: string;
</script>

<span class="origin-color">{origin}</span><span class="default-color">/api?</span><span
  class="disable-save-login-color">{disableSaveLogin ? 'disable_save_login=true' : ''}</span
><span class="default-color">{disableSaveLogin ? '&' : ''}</span><span class="data-color"
  >data={data}</span
>

<style>
  .default-color {
    color: black;
  }

  .origin-color {
    color: blue;
  }

  .disable-save-login-color {
    color: red;
  }

  .data-color {
    color: green;
  }
</style>
