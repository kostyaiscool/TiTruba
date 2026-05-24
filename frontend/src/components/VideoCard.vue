<template>
  <div class="video-card" @click="goToVideo">
    <div class="thumbnail-wrapper">
      <img :src="video.thumbnail" alt="Thumbnail" class="thumbnail" />
    </div>

    <div class="info">
      <h3 class="title">{{ video.title }}</h3>
      <p class="meta">{{ video.public_name }}</p>
    </div>
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

<style scoped>
.video-card {
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  transition: transform 0.2s, box-shadow 0.2s;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #000;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info {
  padding: 10px;
  text-align: left;
}

.title {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  line-height: 1.3;

  /* обрезка длинных заголовков */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  font-size: 12px;
  color: #777;
  margin-top: 6px;
}
</style>