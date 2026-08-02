<template>
  <canvas
    ref="canvas"
    class="thumbnail"
  ></canvas>

  <video
    ref="video"
    :src="videoSrc"
    style="display:none"
    muted
    preload="metadata"
  ></video>
</template>

<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  videoSrc: String,
});

const video = ref(null);
const canvas = ref(null);

onMounted(() => {

  video.value.addEventListener("loadeddata", () => {

    video.value.currentTime = 1;

  });

  video.value.addEventListener("seeked", () => {

    const ctx = canvas.value.getContext("2d");

    canvas.value.width = 320;
    canvas.value.height = 180;

    ctx.drawImage(
      video.value,
      0,
      0,
      320,
      180
    );

  });

});
</script>

<style scoped>
.thumbnail{
    width:320px;
    border-radius:10px;
}
</style>