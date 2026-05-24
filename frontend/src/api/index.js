import axios from "axios";
import config from "../config";
export const connection = axios.create({
  baseURL: config.API_BASE_URL,
});
connection.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    console.log(token)
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);
export default connection;