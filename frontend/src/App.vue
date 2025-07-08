<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav class="fancy-navbar">
      <!-- Logo -->
      <RouterLink to="/" class="logo-link" aria-label="Home">
        <img
          alt="Logo"
          class="logo-img"
          src="@/assets/logo.jpg"
          width="48"
          height="48"
        />
      </RouterLink>

      <ul class="nav-links">
        <li><RouterLink to="/" exact-active-class="active">Home</RouterLink></li>
        <li><RouterLink to="/about" exact-active-class="active">About</RouterLink></li>
        <li><RouterLink to="/properties" exact-active-class="active">Properties</RouterLink></li>
        <li><RouterLink to="/categories" exact-active-class="active">Categories</RouterLink></li>
        <li><RouterLink to="/departments" exact-active-class="active">Departments</RouterLink></li>
      </ul>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
.fancy-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  padding: 1rem 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin: 1.5rem auto 2.5rem;
  max-width: 960px;
  border: 1px solid #e2e8f0;
  position: relative;
  z-index: 10;
}

.logo-link {
  text-decoration: none;
  display: flex;
  align-items: center;
}

.logo-img {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  object-fit: cover;
  border: 2px solid #e0e0e0;
  background-color: #f1f5f9;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.logo-link:hover .logo-img {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.nav-links {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 0.5rem;
}

.nav-links li {
  margin: 0 0.4rem;
}

.nav-links a {
  color: #334155;
  background: transparent;
  padding: 0.45rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.nav-links a:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.nav-links a.active {
  color: #1e40af;
  font-weight: 600;
  position: relative;
}

.nav-links a.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 10%;
  width: 80%;
  height: 2px;
  background-color: #1e40af;
  border-radius: 2px;
}


@media (max-width: 600px) {
  .fancy-navbar {
    flex-direction: column;
    align-items: stretch;
    padding: 1rem;
    border-radius: 0 0 16px 16px;
    gap: 1rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.3rem;
  }

  .logo-img {
    margin-bottom: 0.5rem;
    width: 44px;
    height: 44px;
  }
}
</style>
