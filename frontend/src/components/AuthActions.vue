<script setup>
import { useAuth } from "@/composables/useAuth";

const { isLoggedIn, user, logout } = useAuth();
</script>

<template>
  <div class="auth-actions">

    <!-- ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ -->
    <router-link
      v-if="isLoggedIn"
      to="/upload"
      class="btn primary"
    >
      Upload
    </router-link>

    <!-- НЕ ЗАЛОГИНЕН -->
    <template v-if="!isLoggedIn">
      <router-link to="/login" class="btn ghost">
        Login
      </router-link>

      <router-link to="/register" class="btn primary">
        Register
      </router-link>
    </template>

    <!-- ЗАЛОГИНЕН -->
    <template v-else>

      <router-link
        to="/profile"
        class="profile-btn"
      >
        <div class="avatar">
          {{ user?.username?.[0]?.toUpperCase() || "U" }}
        </div>

        <span>
          {{ user?.username || "Profile" }}
        </span>
      </router-link>

      <button class="btn danger" @click="logout">
        Logout
      </button>

    </template>

  </div>
</template>

<style scoped>
.auth-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn {
  padding: 6px 14px;
  border-radius: 8px;
  border: none;
  text-decoration: none;
  cursor: pointer;
  font-size: 14px;
}

.primary {
  background: red;
  color: white;
}

.ghost {
  background: transparent;
  border: 1px solid #ddd;
  color: #333;
}

.danger {
  background: #333;
  color: white;
}

.profile-btn {
  display: flex;
  align-items: center;
  gap: 8px;

  padding: 5px 10px;

  background: #f5f5f5;
  border-radius: 999px;

  text-decoration: none;
  color: #333;
}

.avatar {
  width: 28px;
  height: 28px;

  border-radius: 50%;

  background: red;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;
}
</style>