<template>
  <div class="categories-page">
    <h2>Categories Management</h2>

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

    <div v-if="categories.length === 0" class="no-data">No categories found.</div>

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
        <tr v-for="cat in categories" :key="cat.id">
          <td>{{ cat.name }}</td>
          <td>{{ cat.code }}</td>
          <td>{{ cat.description }}</td>
          <td>
            <button @click="edit(cat)" class="btn small">Edit</button>
            <button @click="remove(cat.id)" class="btn danger small">Delete</button>
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
const categories = ref([])
const form = ref({ name: '', code: '', description: '', id: null })

const fetchCategories = async () => {
  try {
    const res = await apiRequest('/api/categories/')
    categories.value = res.results || res
  } catch (err) {
    alert('Failed to fetch categories: ' + err.message)
  }
}

const handleSubmit = async () => {
  try {
    if (form.value.id) {
      await apiRequest(`/api/categories/${form.value.id}/`, 'PATCH', form.value)
    } else {
      await apiRequest('/api/categories/', 'POST', form.value)
    }
    resetForm()
    await fetchCategories()
  } catch (err) {
    alert('Error: ' + err.message)
  }
}

const edit = (cat) => {
  form.value = { ...cat }
}

const resetForm = () => {
  form.value = { name: '', code: '', description: '', id: null }
}

const remove = async (id) => {
  if (!confirm('Are you sure you want to delete this category?')) return
  try {
    await apiRequest(`/api/categories/${id}/`, 'DELETE')
    await fetchCategories()
  } catch (err) {
    alert('Error: ' + err.message)
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.categories-page {
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
