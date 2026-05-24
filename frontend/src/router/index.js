import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import VideoView from '../views/VideoView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ProfileView from '../views/ProfileView.vue'
import UploadView from "../views/UploadView.vue";
import SubscriptionsView from "../views/SubscriptionsView.vue";
import ChannelView from "../views/ChannelView.vue"

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/video/:id', name: 'Video', component: VideoView, props: true },
  { path: '/login', name: 'Login', component: LoginView},
  { path: '/register', name: 'Register', component: RegisterView},
  { path: '/profile', name: 'Profile', component: ProfileView},
  { path: '/upload', name: 'Upload', component: UploadView},
  { path: "/subscriptions", component: SubscriptionsView},
  { path: "/channel/:id", component: ChannelView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;