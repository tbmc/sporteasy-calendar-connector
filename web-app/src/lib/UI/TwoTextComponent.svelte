<script lang="ts">
  export let originalText: string;
  export let otherText: string;

  let text1Element: HTMLSpanElement;
  let text2Element: HTMLSpanElement;

  export const animate = () => {
    text1Element.style.display = 'none';
    text2Element.style.display = 'inline';

    setTimeout(() => {
      text1Element.style.display = 'inline';
      text2Element.style.display = 'none';
    }, 2_000);
  };
</script>

<span bind:this={text1Element}>{originalText}</span>
<span bind:this={text2Element} style="display: none;">{otherText}</span>
