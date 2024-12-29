<template>
  <div class="video-page">
    <h1>Video Page</h1>
    <p>Video ID: {{ id }}</p>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: String,
      required: true,
    },
  },
};
</script>

<style>
.video-page {
  padding: 16px;
}
</style>
