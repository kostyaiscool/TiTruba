<template>
  <div class="video-page">
    <h1>Video Page</h1>
    <p>Currently viewing video ID: {{ id }}</p>
    <!-- Загрузка и отображение контента на основе ID -->
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
  padding: 20px;
}
</style>
