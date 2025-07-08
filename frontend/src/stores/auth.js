// frontend/src/stores/auth.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const accessToken = ref(localStorage.getItem("access_token"));
  const refreshToken = ref(localStorage.getItem("refresh_token"));

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);

  const login = async (credentials) => {
    try {
      const response = await fetch(`${API_BASE}/api/auth/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
      }

      const data = await response.json();

      // Store tokens
      accessToken.value = data.access;
      refreshToken.value = data.refresh;
      user.value = data.user;

      // Store in localStorage
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      localStorage.setItem("user", JSON.stringify(data.user));

      return data;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await fetch(`${API_BASE}/api/auth/logout/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken.value}`,
          },
          body: JSON.stringify({ refresh: refreshToken.value }),
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      // Clear everything
      accessToken.value = null;
      refreshToken.value = null;
      user.value = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
    }
  };

  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error("No refresh token available");
      }

      const response = await fetch(`${API_BASE}/api/auth/token/refresh/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh: refreshToken.value }),
      });

      if (!response.ok) {
        throw new Error("Token refresh failed");
      }

      const data = await response.json();
      accessToken.value = data.access;
      localStorage.setItem("access_token", data.access);

      return data.access;
    } catch (error) {
      console.error("Token refresh error:", error);
      // If refresh fails, logout
      await logout();
      throw error;
    }
  };

  const initializeAuth = () => {
    const storedUser = localStorage.getItem("user");
    const storedAccessToken = localStorage.getItem("access_token");
    const storedRefreshToken = localStorage.getItem("refresh_token");

    if (storedUser && storedAccessToken && storedRefreshToken) {
      try {
        user.value = JSON.parse(storedUser);
        accessToken.value = storedAccessToken;
        refreshToken.value = storedRefreshToken;
      } catch (error) {
        console.error("Error parsing stored user data:", error);
        logout();
      }
    }
  };

  // Initialize on store creation
  initializeAuth();

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    login,
    logout,
    refreshAccessToken,
    initializeAuth,
  };
});
