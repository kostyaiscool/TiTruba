<script setup>
const userId = localStorage.getItem("user_id");
</script>
<template>
  <aside class="sidebar">
    <nav>
      <ul>
        <li>Главная</li>
        <li>Тренды</li>
        <li>
        <router-link to="/subscriptions">
        Subscriptions
        </router-link>
        </li>
        <li>Библиотека</li>
        <li>
        <router-link :to="`/history/${userId}`">
  History
</router-link>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<style>
.sidebar {
  width: 240px;
  background-color: #f9f9f9;
  border-right: 1px solid #ddd;
}
nav ul {
  list-style: none;
  padding: 0;
}
nav ul li {
  padding: 12px 16px;
  cursor: pointer;
}
nav ul li:hover {
  background-color: #e6e6e6;
}
</style>
