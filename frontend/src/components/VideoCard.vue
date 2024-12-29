<template>
  <div class="video-card" @click="goToVideo">
    <img :src="video.thumbnail" alt="Thumbnail" />
    <h3>{{ video.title }}</h3>
  </div>
</template>

<script>
export default {
  props: {
    video: {
      type: Object,
      required: true,
    },
  },
  methods: {
    goToVideo() {
      this.$router.push({ name: 'Video', params: { id: this.video.id } });
    },
  },
};
</script>

<style>
.video-card {
  cursor: pointer;
}
</style>
