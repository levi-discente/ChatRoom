<template>
  <div class="terminal">
    <h1>Salas Disponíveis</h1>
    <ul>
      <li v-for="room in rooms" :key="room.room_id">
        <router-link :to="`/rooms/${room.room_id}`">{{ room.name }}</router-link>
      </li>
    </ul>
    <button @click="createRoom">Criar Nova Sala</button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rooms: [],
      error: null
    };
  },
  async created() {
    this.error = null;
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        this.error = 'Você precisa estar logado para ver as salas.';
        this.$router.push('/login');
        return;
      }
      const response = await axios.get('http://127.0.0.1:8000/rooms', {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.rooms = response.data;
    } catch (error) {
      this.error = 'Falha ao carregar as salas. Tente novamente mais tarde.';
      console.error(error);
    }
  },
  methods: {
    async createRoom() {
      this.error = null;
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = 'Você precisa estar logado para criar uma sala.';
          this.$router.push('/login');
          return;
        }
        await axios.post(
          'http://127.0.0.1:8000/rooms',
          { name: `Sala ${Date.now()}` }, // Nome dinâmico para a sala
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.$router.go(0); // Recarrega a lista
      } catch (error) {
        this.error = 'Falha ao criar sala. Verifique suas permissões.';
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
