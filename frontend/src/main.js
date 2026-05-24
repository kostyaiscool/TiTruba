import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { onMounted } from "vue";
import { useAuth } from "@/composables/useAuth";


const app = createApp(App);
const { checkAuth } = useAuth();

app.use(router);
app.mount('#app');

onMounted(() => {
  checkAuth();
});