<template>
  <div class="search-bar">
    <input type="text" placeholder="Search..." class="search-input" />
    <button class="search-button">🔍</button>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
};
</script>

<style>
.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}
.search-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.search-button {
  padding: 8px 12px;
  background-color: #f00;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.search-button:hover {
  background-color: #c00;
}
</style>
