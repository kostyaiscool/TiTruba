<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import connection from "@/api";

const router = useRouter();

const history = ref([]);

const loading = ref(true);

const error = ref("");

const loadHistory = async () => {
  try {
    loading.value = true;

    const response = await connection.get(
      "/history/history/"
    );

    history.value = response.data;

  } catch (err) {
    console.error(err);

    if (err.response?.status === 401) {
      error.value =
        "Войдите в аккаунт, чтобы посмотреть историю.";
    } else {
      error.value =
        "Ошибка загрузки истории.";
    }

  } finally {
    loading.value = false;
  }
};

const openVideo = (videoId) => {
  router.push(`/video/${videoId}`);
};

onMounted(loadHistory);
</script>

<template>
  <div class="history-page">

    <h1 class="page-title">
      История просмотра
    </h1>

    <div
      v-if="loading"
      class="status"
    >
      Загрузка...
    </div>

    <div
      v-else-if="error"
      class="status error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="history.length === 0"
      class="status"
    >
      История пуста
    </div>

    <div
      v-else
      class="history-list"
    >

      <div
        v-for="item in history"
        :key="item.id"
        class="history-card"
        @click="openVideo(item.video_id)"
      >

        <div class="video-avatar">
          ▶
        </div>

        <div class="history-info">

          <div class="video-id">
            Видео #{{ item.video_id }}
          </div>

          <div class="watch-date">
            {{
              new Date(
                item.created_at
              ).toLocaleString()
            }}
          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<style scoped>
.history-page {
  padding: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 24px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.history-card {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 14px;

  border-radius: 14px;

  background: #f5f5f5;

  cursor: pointer;

  transition: 0.2s;
}

.history-card:hover {
  background: #ececec;
}

.video-avatar {
  width: 56px;
  height: 56px;

  border-radius: 12px;

  background: red;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 24px;
}

.history-info {
  display: flex;
  flex-direction: column;
}

.video-id {
  font-size: 18px;
  font-weight: bold;
}

.watch-date {
  margin-top: 4px;
  color: gray;
  font-size: 14px;
}

.status {
  text-align: center;
  margin-top: 30px;
  font-size: 18px;
}

.error {
  color: red;
}
</style>