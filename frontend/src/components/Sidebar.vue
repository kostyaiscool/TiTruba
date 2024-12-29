<template>
  <aside class="sidebar">
    <nav>
      <ul>
        <li>Главная</li>
        <li>Тренды</li>
        <li>Подписки</li>
        <li>Библиотека</li>
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
