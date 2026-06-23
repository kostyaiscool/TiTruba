<script setup>
import { ref, computed, onMounted } from "vue";
import connection from "@/api";

const props = defineProps({
  videoId: {
    type: [String, Number],
    required: true,
  },
});

const currentUser = ref(
  localStorage.getItem("username")
);

const videoInfo = ref(null);

const isSubscribed = ref(false);

const videoUrl = computed(() => {
  return `http://localhost:8000/videos/watch/${props.videoId}`;
});

const isOwnChannel = computed(() => {
  return (
    currentUser.value &&
    videoInfo.value?.author &&
    currentUser.value === videoInfo.value.author
  );
});

const loadVideoInfo = async () => {
  try {
    const response = await connection.get(
      `/videos/video_info/${props.videoId}`
    );

    videoInfo.value = response.data;

    console.log(response.data);
  } catch (err) {
    console.error(err);
  }
};

const toggleSubscribe = async () => {
  try {
    if (isOwnChannel.value) return;

    await connection.post(
      `/subscribers/subscribe/${videoInfo.value.author}`
    );

    isSubscribed.value = !isSubscribed.value;
  } catch (err) {
    console.error(err);
  }
};

onMounted(loadVideoInfo);
</script>

<template>
  <div
    v-if="videoInfo"
    class="video-wrapper"
  >
    <video
      class="video-player"
      controls
      autoplay
    >
      <source
        :src="videoUrl"
        type="video/mp4"
      />
    </video>

    <h1 class="video-title">
      {{ videoInfo.title }}
    </h1>

    <div class="video-stats">
      👁 {{ videoInfo.views }} просмотров
    </div>

    <div class="video-meta">

      <div class="author-info">

        <div class="avatar">
          {{
            videoInfo.author?.[0]
              ?.toUpperCase()
          }}
        </div>

        <div>

          <div class="author-name">
            {{ videoInfo.author }}
          </div>

          <div class="video-date">
            {{
              new Date(
                videoInfo.created_at
              ).toLocaleDateString()
            }}
          </div>

        </div>

      </div>

      <button
        v-if="!isOwnChannel"
        class="subscribe-btn"
        :class="{
          subscribed: isSubscribed
        }"
        @click="toggleSubscribe"
      >
        {{
          isSubscribed
            ? "Subscribed"
            : "Subscribe"
        }}
      </button>

    </div>

    <div class="description-box">
      {{ videoInfo.description }}
    </div>

  </div>
</template>

<style scoped>
.video-wrapper {
  width: 100%;
}

.video-player {
  width: 100%;
  max-height: 700px;

  border-radius: 16px;
  background: black;
}

.video-title {
  margin-top: 18px;

  font-size: 24px;
  font-weight: bold;
}

.video-stats {
  margin-top: 8px;

  color: #666;
}

.video-meta {
  margin-top: 20px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 50px;
  height: 50px;

  border-radius: 50%;

  background: red;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-weight: bold;
  font-size: 20px;
}

.author-name {
  font-weight: bold;
}

.video-date {
  color: #777;
  font-size: 13px;
}

.subscribe-btn {
  padding: 10px 18px;

  border: none;
  border-radius: 999px;

  background: red;
  color: white;

  cursor: pointer;

  font-weight: bold;
}

.subscribe-btn.subscribed {
  background: #ddd;
  color: #333;
}

.description-box {
  margin-top: 20px;

  padding: 16px;

  border-radius: 12px;

  background: #f5f5f5;

  white-space: pre-wrap;
}
</style>