<script setup>
import RegisterForm from '../components/RegisterForm.vue';


</script>

<template>
  <main class="register">
    <!-- Вывод списка карточек видео -->
    <RegisterForm/>
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
