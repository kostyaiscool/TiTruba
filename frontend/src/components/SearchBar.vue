<template>
  <div class="search-bar">
    <input
      v-model="search"
      @keyup.enter="startSearch"
      type="text"
      placeholder="Поиск..."
      class="search-input"
    />

    <button
      class="search-button"
      @click="startSearch"
    >
      🔍
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const search = ref("");

const startSearch = () => {

  const query = search.value.trim();

  if (!query) return;

  router.push(`/search/${encodeURIComponent(query)}`);

};
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;

  width: 500px;
}

.search-input {
  flex: 1;

  padding: 8px 12px;

  border: 1px solid #ddd;
  border-radius: 20px;

  outline: none;

  font-size: 15px;
}

.search-input:focus {
  border-color: #ff0000;
}

.search-button {
  padding: 8px 16px;

  background-color: #ff0000;

  color: white;

  border: none;

  border-radius: 20px;

  cursor: pointer;

  transition: .2s;
}

.search-button:hover {
  background-color: #d60000;
}
</style>