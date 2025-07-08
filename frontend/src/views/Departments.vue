<template>
  <div class="departments-page">
    <h2>Departments Management</h2>

    <form @submit.prevent="handleSubmit" class="form">
      <input v-model="form.name" required placeholder="Name" class="input" />
      <input v-model="form.code" required placeholder="Code (unique)" class="input" />
      <input v-model="form.description" placeholder="Description" class="input" />
      <button type="submit" class="btn primary">
        {{ form.id ? "Update" : "Add" }}
      </button>
      <button v-if="form.id" type="button" @click="resetForm" class="btn secondary">
        Cancel
      </button>
    </form>

    <div v-if="departments.length === 0" class="no-data">
      No departments available.
    </div>

    <table v-else class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Code</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dept in departments" :key="dept.id">
          <td>{{ dept.name }}</td>
          <td>{{ dept.code }}</td>
          <td>{{ dept.description }}</td>
          <td>
            <button @click="edit(dept)" class="btn small">Edit</button>
            <button @click="remove(dept.id)" class="btn danger small">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { apiRequest } from '@/stores/properties'

const authStore = useAuthStore()
const departments = ref([])
const form = ref({ name: '', code: '', description: '', id: null })

const fetchDepartments = async () => {
  try {
    const res = await apiRequest('/api/departments/')
    departments.value = res.results || res
  } catch (err) {
    console.error('❌ Failed to fetch departments:', err.message)
  }
}

const handleSubmit = async () => {
  try {
    if (form.value.id) {
      await apiRequest(`/api/departments/${form.value.id}/`, 'PATCH', form.value)
    } else {
      await apiRequest('/api/departments/', 'POST', form.value)
    }
    resetForm()
    await fetchDepartments()
  } catch (err) {
    alert('Error: ' + err.message)
  }
}

const edit = (dept) => {
  form.value = { ...dept }
}

const resetForm = () => {
  form.value = { name: '', code: '', description: '', id: null }
}

const remove = async (id) => {
  if (!confirm('Are you sure you want to delete this department?')) return
  try {
    await apiRequest(`/api/departments/${id}/`, 'DELETE')
    await fetchDepartments()
  } catch (err) {
    alert('Error: ' + err.message)
  }
}

onMounted(() => {
  fetchDepartments()
})
</script>

<style scoped>
.departments-page {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

h2 {
  margin-bottom: 1.5rem;
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
}

.form {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.input {
  flex: 1 1 250px;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}
.btn.primary {
  background-color: #667eea;
  color: white;
}
.btn.primary:hover {
  background-color: #5a67d8;
}
.btn.secondary {
  background-color: #e2e8f0;
  color: #1a202c;
}
.btn.small {
  font-size: 0.85rem;
  padding: 0.3rem 0.7rem;
}
.btn.danger {
  background-color: #e53e3e;
  color: white;
}
.btn.danger:hover {
  background-color: #c53030;
}

.table {
  width: 100%;
  border-collapse: collapse;
}
.table th,
.table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}
.table th {
  background-color: #f1f5f9;
  font-weight: 600;
}

.no-data {
  padding: 2rem;
  text-align: center;
  font-style: italic;
  color: #64748b;
}
</style>
