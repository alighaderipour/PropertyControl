<template>
  <div class="about-page">
    <section class="hero">
      <h1>About This App</h1>
      <p class="subtitle">
        A modern property management system for departments and categories—built with Django & Vue.
      </p>
    </section>

    <section class="content">
      <h2>📦 Features</h2>
      <ul>
        <li>Department & Category Management</li>
        <li>Property Tracking with Transfer Logs</li>
        <li>User Roles: Admin and Regular</li>
        <li>Dashboard with Real-Time Stats</li>
        <li>JWT-based Authentication</li>
        <li>Responsive UI with Vue & Pinia</li>
      </ul>

      <h2>💡 Purpose</h2>
      <p>
        This platform is designed to help organizations track and manage their assets across multiple
        departments, making it easier to monitor changes, assignments, and usage over time.
      </p>

      <h2>🛠️ Tech Stack</h2>
      <div class="tech-tags">
        <span>Vue 3</span>
        <span>Pinia</span>
        <span>Django</span>
        <span>Django REST Framework</span>
        <span>SQL Server</span>
      </div>
    </section>
  </div>
</template>

<script setup>
// no logic needed for static page
</script>

<style scoped>
.about-page {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
}

.hero {
  text-align: center;
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 2.4rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.1rem;
  color: #475569;
}

.content h2 {
  font-size: 1.4rem;
  color: #334155;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
}

.content p {
  font-size: 1rem;
  line-height: 1.6;
  color: #4b5563;
}

ul {
  padding-left: 1.5rem;
  list-style: disc;
  margin-bottom: 1.5rem;
}

ul li {
  margin-bottom: 0.5rem;
  color: #374151;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.tech-tags span {
  background-color: #f1f5f9;
  color: #334155;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
}
</style>
