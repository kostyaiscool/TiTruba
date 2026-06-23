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

    <button
      class="login-button"
      @click="handleLogin"
      :disabled="loading"
    >
      {{ loading ? "Loading..." : "Login" }}
    </button>

    <p
      v-if="error"
      class="error"
    >
      {{ error }}
    </p>
  </div>
</template>

<script>
import connection from "../api";
import { useAuth } from "@/composables/useAuth";

export default {
  name: "LoginForm",

  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: null,
    };
  },

  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;

      try {
        const formData = new FormData();

        formData.append(
          "username",
          this.username
        );

        formData.append(
          "password",
          this.password
        );

        const response = await connection.post(
          "/auth/auth/login",
          formData
        );

        const token =
          response.data.access_token;

        const { login } = useAuth();

        await login(token);

        connection.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${token}`;

        /*
          👇 получаем текущего пользователя
        */
        const me = await connection.get(
          "/users/me"
        );

        localStorage.setItem(
          "user_id",
          me.data.id
        );

        localStorage.setItem(
          "username",
          me.data.username
        );

        console.log(
          "Current user:",
          me.data
        );

        this.$router.push("/");

      } catch (err) {
        console.error(err);

        this.error =
          "Неверный логин или пароль";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
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

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error {
  color: #c00;
  font-size: 14px;
}
</style>