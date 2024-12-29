<template>
  <div class="videos-grid">
    <VideoCard v-for="video in videos" :key="video.id" :video="video" />
  </div>
</template>

<script>
import VideoCard from '../components/VideoCard.vue';

export default {
  components: { VideoCard },
  data() {
    return {
      videos: [
        { id: '1', title: 'Video 1', thumbnail: 'thumb1.jpg' },
        { id: '2', title: 'Video 2', thumbnail: 'thumb2.jpg' },
      ],
    };
  },
};
</script>
