<template>
  <div class="terminal">
    <h1>Registrar</h1>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Registrar</button>
    </form>
    <p>Já tem uma conta? <router-link to="/login">Faça login aqui</router-link></p>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      message: null,
      error: null
    };
  },
  methods: {
    async register() {
      this.message = null;
      this.error = null;
      try {
        await axios.post('http://127.0.0.1:8000/users', {
          username: this.username,
          password: this.password,
        });
        this.message = 'Usuário registrado com sucesso! Faça login.';
        this.$router.push('/login');
      } catch (error) {
        this.error = 'Erro ao registrar. Por favor, tente novamente.';
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.message {
  color: green;
}

.error {
  color: red;
}
</style>
