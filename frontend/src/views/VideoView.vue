<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

import connection from "@/api";
import VideoPlayer from "@/components/VideoPlayer.vue";

const route = useRoute();

const videoId = Number(route.params.id);

const author = ref("Unknown");

const loadAuthor = async () => {
  try {
    const response = await connection.get(
      `/videos/info/${videoId}`
    );

    author.value =
      response.data.author;

  } catch (err) {
    console.error(err);
  }
};

onMounted(loadAuthor);
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