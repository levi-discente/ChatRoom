<template>
  <div>
    <h1>Bem-vindo ao Chat Terminal</h1>
    <div v-if="!isLoggedIn">
      <h2>Login ou Cadastro</h2>
      <form @submit.prevent="handleAuth">
        <label for="username">Usuário:</label>
        <input type="text" id="username" v-model="username" required />

        <label for="password">Senha:</label>
        <input type="password" id="password" v-model="password" required />

        <button type="submit">{{ isRegistering ? 'Cadastrar' : 'Entrar' }}</button>
      </form>
      <button @click="toggleAuthMode">
        {{ isRegistering ? 'Já possui uma conta? Faça login' : 'Não possui uma conta? Cadastre-se' }}
      </button>
    </div>

    <div v-else>
      <h2>Salas Disponíveis</h2>
      <ul>
        <li v-for="room in rooms" :key="room.id" @click="joinRoom(room.id)">
          {{ room.name }}
        </li>
      </ul>
      <button @click="createRoom">Criar Nova Sala</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      isLoggedIn: false,
      isRegistering: false,
      username: "",
      password: "",
      rooms: [],
    };
  },
  methods: {
    async handleAuth() {
      try {
        const endpoint = this.isRegistering ? "/users" : "/login";
        const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (!response.ok) {
          throw new Error("Falha na autenticação.");
        }

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        this.isLoggedIn = true;
        this.fetchRooms();
      } catch (error) {
        alert(error.message);
      }
    },
    toggleAuthMode() {
      this.isRegistering = !this.isRegistering;
    },
    async fetchRooms() {
      try {
        const response = await fetch("http://127.0.0.1:8000/rooms", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!response.ok) {
          throw new Error("Falha ao carregar as salas.");
        }

        this.rooms = await response.json();
      } catch (error) {
        alert(error.message);
      }
    },
    async createRoom() {
      const roomName = prompt("Digite o nome da nova sala:");
      if (!roomName) return;

      try {
        const response = await fetch("http://127.0.0.1:8000/rooms", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({ name: roomName }),
        });

        if (!response.ok) {
          throw new Error("Falha ao criar a sala.");
        }

        this.fetchRooms();
      } catch (error) {
        alert(error.message);
      }
    },
    joinRoom(roomId) {
      this.$router.push(`/room/${roomId}`);
    },
  },
  created() {
    const token = localStorage.getItem("token");
    if (token) {
      this.isLoggedIn = true;
      this.fetchRooms();
    }
  },
};
</script>

<style scoped>
h1 {
  color: #0f0;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button {
  background: none;
  border: 1px solid #0f0;
  color: #0f0;
  padding: 5px 10px;
  cursor: pointer;
}

button:hover {
  background: #0f0;
  color: #000;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  cursor: pointer;
  margin: 5px 0;
  padding: 5px;
  border: 1px solid #0f0;
}

li:hover {
  background: #0f0;
  color: #000;
}
</style>
