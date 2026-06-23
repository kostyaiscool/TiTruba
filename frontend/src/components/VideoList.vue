<script setup>
import { ref, onMounted } from "vue";
import connection from "@/api";

const videos = ref([]);
const page = ref(1);
const loading = ref(false);

const loadVideos = async () => {
  try {
    loading.value = true;

    const response = await connection.get(
      `/videos/videos/${page.value}`
    );

    videos.value = response.data;

  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const nextPage = async () => {
  page.value++;
  await loadVideos();
};

const prevPage = async () => {
  if (page.value <= 1) return;

  page.value--;
  await loadVideos();
};

onMounted(loadVideos);
</script>

<template>
  <div class="video-list">

    <div
      v-if="loading"
      class="loading"
    >
      Загрузка...
    </div>

    <div
      v-else
      class="videos-grid"
    >

      <router-link
        v-for="video in videos"
        :key="video.id"
        :to="`/video/${video.id}`"
        class="video-card"
      >

        <video
          class="preview-video"
          muted
          preload="metadata"
        >
          <source
            :src="`http://localhost:8000/videos/watch/${video.id}`"
            :type="video.content_type || 'video/mp4'"
          />
        </video>

        <div class="video-info">

          <div class="video-title">
            {{ video.public_name }}
          </div>

          <div class="video-author">
            {{ video.author }}
          </div>

        </div>

      </router-link>

    </div>

    <div class="pagination">

      <button
        @click="prevPage"
        :disabled="page === 1"
      >
        ← Назад
      </button>

      <span>
        Страница {{ page }}
      </span>

      <button
        @click="nextPage"
      >
        Вперёд →
      </button>

    </div>

  </div>
</template>

<style scoped>
.video-list {
  width: 100%;
}

.loading {
  text-align: center;
  padding: 40px;
}

.videos-grid {
  display: grid;
  grid-template-columns:
    repeat(auto-fill, minmax(320px, 1fr));

  gap: 20px;
}

.video-card {
  text-decoration: none;
  color: inherit;
}

.preview-video {
  width: 100%;
  height: 220px;

  object-fit: cover;

  border-radius: 12px;

  background: black;
}

.video-info {
  margin-top: 10px;
}

.video-title {
  font-size: 16px;
  font-weight: bold;
}

.video-author {
  margin-top: 4px;

  font-size: 14px;
  color: #777;
}

.pagination {
  margin-top: 30px;

  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.pagination button {
  padding: 8px 14px;

  border: none;
  border-radius: 8px;

  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: default;
}
</style>