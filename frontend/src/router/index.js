import { createRouter, createWebHistory } from 'vue-router';
import Content from '../views/HomeView.vue'; // Если Content.vue теперь маршрут
import VideoPage from '../views/VideoView.vue';

const routes = [
  { path: '/', name: 'Home', component: Content },
  { path: '/video/:id', name: 'Video', component: VideoPage, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
