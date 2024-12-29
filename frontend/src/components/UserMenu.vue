<template>
  <div class="user-menu">
    <!-- Аватар пользователя -->
    <img
      src="https://via.placeholder.com/40"
      alt="User Avatar"
      class="user-avatar"
      @click="toggleMenu"
    />
    <!-- Выпадающее меню -->
    <div v-if="menuOpen" class="menu-dropdown">
      <ul>
        <li @click="goToProfile">Profile</li>
        <li @click="goToSettings">Settings</li>
        <li @click="signOut">Sign Out</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserMenu",
  data() {
    return {
      menuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    goToProfile() {
      console.log("Go to Profile");
    },
    goToSettings() {
      console.log("Go to Settings");
    },
    signOut() {
      console.log("Sign Out");
    },
  },
};
</script>

<style>
.user-menu {
  position: relative;
  display: inline-block;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}

.menu-dropdown {
  position: absolute;
  top: 50px;
  right: 0;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.menu-dropdown ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu-dropdown ul li {
  padding: 12px 16px;
  cursor: pointer;
}

.menu-dropdown ul li:hover {
  background-color: #f0f0f0;
}
</style>
