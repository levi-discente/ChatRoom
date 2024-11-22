<template>
  <div class="terminal">
    <h1>Sala: {{ roomName }}</h1>
    <div class="messages">
      <p v-for="msg in messages" :key="msg.id">{{ msg.sender }}: {{ msg.content }}</p>
    </div>
    <form @submit.prevent="sendMessage">
      <input v-model="newMessage" placeholder="Digite sua mensagem" />
      <button type="submit">Enviar</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['id'],
  data() {
    return { roomName: '', messages: [], newMessage: '' };
  },
  async created() {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/rooms/${this.id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      this.roomName = response.data.name;
      this.messages = response.data.messages;
    } catch (error) {
      console.error('Failed to fetch room details', error);
    }
  },
  methods: {
    async sendMessage() {
      try {
        const response = await axios.post(
          `http://127.0.0.1:8000/rooms/${this.id}/message/`,
          {
            room_id: this.room_id,
            username: this.username, // Certifique-se de que esta variável está definida no componente
            content: this.newMessage,
          },
          {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          }
        );
        this.messages.push(response.data);
        this.newMessage = '';
      } catch (error) {
        console.error('Failed to send message', error);
      }
    },
  },
};
</script>
