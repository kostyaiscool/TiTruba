<script setup>
import { useAuth } from "@/composables/useAuth";

const { user } = useAuth();
</script>

<template>
  <div class="profile-page">
    <div class="profile-card">

      <!-- Аватар -->
      <div class="avatar">
        {{ user?.username?.[0]?.toUpperCase() || "U" }}
      </div>

      <!-- Инфо -->
      <h2 class="username">
        {{ user?.username || "User" }}
      </h2>

      <p class="email">
        {{ user?.email || "no-email@example.com" }}
      </p>

      <!-- Статы (заглушка) -->
      <div class="stats">
        <div class="stat">
          <span class="number">0</span>
          <span class="label">Videos</span>
        </div>
        <div class="stat">
          <span class="number">0</span>
          <span class="label">Subscribers</span>
        </div>
      </div>

      <!-- Кнопки -->
      <div class="actions">
        <button class="btn ghost">Edit profile</button>
        <button class="btn danger">Delete account</button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.profile-page {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  background: #f9f9f9;
  min-height: 100vh;
}

.profile-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

/* Аватар */
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #f00;
  color: #fff;
  font-size: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

/* Имя */
.username {
  margin: 0;
  font-size: 20px;
}

/* Email */
.email {
  color: #777;
  font-size: 14px;
  margin-top: 4px;
}

/* Статы */
.stats {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

.stat {
  display: flex;
  flex-direction: column;
}

.number {
  font-weight: bold;
  font-size: 18px;
}

.label {
  font-size: 12px;
  color: #777;
}

/* Кнопки */
.actions {
  display: flex;
  gap: 10px;
}

.btn {
  flex: 1;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
}

/* edit */
.ghost {
  background: #eee;
}

/* delete */
.danger {
  background: #f00;
  color: #fff;
}

.danger:hover {
  background: #c00;
}
</style>