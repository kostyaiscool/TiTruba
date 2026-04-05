<template>
  <header class="header">
    <div class="logo">
      <a href="http://localhost:5173/">ТыТруба</a>
    </div>

    <SearchBar />

    <div class="auth-actions">
      <a href="/login" class="auth-button login">Login</a>
      <a href="/register" class="auth-button register">Register</a>
    </div>
  </header>
</template>

<script>
import SearchBar from './SearchBar.vue';

export default {
  components: {
    SearchBar,
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  height: 56px;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}

.auth-actions {
  display: flex;
  gap: 8px;
}

.auth-button {
  padding: 6px 12px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  cursor: pointer;
}

.login {
  border: 1px solid #ddd;
  color: #333;
}

.register {
  background-color: #f00;
  color: #fff;
}

.register:hover {
  background-color: #c00;
}
</style>