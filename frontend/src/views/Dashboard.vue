<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>داشبورد مديريت كالاها</h1>
      <div class="user-info">
        <span class="farsi-greeting">
  خوش آمديد {{ authStore.user?.first_name || authStore.user?.username }}😊
</span>

        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </header>

    <div class="stats-grid">
      <router-link to="/properties" class="card-link">
      <div class="stat-card">
        <h3>Total Properties</h3>
        <p class="stat-number">{{ stats.total_properties }}</p>
      </div>
      </router-link>
      <div class="stat-card">
        <h3>Active Properties</h3>
        <p class="stat-number">{{ stats.active_properties }}</p>
      </div>

      <div class="stat-card clickable" @click="goToDepartments">
        <h3>Departments</h3>
        <p class="stat-number">{{ stats.total_departments }}</p>
      </div>
      <div class="stat-card clickable" @click="goToCategories">
  <h3>Categories</h3>
  <p class="stat-number">{{ stats.total_categories || 0 }}</p>
</div>

    </div>

    <RecentTransfers :max-items="5" />

    <div class="dashboard-actions">

      <router-link to="/properties/add" class="action-btn">Add Property</router-link>
      <router-link to="/transfers" class="action-btn">View Transfers</router-link>
      <router-link v-if="authStore.isAdmin" to="/admin" class="action-btn admin-btn">Admin Panel</router-link>
    </div>

    <div class="department-chart">
      <h3>Properties by Department</h3>
      <div v-if="Object.keys(stats.properties_by_department).length === 0" class="no-data">
        No department data available
      </div>
      <div v-else class="chart-container">
        <div
          v-for="(count, dept) in stats.properties_by_department"
          :key="dept"
          class="chart-bar"
        >
          <div class="bar-label">{{ dept }}</div>
          <div class="bar" :style="{ width: `${maxDeptCount > 0 ? (count / maxDeptCount) * 100 : 0}%` }">
            {{ count }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import RecentTransfers from '@/components/RecentTransfers.vue'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref({
  total_properties: 0,
  active_properties: 0,
  total_departments: 0,
  recent_transfers: 0,
  properties_by_department: {}
})

const maxDeptCount = computed(() => {
  const values = Object.values(stats.value.properties_by_department)
  return values.length > 0 ? Math.max(...values) : 0
})

const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/dashboard/stats/', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      stats.value = data
    } else {
      console.error('❌ Failed to fetch stats:', response.statusText)
    }
  } catch (error) {
    console.error('💥 Error fetching stats:', error)
  }
}

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}

const goToDepartments = () => {
  router.push('/departments')
}
const goToCategories = () => {
  router.push('/categories')
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  background: #f8fafc;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-bottom: 2px solid #e2e8f0;
}

.dashboard-header h1 {
  margin: 0;
  color: #1e293b;
  font-size: 24px;
  font-weight: 700;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info span {
  color: #64748b;
  font-weight: 500;
}

.logout-btn {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}
.logout-btn:hover {
  background: #dc2626;
  transform: translateY(-1px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
}
.stat-card h3 {
  margin: 0 0 1rem 0;
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
}
.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  margin: 0;
}

.clickable {
  cursor: pointer;
  transition: all 0.2s ease;
}
.clickable:hover {
  transform: translateY(-2px);
  background: #edf2f7;
}

.dashboard-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}
.action-btn {
  background: #667eea;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}
.action-btn:hover {
  background: #5a67d8;
  transform: translateY(-1px);
}
.admin-btn {
  background: #38b2ac;
}
.admin-btn:hover {
  background: #319795;
}

.department-chart {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.chart-bar {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}
.bar-label {
  width: 180px;
  text-align: right;
  margin-right: 1rem;
  font-size: 0.9rem;
  color: #374151;
}
.bar {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  min-width: 40px;
  text-align: center;
  font-weight: 600;
  transition: all 0.2s ease;
}
.bar:hover {
  transform: scale(1.02);
}

.no-data {
  text-align: center;
  color: #64748b;
  padding: 2rem;
  font-style: italic;
}
.farsi-greeting {
  direction: rtl;
  font-family: "Vazirmatn", Tahoma, sans-serif;
  font-weight: 600;
  font-size: 1.1rem;
  color: #2d3748;
  background-color: #edf2f7;
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  display: inline-block;
  line-height: 1.4;
}


</style>
