<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

import connection from "@/api";

const route = useRoute();

const videos = ref([]);

const loading = ref(true);

const authorId = route.params.id;

const loadVideos = async () => {
  try {
    const response =
      await connection.get(
        `/videos/get_video_by_author/${authorId}`
      );

    videos.value = response.data;

  } catch (err) {
    console.error(err);

  } finally {
    loading.value = false;
  }
};

onMounted(loadVideos);
</script>

<template>

  <div class="channel-page">

    <h1>
      Channel
    </h1>

    <div v-if="loading">
      Loading...
    </div>

    <div
      v-else
      class="videos-grid"
    >

      <VideoCard
        v-for="video in videos"
        :key="video.id"
        :video="video"
      />

    </div>

  </div>

</template>

<style scoped>
.channel-page {
  padding: 24px;
}

.channel-header {
  display: flex;
  align-items: center;
  gap: 18px;

  margin-bottom: 30px;
}

.channel-avatar {
  width: 82px;
  height: 82px;

  border-radius: 50%;

  background: red;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 32px;
  font-weight: bold;
}

.channel-name {
  font-size: 32px;
  font-weight: bold;
}

.channel-subtitle {
  color: #777;
}

.videos-grid {
  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(260px, 1fr));

  gap: 20px;
}

.status {
  padding: 40px;
  text-align: center;
}

.error {
  color: red;
}
</style>