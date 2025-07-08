<!-- frontend/src/components/RecentTransfers.vue -->
<template>
  <div class="recent-transfers">
    <div class="section-header">
      <h3>Recent Transfers</h3>
      <router-link to="/transfers" class="view-all-link">View All</router-link>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <span>Loading transfers...</span>
    </div>

    <div v-else-if="error" class="error-message">
      <span>{{ error }}</span>
      <button @click="fetchTransfers" class="retry-btn">Retry</button>
    </div>

    <div v-else-if="transfers.length === 0" class="no-transfers">
      <div class="no-data-icon">📦</div>
      <p>No recent transfers found</p>
    </div>

    <div v-else class="transfers-list">
      <div 
        v-for="transfer in displayedTransfers" 
        :key="transfer.id"
        class="transfer-item"
      >
        <div class="transfer-main">
          <div class="property-info">
            <h4 class="property-name">{{ transfer.property_name || 'Unknown Property' }}</h4>
            <span class="property-code">{{ transfer.property_code || 'N/A' }}</span>
          </div>
          
          <div class="transfer-direction">
            <div class="department from-dept">
              <span class="dept-label">From:</span>
              <span class="dept-name">{{ transfer.from_department_name || 'Unknown' }}</span>
            </div>
            <div class="arrow">→</div>
            <div class="department to-dept">
              <span class="dept-label">To:</span>
              <span class="dept-name">{{ transfer.to_department_name || 'Unknown' }}</span>
            </div>
          </div>
        </div>

        <div class="transfer-meta">
          <div class="transfer-date">
            <span class="date-icon">📅</span>
            <span>{{ formatDate(transfer.transfer_date) }}</span>
          </div>
          
          <div v-if="transfer.transferred_by_name" class="transferred-by">
            <span class="user-icon">👤</span>
            <span>{{ transfer.transferred_by_name }}</span>
          </div>
          
         
        </div>

        <div v-if="transfer.notes" class="transfer-notes">
          <span class="notes-icon">💬</span>
          <span class="notes-text">{{ transfer.notes }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

// Props
const props = defineProps({
  maxItems: {
    type: Number,
    default: 5
  }
})

// Reactive data
const authStore = useAuthStore()
const transfers = ref([])
const loading = ref(false)
const error = ref(null)

// Computed
const displayedTransfers = computed(() => {
  return transfers.value.slice(0, props.maxItems)
})

// Methods
const fetchTransfers = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch('http://localhost:8000/api/transfers/', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    
    // Sort by transfer_date descending (most recent first)
    transfers.value = (data.results || data).sort((a, b) => {
      return new Date(b.transfer_date) - new Date(a.transfer_date)
    })
    
    console.log('✅ Recent transfers loaded:', transfers.value.length)
    
  } catch (err) {
    console.error('❌ Error fetching transfers:', err)
    error.value = 'Failed to load recent transfers'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown date'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return 'Invalid date'
  }
}

// Lifecycle
onMounted(() => {
  fetchTransfers()
})
</script>

<style scoped>
.recent-transfers {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.section-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 18px;
  font-weight: 600;
}

.view-all-link {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.view-all-link:hover {
  color: #5a67d8;
}

/* Loading State */
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  color: #64748b;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e2e8f0;
  border-top: 2px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  color: #dc2626;
  text-align: center;
}

.retry-btn {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.2s ease;
}

.retry-btn:hover {
  background: #b91c1c;
}

/* No Data State */
.no-transfers {
  text-align: center;
  padding: 2rem;
  color: #64748b;
}

.no-data-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.no-transfers p {
  margin: 0;
  font-style: italic;
}

/* Transfers List */
.transfers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.transfer-item {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.transfer-item:hover {
  border-color: #667eea;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
}

.transfer-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
  gap: 1rem;
}

.property-info {
  flex: 1;
}

.property-name {
  margin: 0 0 0.25rem 0;
  color: #1e293b;
  font-size: 16px;
  font-weight: 600;
}

.property-code {
  color: #64748b;
  font-size: 12px;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.transfer-direction {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 2;
}

.department {
  text-align: center;
  min-width: 0;
}

.dept-label {
  display: block;
  font-size: 10px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.dept-name {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  word-wrap: break-word;
}

.from-dept .dept-name {
  color: #dc2626;
}

.to-dept .dept-name {
  color: #059669;
}

.arrow {
  color: #667eea;
  font-weight: bold;
  font-size: 16px;
  flex-shrink: 0;
}

.transfer-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.transfer-date,
.transferred-by {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.date-icon,
.user-icon {
  font-size: 12px;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-left: auto;
}

.status-completed {
  background: #dcfce7;
  color: #166534;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.transfer-notes {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 12px;
  color: #64748b;
  background: #f8fafc;
  padding: 0.5rem;
  border-radius: 4px;
}

.notes-icon {
  font-size: 12px;
  margin-top: 2px;
}

.notes-text {
  line-height: 1.4;
}

/* Responsive Design */
@media (max-width: 768px) {
  .transfer-main {
    flex-direction: column;
    align-items: stretch;
  }
  
  .transfer-direction {
    justify-content: space-between;
    margin-top: 0.75rem;
  }
  
  .department {
    flex: 1;
  }
  
  .transfer-meta {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .status {
    margin-left: 0;
  }
}

@media (max-width: 480px) {
  .recent-transfers {
    padding: 1rem;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .transfer-direction {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .arrow {
    transform: rotate(90deg);
  }
}
</style>
