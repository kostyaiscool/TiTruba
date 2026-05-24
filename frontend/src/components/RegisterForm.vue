<template>
  <div class="register-form">
    <input
      type="email"
      placeholder="Email"
      class="register-input"
      v-model="email"
    />

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

    <button class="register-button" @click="handleRegister" :disabled="loading">
      {{ loading ? "Loading..." : "Register" }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import connection from "../api";

export default {
  data() {
    return {
      email: "",
      username: "",
      password: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    async handleRegister() {
      this.loading = true;
      this.error = null;

      try {
        const response = await connection.post("/auth/auth/register", {
          email: this.email,
          password: this.password,
          username: this.username
        });

        const token = response.data.token;

        if (token) {
          localStorage.setItem("token", token);
          connection.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${token}`;
        }

        this.$router.push("/");
      } catch (err) {
        console.error(err);
        this.error =
          err.response?.data?.detail || "Ошибка регистрации";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>