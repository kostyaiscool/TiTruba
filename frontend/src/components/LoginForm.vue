<template>
  <div class="login-form">
    <input
      type="text"
      placeholder="Username"
      class="login-input"
      v-model="username"
    />
    <input
      type="password"
      placeholder="Password"
      class="login-input"
      v-model="password"
    />
    <button class="login-button" @click="handleLogin">
      Login
    </button>
  </div>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      console.log("Username:", this.username);
      console.log("Password:", this.password);
      // тут потом добавишь API-запрос
    },
  },
};
</script>

<style>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 220px;
}

.login-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-button {
  padding: 8px 12px;
  background-color: #f00;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #c00;
}
</style>