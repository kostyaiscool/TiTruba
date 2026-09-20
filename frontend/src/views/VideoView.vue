<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

import connection from "@/api";
import VideoPlayer from "@/components/VideoPlayer.vue";

const route = useRoute();

const videoId = route.params.id;

const video = ref(null);

const loading = ref(true);
const error = ref(null);

const loadVideo = async () => {
  try {
    const response = await connection.get(
      `/videos/video_info/${videoId}`
    );

    video.value = response.data;

  } catch (err) {
    console.error(err);

    error.value = "Не удалось загрузить видео";

  } finally {
    loading.value = false;
  }
};

onMounted(loadVideo);
</script>

<template>
  <div class="video-page">

    <!-- Загрузка -->
    <div
      v-if="loading"
      class="status"
    >
      Загрузка...
    </div>

    <!-- Ошибка -->
    <div
      v-else-if="error"
      class="status error"
    >
      {{ error }}
    </div>

    <!-- Видео -->
    <VideoPlayer
  :video-id="videoId"
/>

  </div>
</template>

<style scoped>
.video-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.status {
  padding: 50px;
  text-align: center;
  font-size: 18px;
}

.error {
  color: red;
}
</style>
