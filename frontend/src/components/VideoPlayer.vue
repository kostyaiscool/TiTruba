<script setup>
import { ref, computed, onMounted } from "vue";
import connection from "@/api";

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

const currentUser = ref(
  localStorage.getItem("username")
);

const isSubscribed = ref(false);

const likes = ref(0);
const dislikes = ref(0);

const videoInfo = ref({
  title: "",
  description: "",
  author: "",
  views: 0,
  created_at: null,
});

const isOwnChannel = computed(() => {
  return (
    currentUser.value &&
    props.author &&
    currentUser.value === props.author
  );
});

const videoUrl = computed(() => {
  return `http://localhost:8000/videos/watch/${props.videoId}`;
});

const loadVideoInfo = async () => {
  try {
    const response =
      await connection.get(
        `/videos/video_info/${props.videoId}`
      );

    videoInfo.value = response.data;
  } catch (err) {
    console.error(err);
  }
};

const loadRating = async () => {
  try {
    const response =
      await connection.get(
        `/likes/rating/${props.videoId}`
      );

    likes.value =
      response.data.likes;

    dislikes.value =
      response.data.dislikes;

  } catch (err) {
    console.error(err);
  }
};

const likeVideo = async () => {
  try {
    await connection.post(
      `/likes/like/${props.videoId}`
    );

    await loadRating();

  } catch (err) {
    console.error(err);
  }
};

const dislikeVideo = async () => {
  try {
    await connection.post(
      `/likes/dislike/${props.videoId}`
    );

    await loadRating();

  } catch (err) {
    console.error(err);
  }
};

const toggleSubscribe = async () => {
  try {
    if (isOwnChannel.value)
      return;

    await connection.post(
      `/subscribers/subscribe/${props.author}`
    );

    isSubscribed.value =
      !isSubscribed.value;

  } catch (err) {
    console.error(err);
  }
};

onMounted(async () => {
  await loadVideoInfo();
  await loadRating();
});
</script>

<template>
  <div class="video-wrapper">

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

    <!-- название -->
    <h1 class="video-title">
      {{ videoInfo.title }}
    </h1>

    <!-- просмотры -->
    <div class="video-stats">

      <span>
        👁
        {{ videoInfo.views }}
        просмотров
      </span>

      <span>
        📅
        {{
          videoInfo.created_at
            ? new Date(
                videoInfo.created_at
              ).toLocaleDateString()
            : ""
        }}
      </span>

    </div>

    <!-- лайки -->
    <div class="rating-panel">

      <button
        class="like-btn"
        @click="likeVideo"
      >
        👍 {{ likes }}
      </button>

      <button
        class="dislike-btn"
        @click="dislikeVideo"
      >
        👎 {{ dislikes }}
      </button>

    </div>

    <!-- автор -->
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

          <div class="subscribers">
            channel
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

    <!-- описание -->
    <div class="description-box">

      <h3>
        Описание
      </h3>

      <p>
        {{
          videoInfo.description ||
          "Описание отсутствует"
        }}
      </p>

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
  margin-top: 16px;
  font-size: 24px;
  font-weight: bold;
}

.video-stats {
  margin-top: 8px;

  display: flex;
  gap: 18px;

  color: #777;
}

.rating-panel {
  display: flex;
  gap: 12px;

  margin-top: 16px;
}

.like-btn,
.dislike-btn {
  border: none;

  border-radius: 999px;

  padding: 10px 18px;

  cursor: pointer;

  font-weight: bold;
}

.like-btn {
  background: #e8ffe8;
}

.dislike-btn {
  background: #ffe8e8;
}

.video-meta {
  margin-top: 24px;

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
  margin-top: 24px;

  background: #f5f5f5;

  padding: 16px;

  border-radius: 12px;
}

.description-box h3 {
  margin-bottom: 10px;
}
</style>