<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const open = (route) => {
  router.push(route);
};
</script>

<template>
  <div class="library">

    <h1>Библиотека</h1>

    <div
      class="card"
      @click="open('/history')"
    >
      <div class="icon">🕒</div>

      <div>
        <h3>История</h3>
        <p>Просмотренные видео</p>
      </div>
    </div>

    <div
      class="card"
      @click="open('/liked')"
    >
      <div class="icon">👍</div>

      <div>
        <h3>Понравившиеся</h3>
        <p>Видео, которым вы поставили лайк</p>
      </div>
    </div>

    <div
      class="card"
      @click="open('/disliked')"
    >
      <div class="icon">👎</div>

      <div>
        <h3>Не понравившиеся</h3>
        <p>Видео с дизлайком</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
.library{
    max-width:900px;
    margin:auto;
    padding:30px;
}

.card{
    display:flex;
    align-items:center;
    gap:20px;

    padding:20px;

    margin-bottom:15px;

    border-radius:15px;

    background:#f5f5f5;

    cursor:pointer;

    transition:.2s;
}

.card:hover{
    background:#ececec;
}

.icon{
    font-size:35px;
}
</style>