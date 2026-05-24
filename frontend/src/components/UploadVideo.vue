<script setup>
import { ref } from "vue";
import connection from "@/api";

const file = ref(null);
const loading = ref(false);
const message = ref(null);

const handleFileChange = (e) => {
  file.value = e.target.files[0];
};

const uploadVideo = async () => {
  if (!file.value) {
    message.value = "Выбери файл";
    return;
  }

  loading.value = true;
  message.value = null;

  try {
    const formData = new FormData();
    formData.append("video", file.value); // 👈 имя должно совпадать с FastAPI

    await connection.post("/videos/video_upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    message.value = "Видео успешно загружено 🎉";
    file.value = null;
  } catch (err) {
    console.error(err);
    message.value = "Ошибка загрузки";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="upload-box">
    <input type="file" @change="handleFileChange" />

    <button class="upload-btn" @click="uploadVideo" :disabled="loading">
      {{ loading ? "Uploading..." : "Upload Video" }}
    </button>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<style scoped>
.upload-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
}

.upload-btn {
  padding: 8px 12px;
  background: #f00;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.upload-btn:hover {
  background: #c00;
}

.message {
  font-size: 14px;
}
</style>