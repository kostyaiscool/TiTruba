<template>
  <header class="header">
    <div class="logo"><a href='http://localhost:5173/'>ТыТруба</a></div>
    <SearchBar />
    <div class="user-actions">
      <NotificationBell />
      <UserMenu />
    </div>
  </header>
</template>

<script>
import SearchBar from './SearchBar.vue';
import NotificationBell from './NotificationBell.vue';
import UserMenu from './UserMenu.vue';

export default {
  components: {
    SearchBar,
    NotificationBell,
    UserMenu,
  },
};
</script>

<style>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  height: 56px;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}
</style>
