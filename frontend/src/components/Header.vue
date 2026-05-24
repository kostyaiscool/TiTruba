<template>
  <header class="header">
    <div class="logo">
      <a href="http://localhost:5173/">ТыТруба</a>
    </div>

    <SearchBar />
    <AuthAction />
  </header>
</template>

<script>
import SearchBar from './SearchBar.vue';
import AuthAction from './AuthActions.vue';

export default {
  components: {
    SearchBar,
    AuthAction,
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
</style>