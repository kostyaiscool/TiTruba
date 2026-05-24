<script setup>
import { ref } from "vue";
import connection from "@/api";

const title = ref("");
const description = ref("");
const file = ref(null);

const loading = ref(false);
const error = ref(null);

const handleFileChange = (event) => {
  file.value = event.target.files[0];
};

const uploadVideo = async () => {
  if (!file.value) {
    error.value = "Выбери видео";
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    const formData = new FormData();

    formData.append("video", file.value);
    formData.append("title", title.value);
    formData.append("description", description.value);

    await connection.post(
      "/videos/video_upload",
      formData
    );

    alert("Видео загружено!");

  } catch (err) {
    console.error(err);
    error.value = "Ошибка загрузки";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="upload-page">
    <div class="upload-card">

      <h1>Upload Video</h1>

      <input
        v-model="title"
        type="text"
        placeholder="Название"
        class="upload-input"
      />

      <textarea
        v-model="description"
        placeholder="Описание"
        class="upload-textarea"
      />

      <input
        type="file"
        accept="video/*"
        @change="handleFileChange"
      />

      <button
        class="upload-button"
        @click="uploadVideo"
        :disabled="loading"
      >
        {{ loading ? "Uploading..." : "Upload" }}
      </button>

      <p v-if="error" class="error">
        {{ error }}
      </p>

    </div>
  </div>
</template>

<style scoped>
.upload-page {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.upload-card {
  width: 500px;

  background: white;
  padding: 20px;

  border-radius: 12px;

  display: flex;
  flex-direction: column;
  gap: 12px;
}

.upload-input,
.upload-textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.upload-textarea {
  min-height: 120px;
}

.upload-button {
  padding: 10px;
  background: red;
  color: white;

  border: none;
  border-radius: 8px;

  cursor: pointer;
}

.error {
  color: red;
}
</style>