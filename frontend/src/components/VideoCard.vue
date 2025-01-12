<template>
  <div class="video-card" @click="goToVideo">
    <img :src="video.thumbnail" alt="Thumbnail" class="thumbnail" />
    <h3 class="title">{{ video.title }}</h3>
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
  border: 1px solid #ddd;
  padding: 8px;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.2s;
}
.video-card:hover {
  transform: scale(1.05);
}
.thumbnail {
  width: 100%;
  border-radius: 8px;
}
.title {
  font-size: 16px;
  margin-top: 8px;
}
</style>
