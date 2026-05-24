<script setup>
import { ref, onMounted } from "vue";
import connection from "../api";
import VideoCard from "../components/VideoCard.vue";

const videos = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchVideos = async () => {
  try {
    const response = await connection.get("/videos/videos");
    videos.value = response.data;
  } catch (err) {
    error.value = "Не удалось загрузить видео 😢";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchVideos);
</script>

<template>
  <main class="page">
    <div class="container">
      
      <!-- Skeleton loading -->
      <div v-if="loading" class="videos-grid">
        <div v-for="n in 8" :key="n" class="skeleton-card"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <!-- Videos -->
      <div v-else class="videos-grid">
        <VideoCard
          v-for="video in videos"
          :key="video.id"
          :video="video"
        />
      </div>

    </div>
  </main>
</template>

<style scoped>
.page {
  background: #f9f9f9;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.videos-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(6, 1fr);
}

/* ноуты */
@media (max-width: 1400px) {
  .videos-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

/* планшеты */
@media (max-width: 1100px) {
  .videos-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* маленькие */
@media (max-width: 800px) {
  .videos-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* телефоны */
@media (max-width: 500px) {
  .videos-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Skeleton */
.skeleton-card {
  width: 100%;
  aspect-ratio: 16 / 12;
  border-radius: 12px;
  background: linear-gradient(
    90deg,
    #eee 25%,
    #ddd 37%,
    #eee 63%
  );
  background-size: 400% 100%;
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 100% 0;
  }
  100% {
    background-position: -100% 0;
  }
}

/* Error */
.error {
  text-align: center;
  color: #c00;
  font-size: 18px;
  margin-top: 40px;
}
</style>
