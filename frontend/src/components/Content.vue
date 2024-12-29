<template>
  <main class="content">
    <div class="videos-grid">
      <VideoCard v-for="video in videos" :key="video.id" :video="video" />
    </div>
  </main>
</template>

<script>
import VideoCard from './VideoCard.vue';

export default {
  components: { VideoCard },
  data() {
    return {
      videos: [
        { id: 1, title: 'Видео 1', thumbnail: 'thumb1.jpg' },
        { id: 2, title: 'Видео 2', thumbnail: 'thumb2.jpg' },
      ],
    };
  },
};
</script>

<style>
.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}
.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}
</style>
