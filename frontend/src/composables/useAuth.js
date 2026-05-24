import { ref } from "vue";
import connection from "@/api";

const isLoggedIn = ref(false);
const user = ref(null);
const loading = ref(true);
const error = ref(null);

// 🔍 Проверка авторизации при старте
const checkAuth = async () => {
  const token = localStorage.getItem("token");
  console.log(token)
  console.log("И.В.Илья здесь был")
  if (token) {
    try {
      const response = await connection.get("/users/me");
      user.value = response.data;
      isLoggedIn.value = true;
    } catch (err) {
      console.error("Auth check failed:", err);
      await logout();
    }
  }

  loading.value = false;
};

// 🔐 Логин (принимает токен)
const login = async (token) => {
  localStorage.setItem("token", token);

  // сразу в axios
  connection.defaults.headers.common[
    "Authorization"
  ] = `Bearer ${token}`;

  try {
    const response = await connection.get("/users/me");
    user.value = response.data;
    isLoggedIn.value = true;
    error.value = null;
  } catch (err) {
    await logout();
    throw err;
  }
};

// 🚪 Логаут
const logout = async () => {
  try {
    await connection.post("/auth/logout");
  } catch (err) {
    if (err.response?.status !== 401) {
      console.error("Logout error:", err);
    }
  } finally {
    localStorage.removeItem("token");
    user.value = null;
    isLoggedIn.value = false;
  }
};

// 📝 Регистрация
const register = async (userData) => {
  try {
    const response = await connection.post("/auth/register", userData);
    return response.data;
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Registration failed";
    throw err;
  }
};

// 🔑 Сброс пароля
const resetPassword = async (token, newPassword) => {
  try {
    await connection.post("/auth/reset-password", {
      token,
      password: newPassword,
    });
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Password reset failed";
    throw err;
  }
};

// 🔄 Обновить юзера
const refreshUser = async () => {
  try {
    const response = await connection.get("/users/me");
    user.value = response.data;
  } catch (err) {
    console.error("Failed to refresh user:", err);
    await logout();
  }
};

export function useAuth() {
  return {
    isLoggedIn,
    user,
    loading,
    error,
    checkAuth,
    login,
    logout,
    register,
    resetPassword,
    refreshUser,
  };
}