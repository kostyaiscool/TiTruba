<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute(); // Получение ID из маршрута
const videoId = ref(route.params.id); // ID видео
const videoUrl = ref(null); // Ссылка на поток видео
const isLoading = ref(true); // Флаг загрузки
const error = ref(null); // Флаг ошибки

onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:8000/videos/watch/${videoId.value}`, {
      responseType: 'blob', // Получение данных как blob
    });
    videoUrl.value = URL.createObjectURL(response.data); // Создание локальной ссылки на видео
  } catch (err) {
    error.value = 'Failed to load video.';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="video-page">
    <div v-if="isLoading" class="loading">
      <p>Loading video...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    <div v-else>
      <video class="video-player" controls autoplay>
        <source :src="videoUrl" type="video/webm" />
        Your browser does not support the video tag.
      </video>
    </div>
  </div>
</template>

<style>
.video-page {
  padding: 16px;
}
.video-player {
  width: 100%;
  max-width: 800px;
  margin-bottom: 16px;
}
.loading, .error {
  text-align: center;
  padding: 16px;
}
</style>
