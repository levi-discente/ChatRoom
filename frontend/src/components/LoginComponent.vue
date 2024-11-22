<template>
  <div class="terminal">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
    <p>Não tem uma conta? <router-link to="/register">Registre-se aqui</router-link></p>
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
      error: null
    };
  },
  methods: {
    async login() {
      this.error = null; // Limpa erros anteriores
      try {
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);

        const response = await axios.post('http://127.0.0.1:8000/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/rooms');
      } catch (error) {
        this.error = 'Falha no login: Verifique suas credenciais.';
        console.error(error.response?.data || error.message);
      }
    }
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
