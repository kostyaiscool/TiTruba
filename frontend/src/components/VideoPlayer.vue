<script setup>
import { computed, ref } from "vue";
import connection from "@/api";

/*
  👇 props СНАЧАЛА
*/
const props = defineProps({
  videoId: {
    type: [String, Number],
    required: true,
  },

  author: {
    type: String,
    default: "Unknown",
  },
});

/*
  👇 текущий пользователь
*/
const currentUser = ref(
  localStorage.getItem("username")
);

/*
  👇 защита от подписки на себя
*/
const isOwnChannel = computed(() => {
  return (
    currentUser.value &&
    props.author &&
    currentUser.value === props.author
  );
});

/*
  🎥 видео URL
*/
const videoUrl = computed(() => {
  return `http://localhost:8000/videos/watch/${props.videoId}`;
});

/*
  🔔 состояние подписки
*/
const isSubscribed = ref(false);

/*
  🔔 подписка
*/
const toggleSubscribe = async () => {
  try {
    /*
      ❗ защита на уровне фронта (UI)
    */
    if (isOwnChannel.value) return;

    await connection.post(
      `/subscribers/subscribe/${props.author}`
    );

    isSubscribed.value =
      !isSubscribed.value;

  } catch (err) {
    console.error(err);
  }
};
</script>

<template>
  <div class="video-wrapper">

    <!-- 🎥 video -->
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

    <!-- 👤 meta -->
    <div class="video-meta">

      <div class="author-info">

        <div class="avatar">
          {{
            props.author?.[0]
              ?.toUpperCase()
          }}
        </div>

        <div>

          <div class="author-name">
            {{ props.author }}
          </div>

          <div class="subscribers">
            channel
          </div>

        </div>

      </div>

      <!-- 🔔 -->
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

.video-meta {
  margin-top: 18px;
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
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: red;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}

.author-name {
  font-size: 16px;
  font-weight: bold;
}

.subscribers {
  font-size: 13px;
  color: #777;
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
</style>