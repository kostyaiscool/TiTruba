<script setup>
import LoginForm from '../components/LoginForm.vue';


</script>

<template>
  <main class="login">
    <!-- Вывод списка карточек видео -->
    <LoginForm/>
  </main>
</template>

<style>
.login {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  padding: 16px;
}
</style>
