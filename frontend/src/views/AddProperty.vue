<!-- frontend/src/views/AddProperty.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'

const router = useRouter()
const propertiesStore = usePropertiesStore()

const form = ref({
  name: '',
  description: '',
  category: '',
  department: '',
  status: 'active',
  purchase_date: '',
  purchase_price: '',
  current_value: '',
  serial_number: '',
  property_code :'',
  brand: '',
  model: ''
})

const loading = ref(false)
const departments = computed(() => propertiesStore.departments)
const categories = computed(() => propertiesStore.categories)

const submitProperty = async () => {
  loading.value = true
  try {
    const payload = {}
    for (const [k, v] of Object.entries(form.value)) {
      if (v !== '') payload[k] = v
    }

    // Convert number fields from string to float
    if (payload.purchase_price) {
      payload.purchase_price = parseFloat(payload.purchase_price)
    }
    if (payload.current_value) {
      payload.current_value = parseFloat(payload.current_value)
    }

    await propertiesStore.addProperty(payload)
    alert('Property added successfully!')
    router.push('/properties')
  } catch (err) {
    console.error('💥 Error submitting property:', err)
    alert('Error adding property: ' + (err.response?.data?.detail || err.message))
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await propertiesStore.fetchDepartments()
  await propertiesStore.fetchCategories()
})
</script>

<!-- ✅ Make sure you have ONLY ONE template block -->
<template>
  <div class="add-property">
    <div class="form-header">
      <h1>Add New Property</h1>
      <router-link to="/properties" class="back-btn">← Back to Properties</router-link>
    </div>

    <form @submit.prevent="submitProperty" class="property-form">
      <!-- Name -->
      <div class="form-group">
        <label for="name">Property Name *</label>
        <input id="name" v-model="form.name" type="text" required />
      </div>

      <!-- Description -->
      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="form.description" rows="3" />
      </div>

      <!-- Category & Department -->
      <div class="form-row">
        <div class="form-group">
          <label for="category">Category *</label>
          <select id="category" v-model="form.category" required>
            <option value="">Select Category</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="department">Department *</label>
          <select id="department" v-model="form.department" required>
            <option value="">Select Department</option>
            <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
          </select>
        </div>
      </div>

      <!-- Status & Purchase Date -->
      <div class="form-row">
        <div class="form-group">
          <label for="status">Status</label>
          <select id="status" v-model="form.status">
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="under_maintenance">Under Maintenance</option>
          </select>
        </div>
        <div class="form-group">
          <label for="purchase_date">Purchase Date *</label>
          <input id="purchase_date" v-model="form.purchase_date" type="date" required />
        </div>
      </div>

      <!-- Price Fields -->
      <div class="form-row">
        <div class="form-group">
          <label for="purchase_price">Purchase Price *</label>
          <input id="purchase_price" v-model="form.purchase_price" type="number" step="0.01" required />
        </div>
        <div class="form-group">
          <label for="current_value">Current Value</label>
          <input id="current_value" v-model="form.current_value" type="number" step="0.01" />
        </div>
      </div>

      <!-- Serial, Brand, Model -->
      <div class="form-row">
        <div class="form-group">
    <label for="serial_number">Serial Number</label>
    <input
      id="serial_number"
      v-model="form.serial_number"
      type="text"
      autocomplete="off"
      maxlength="100"
    />
  </div>
        <div class="form-group">
    <label for="property_code">Property Code *</label>
    <input
      id="property_code"
      v-model="form.property_code"
      type="text"
      required
      autocomplete="off"
      maxlength="100"
    />
  </div>
        <div class="form-group">
          <label for="brand">Brand</label>
          <input id="brand" v-model="form.brand" type="text" />
        </div>
      </div>

      <div class="form-group">
        <label for="model">Model</label>
        <input id="model" v-model="form.model" type="text" />
      </div>

      <!-- Submit Buttons -->
      <div class="form-actions">
        <button type="button" @click="$router.go(-1)" class="cancel-btn">Cancel</button>
        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? 'Adding...' : 'Add Property' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.add-property {
  max-width: 800px;
  margin: 40px auto;
  padding: 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  font-family: sans-serif;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.form-header h1 {
  margin: 0;
  font-size: 24px;
}

.back-btn {
  color: #007bff;
  text-decoration: none;
}

.back-btn:hover {
  text-decoration: underline;
}

.property-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group label {
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.cancel-btn {
  padding: 10px 20px;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.cancel-btn:hover {
  background: #4b5563;
}

.submit-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.submit-btn:hover:not(:disabled) {
  background: #0056b3;
}

.submit-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
