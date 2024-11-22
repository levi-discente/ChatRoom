import { createRouter, createWebHistory } from 'vue-router';
import LoginComponent from '@/components/LoginComponent.vue';
import RegisterComponent from '@/components/RegisterComponent.vue';
import RoomList from '@/components/RoomList.vue';
import ChatRoom from '@/components/ChatRoom.vue';
import HomeView from '@/views/HomeView.vue';

const routes = [
  { path: '/', name: 'HomeView', component: HomeView },
  { path: '/login', name: 'Login', component: LoginComponent },
  { path: '/register', name: 'Register', component: RegisterComponent },
  { path: '/rooms', name: 'Rooms', component: RoomList },
  { path: '/rooms/:id', name: 'ChatRoom', component: ChatRoom, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;


