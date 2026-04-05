<template>
  <div class="register-form">
    <input
      type="text"
      placeholder="Username"
      class="register-input"
      v-model="username"
    />
    <input
      type="password"
      placeholder="Password"
      class="register-input"
      v-model="password"
    />
    <button class="register-button" @click="handleRegister">
      Register
    </button>
  </div>
</template>

<script>
export default {
  name: "RegisterForm",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleRegister() {
      console.log("Username:", this.username);
      console.log("Password:", this.password);
      // тут потом добавишь API-запрос
    },
  },
};
</script>

<style>
.register-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 220px;
}

.register-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.register-button {
  padding: 8px 12px;
  background-color: #f00;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #c00;
}
</style>