<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

import connection from "@/api";
import VideoPlayer from "@/components/VideoPlayer.vue";

const route = useRoute();

const videoId = route.params.id;

const video = ref(null);

const loadVideo = async () => {
  try {
    const response = await connection.get(
      `/videos/video_info/${videoId}`
    );

    video.value = response.data;

  } catch (err) {
    console.error(err);
  }
};

onMounted(loadVideo);
</script>

<template>
  <div class="video-page">

    <VideoPlayer
      :video-id="videoId"
      :author="author"
    />

  </div>
</template>

<style scoped>
.video-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>