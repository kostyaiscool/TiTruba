<script setup>
import { ref, onMounted } from "vue";
import connection from "../api";
import VideoCard from "../components/VideoCard.vue";

const videos = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchVideos = async () => {
  try {
    const response = await connection.get("/videos"); // <-- эндпоинт
    videos.value = response.data;
  } catch (err) {
    error.value = "Ошибка загрузки видео";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchVideos();
});
</script>

<template>
  <main class="videos-grid">
    <p v-if="loading">Загрузка...</p>
    <p v-else-if="error">{{ error }}</p>

    <VideoCard
      v-else
      v-for="video in videos"
      :key="video.id"
      :video="video"
    />
  </main>
</template>

<style scoped>
.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 16px;
}
</style>