import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import VideoView from '../views/VideoView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/video/:id', name: 'Video', component: VideoView, props: true },
  { path: '/login', name: 'Login', component: LoginView},
  { path: '/register', name: 'Register', component: RegisterView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;