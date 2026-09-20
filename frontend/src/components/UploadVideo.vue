<script setup>
import { ref, onMounted } from "vue";
import connection from "@/api";

const file = ref(null);
const title = ref("");
const description = ref("");

const loading = ref(false);
const message = ref(null);

const tags = ref([]);
const selectedTags = ref([]);
const showTagsModal = ref(false);


// =========================
// Файл
// =========================

const handleFileChange = (e) => {
  file.value = e.target.files[0] || null;
};


// =========================
// Загрузка тегов
// =========================

const loadTags = async () => {
  try {
    const response = await connection.get("/tags/all");

    console.log("Теги:", response.data);

    tags.value = response.data;
  } catch (err) {
    console.error("Ошибка загрузки тегов:", err);
  }
};


// =========================
// Выбор тегов
// =========================

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag.id);

  // Если уже выбран — убираем
  if (index !== -1) {
    selectedTags.value.splice(index, 1);
    return;
  }

  // Максимум 3
  if (selectedTags.value.length >= 3) {
    return;
  }

  selectedTags.value.push(tag.id);
};

const isSelected = (tag) => {
  return selectedTags.value.includes(tag.id);
};


// =========================
// Получение названий выбранных тегов
// =========================

const getSelectedTagNames = () => {
  return tags.value
    .filter((tag) => selectedTags.value.includes(tag.id))
    .map((tag) => tag.name);
};


// =========================
// Загрузка видео
// =========================

const uploadVideo = async () => {
  if (!file.value) {
    message.value = "Выбери видео";
    return;
  }

  if (!title.value.trim()) {
    message.value = "Введи название видео";
    return;
  }

  loading.value = true;
  message.value = null;

  try {
    const formData = new FormData();

    formData.append("video", file.value);
    formData.append("title", title.value);
    formData.append("description", description.value);

    // Передаём выбранные теги
    for (const tagId of selectedTags.value) {
      formData.append("tag_ids", tagId);
    }

    await connection.post(
      "/videos/video_upload",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    message.value = "Видео успешно загружено 🎉";

    // Очищаем форму
    file.value = null;
    title.value = "";
    description.value = "";
    selectedTags.value = [];

    // Сбрасываем input файла
    const fileInput = document.querySelector("#video-file");

    if (fileInput) {
      fileInput.value = "";
    }

  } catch (err) {
    console.error("Ошибка загрузки:", err);

    if (err.response?.data?.detail) {
      message.value = err.response.data.detail;
    } else {
      message.value = "Ошибка загрузки";
    }
  } finally {
    loading.value = false;
  }
};


// =========================
// При открытии страницы
// =========================

onMounted(() => {
  loadTags();
});
</script>


<template>
  <div class="upload-box">

    <h2>Загрузка видео</h2>


    <!-- Видео -->

    <input
      id="video-file"
      type="file"
      accept="video/*"
      @change="handleFileChange"
    />


    <!-- Название -->

    <input
      v-model="title"
      type="text"
      class="text-input"
      placeholder="Название видео"
    />


    <!-- Описание -->

    <textarea
      v-model="description"
      class="description-input"
      placeholder="Описание видео"
      rows="5"
    ></textarea>


    <!-- Теги -->

    <button
      type="button"
      class="tags-btn"
      @click="showTagsModal = true"
    >
      Выбрать теги
      ({{ selectedTags.length }}/3)
    </button>


    <!-- Выбранные теги -->

    <div
      v-if="selectedTags.length"
      class="selected-tags"
    >
      <span
        v-for="tagName in getSelectedTagNames()"
        :key="tagName"
        class="selected-tag"
      >
        #{{ tagName }}
      </span>
    </div>


    <!-- Загрузка -->

    <button
      type="button"
      class="upload-btn"
      @click="uploadVideo"
      :disabled="loading"
    >
      {{ loading ? "Uploading..." : "Upload Video" }}
    </button>


    <!-- Сообщение -->

    <p
      v-if="message"
      class="message"
    >
      {{ message }}
    </p>


    <!-- ========================= -->
    <!-- Модальное окно тегов -->
    <!-- ========================= -->

    <div
      v-if="showTagsModal"
      class="modal-overlay"
      @click.self="showTagsModal = false"
    >

      <div class="tags-modal">

        <h2>Выбери теги</h2>

        <p class="hint">
          Можно выбрать максимум 3 тега
        </p>


        <div class="tags-list">

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


        <p
          v-if="!tags.length"
          class="no-tags"
        >
          Теги не найдены
        </p>


        <button
          type="button"
          class="close-btn"
          @click="showTagsModal = false"
        >
          Готово
        </button>

      </div>

    </div>

  </div>
</template>


<style scoped>

.upload-box {
  width: 100%;
  max-width: 600px;

  margin: 30px auto;
  padding: 20px;

  display: flex;
  flex-direction: column;
  gap: 12px;
}

.upload-box h2 {
  margin: 0 0 10px;
}


/* ========================= */
/* Поля */
/* ========================= */

.text-input,
.description-input {
  width: 100%;
  box-sizing: border-box;

  padding: 10px;

  border: 1px solid #ccc;
  border-radius: 6px;

  font-size: 15px;
}

.description-input {
  resize: vertical;
}


/* ========================= */
/* Кнопки */
/* ========================= */

.upload-btn,
.tags-btn,
.close-btn {
  padding: 10px 14px;

  border: none;
  border-radius: 6px;

  cursor: pointer;

  font-size: 14px;
}

.upload-btn {
  background: #f00;
  color: white;
}

.upload-btn:hover {
  background: #c00;
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tags-btn {
  background: #eee;
  color: #222;
}

.tags-btn:hover {
  background: #ddd;
}


/* ========================= */
/* Выбранные теги */
/* ========================= */

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


/* ========================= */
/* Сообщение */
/* ========================= */

.message {
  margin: 0;

  font-size: 14px;
}


/* ========================= */
/* Модальное окно */
/* ========================= */

.modal-overlay {
  position: fixed;

  inset: 0;

  background: rgba(0, 0, 0, 0.55);

  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 1000;
}

.tags-modal {
  width: 500px;
  max-width: 90vw;
  max-height: 80vh;

  padding: 20px;

  background: white;

  border-radius: 10px;

  overflow-y: auto;
}

.tags-modal h2 {
  margin-top: 0;
}

.hint {
  color: #777;
  font-size: 14px;
}


/* ========================= */
/* Список тегов */
/* ========================= */

.tags-list {
  display: flex;
  flex-wrap: wrap;

  gap: 8px;

  margin: 20px 0;
}

.tag {
  padding: 8px 12px;

  border: 1px solid #ccc;
  border-radius: 20px;

  background: white;

  cursor: pointer;

  transition: 0.15s;
}

.tag:hover {
  background: #eee;
}

.tag.selected {
  background: #f00;
  color: white;

  border-color: #f00;
}

.no-tags {
  color: #777;
}


/* ========================= */
/* Готово */
/* ========================= */

.close-btn {
  width: 100%;

  background: #222;
  color: white;
}

.close-btn:hover {
  background: #000;
}

</style>