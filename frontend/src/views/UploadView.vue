<script setup>
import { ref, onMounted } from "vue";
import connection from "@/api";

const title = ref("");
const description = ref("");
const file = ref(null);

const tags = ref([]);
const selectedTags = ref([]);
const showTagModal = ref(false);

const loading = ref(false);
const error = ref(null);

const handleFileChange = (event) => {
  file.value = event.target.files[0];
};

const loadTags = async () => {
  try {
    const response = await connection.get("/tags/all");
    tags.value = response.data;
  } catch (err) {
    console.error("Ошибка загрузки тегов:", err);
  }
};

const toggleTag = (tag) => {
  const index = selectedTags.value.findIndex(
    (id) => id === tag.id
  );

  if (index !== -1) {
    selectedTags.value.splice(index, 1);
    return;
  }

  if (selectedTags.value.length >= 3) {
    return;
  }

  selectedTags.value.push(tag.id);
};

const isSelected = (tag) => {
  return selectedTags.value.includes(tag.id);
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

    for (const tagId of selectedTags.value) {
      formData.append("tag_ids", tagId);
    }

    await connection.post(
      "/videos/video_upload",
      formData
    );

    alert("Видео загружено!");

    title.value = "";
    description.value = "";
    file.value = null;
    selectedTags.value = [];

  } catch (err) {
    console.error(err);
    error.value = "Ошибка загрузки";
  } finally {
    loading.value = false;
  }
};

onMounted(loadTags);
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
        type="button"
        class="tag-button"
        @click="showTagModal = true"
      >
        Выбрать теги
        <span v-if="selectedTags.length">
          ({{ selectedTags.length }}/3)
        </span>
      </button>

      <div
        v-if="selectedTags.length"
        class="selected-tags"
      >
        <span
          v-for="tagId in selectedTags"
          :key="tagId"
          class="selected-tag"
        >
          {{
            tags.find(tag => tag.id === tagId)?.name
          }}
        </span>
      </div>

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

    <!-- Модальное окно тегов -->
    <div
      v-if="showTagModal"
      class="modal-overlay"
      @click.self="showTagModal = false"
    >
      <div class="tag-modal">

        <h2>Выбери теги</h2>

        <p class="tag-limit">
          Можно выбрать до 3 тегов
        </p>

        <div class="tag-list">
          <button
            v-for="tag in tags"
            :key="tag.id"
            type="button"
            class="tag"
            :class="{ selected: isSelected(tag) }"
            @click="toggleTag(tag)"
          >
            {{ tag.name }}
          </button>
        </div>

        <button
          type="button"
          class="close-button"
          @click="showTagModal = false"
        >
          Готово
        </button>

      </div>
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

.upload-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tag-button {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.selected-tag {
  padding: 5px 9px;
  background: #eee;
  border-radius: 15px;
  font-size: 13px;
}

.error {
  color: red;
}

/* modal */

.modal-overlay {
  position: fixed;
  inset: 0;

  background: rgba(0, 0, 0, 0.45);

  display: flex;
  align-items: center;
  justify-content: center;

  z-index: 1000;
}

.tag-modal {
  width: 450px;
  max-height: 70vh;

  background: white;
  border-radius: 12px;

  padding: 20px;

  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tag-limit {
  color: #777;
  margin: 0;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  overflow-y: auto;
  max-height: 350px;
}

.tag {
  padding: 8px 12px;

  border: 1px solid #ddd;
  border-radius: 20px;

  background: white;
  cursor: pointer;
}

.tag.selected {
  background: #e60000;
  color: white;
  border-color: #e60000;
}

.close-button {
  padding: 10px;

  border: none;
  border-radius: 8px;

  background: #222;
  color: white;

  cursor: pointer;
}
</style>