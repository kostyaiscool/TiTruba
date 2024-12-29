<template>
  <div id="app">
    <Header />
    <div class="main-layout">
      <Sidebar />
      <Content />
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Sidebar from './components/Sidebar.vue';
import Content from './components/Content.vue';

export default {
  components: {
    Header,
    Sidebar,
    Content,
  },
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.main-layout {
  display: flex;
  flex: 1;
}
</style>
