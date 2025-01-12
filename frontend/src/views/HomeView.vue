<script setup>
import VideoCard from '../components/VideoCard.vue';

// Данные для видео
const videos = [
  { id: '1', title: 'Video 1', thumbnail: 'thumb1.jpg' },
  { id: '2', title: 'Video 2', thumbnail: 'thumb2.jpg' },
];
</script>

<template>
  <main class="videos-grid">
    <!-- Вывод списка карточек видео -->
    <VideoCard
      v-for="video in videos"
      :key="video.id"
      :video="video"
    />
  </main>
</template>

<style>
.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 16px;
}
</style>
