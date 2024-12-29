<template>
  <div class="video-card">
    <img :src="video.thumbnail" alt="thumbnail" class="thumbnail" />
    <div class="info">
      <h3 class="title">{{ video.title }}</h3>
    </div>
  </div>
</template>

<script>
export default {
  props: ['video'],
};
</script>

<style>
.video-card {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}
.thumbnail {
  width: 100%;
  height: auto;
}
.info {
  padding: 8px;
}
.title {
  font-size: 14px;
  font-weight: 500;
}
</style>
