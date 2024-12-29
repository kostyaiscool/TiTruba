<template>
  <div class="notification-bell">
    <button @click="toggleNotifications" class="bell-button">🔔</button>
    <div v-if="showNotifications" class="notifications-dropdown">
      <p>No new notifications</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotificationBell",
  data() {
    return {
      showNotifications: false,
    };
  },
  methods: {
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
    },
  },
};
</script>

<style>
.notification-bell {
  position: relative;
}
.bell-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
.notifications-dropdown {
  position: absolute;
  top: 36px;
  right: 0;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
