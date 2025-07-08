<template>
  <div class="login-container" dir="rtl">
    <div class="login-card">
      <h2>سیستم مدیریت کالا</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">نام کاربری</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">کلمه عبور</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            required
            :disabled="loading"
          />
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? "در حال ورود..." : "ورود" }}
        </button>

        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  username: "",
  password: "",
});

const loading = ref(false);
const error = ref("");

const handleLogin = async () => {
  loading.value = true;
  error.value = "";

  try {
    await authStore.login(form.value);
    router.push("/dashboard");
  } catch (err) {
    error.value = "نام کاربری یا رمز عبور اشتباه است";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  direction: rtl;  /* <--- Forces RTL layout for all children */
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
  text-align: right;  /* <--- Align labels and inputs to right side */
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  text-align: right;  /* <--- */
}
input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  text-align: right; /* <--- For RTL input */
  direction: rtl;    /* <--- Explicit RTL for text fields */
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 1rem;
}

button:hover:not(:disabled) {
  background: #5a67d8;
}

button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

.error {
  color: #e53e3e;
  margin-top: 1rem;
  text-align: center;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2d3748;
}
</style>
