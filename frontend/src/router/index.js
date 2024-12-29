import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomeView.vue';
import VideoPage from '../views/VideoView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/video/:id',
    name: 'Video',
    component: VideoPage,
    props: true, // Передаем параметры маршрута как свойства компонента
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
