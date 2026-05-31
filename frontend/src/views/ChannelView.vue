<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

import connection from "@/api";

const route = useRoute();
const router = useRouter();

const videos = ref([]);

const loading = ref(true);
const error = ref(null);

const authorId = route.params.id;

const loadVideos = async () => {
  try {
    const response = await connection.get(
      `/videos/get_video_by_author/${authorId}`
    );

    videos.value = response.data;

  } catch (err) {
    console.error(err);

    error.value =
      "Не удалось загрузить канал";

  } finally {
    loading.value = false;
  }
};

const openVideo = (id) => {
  router.push(`/video/${id}`);
};

onMounted(loadVideos);
</script>

<template>
  <div class="channel-page">

    <h1 class="channel-title">
      Channel #{{ authorId }}
    </h1>

    <div
      v-if="loading"
      class="status"
    >
      Loading...
    </div>

    <div
      v-else-if="error"
      class="status error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="videos.length === 0"
      class="status"
    >
      На канале пока нет видео
    </div>

    <div
      v-else
      class="videos-grid"
    >

      <div
        v-for="video in videos"
        :key="video.id"
        class="video-card"
        @click="openVideo(video.id)"
      >

        <div class="thumbnail">
          🎥
        </div>

        <div class="video-info">

          <div class="video-title">
            {{ video.public_name }}
          </div>

          <div class="video-author">
            {{ video.author }}
          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<style scoped>
.channel-page {
  padding: 24px;
}

.channel-title {
  margin-bottom: 24px;
  font-size: 32px;
  font-weight: bold;
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(
    auto-fill,
    minmax(280px, 1fr)
  );
  gap: 20px;
}

.video-card {
  cursor: pointer;

  border-radius: 12px;
  overflow: hidden;

  background: #fff;

  box-shadow:
    0 2px 8px rgba(0,0,0,.1);

  transition: .2s;
}

.video-card:hover {
  transform: translateY(-3px);
}

.thumbnail {
  height: 160px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 48px;

  background: #eee;
}

.video-info {
  padding: 12px;
}

.video-title {
  font-weight: bold;
  margin-bottom: 6px;
}

.video-author {
  color: #666;
  font-size: 14px;
}

.status {
  text-align: center;
  padding: 40px;
}

.error {
  color: red;
}
</style>