<!-- frontend/src/views/AllTransfers.vue -->
<template>
    <div class="all-transfers">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">All Property Transfers</h1>
          <p class="page-subtitle">Manage and track property transfers across departments</p>
        </div>
        <div class="header-actions">
          <router-link to="/transfers/add" class="btn btn-primary">
            <span class="btn-icon">➕</span>
            New Transfer
          </router-link>
        </div>
      </div>
  
      <!-- Filters & Controls -->
      <div class="controls-section">
        <div class="filters-row">
          <!-- Search -->
          <div class="search-group">
            <div class="search-input-wrapper">
              <span class="search-icon">🔍</span>
              <input
                v-model="searchQuery"
                type="search"
                placeholder="Search by property name, code, or notes..."
                class="search-input"
                @input="debouncedSearch"
              />
              <button 
                v-if="searchQuery" 
                @click="clearSearch" 
                class="clear-search-btn"
                title="Clear search"
              >
                ✕
              </button>
            </div>
          </div>
  
          <!-- Department Filters -->
          <div class="filter-group">
            <label class="filter-label">From Department:</label>
            <select v-model="filters.fromDepartment" class="filter-select">
              <option value="">All Departments</option>
              <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                {{ dept.name }}
              </option>
            </select>
          </div>
  
          <div class="filter-group">
            <label class="filter-label">To Department:</label>
            <select v-model="filters.toDepartment" class="filter-select">
              <option value="">All Departments</option>
              <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                {{ dept.name }}
              </option>
            </select>
          </div>
  
          <!-- Date Range -->
          <div class="filter-group">
            <label class="filter-label">Date Range:</label>
            <div class="date-range">
              <input 
                v-model="filters.dateFrom" 
                type="date" 
                class="date-input"
                title="From date"
              />
              <span class="date-separator">to</span>
              <input 
                v-model="filters.dateTo" 
                type="date" 
                class="date-input"
                title="To date"
              />
            </div>
          </div>
  
          <!-- Clear Filters -->
          <button 
            @click="clearAllFilters" 
            class="btn btn-outline"
            :disabled="!hasActiveFilters"
          >
            Clear Filters
          </button>
        </div>
  
        <!-- Results Summary & Sort -->
        <div class="results-row">
          <div class="results-info">
            <span class="results-count">
              {{ filteredTransfers.length }} of {{ allTransfers.length }} transfers
            </span>
            <span v-if="hasActiveFilters" class="filter-indicator">
              (filtered)
            </span>
          </div>
  
          <div class="sort-controls">
            <label class="sort-label">Sort by:</label>
            <select v-model="sortBy" class="sort-select">
              <option value="transfer_date">Transfer Date</option>
              <option value="property_name">Property Name</option>
              <option value="from_department_name">From Department</option>
              <option value="to_department_name">To Department</option>
              <option value="transferred_by_name">Transferred By</option>
            </select>
            <button 
              @click="toggleSortOrder" 
              class="sort-order-btn"
              :title="sortOrder === 'desc' ? 'Sort Ascending' : 'Sort Descending'"
            >
              {{ sortOrder === 'desc' ? '↓' : '↑' }}
            </button>
          </div>
        </div>
      </div>
  
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <span>Loading transfers...</span>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        <div class="error-icon">⚠️</div>
        <h3>Failed to load transfers</h3>
        <p>{{ error }}</p>
        <button @click="fetchTransfers" class="btn btn-primary">
          Try Again
        </button>
      </div>
  
      <!-- Empty State -->
      <div v-else-if="allTransfers.length === 0" class="empty-container">
        <div class="empty-icon">📦</div>
        <h3>No transfers found</h3>
        <p>No property transfers have been recorded yet.</p>
        <router-link to="/transfers/add" class="btn btn-primary">
          Create First Transfer
        </router-link>
      </div>
  
      <!-- No Results State -->
      <div v-else-if="filteredTransfers.length === 0" class="empty-container">
        <div class="empty-icon">🔍</div>
        <h3>No matching transfers</h3>
        <p>Try adjusting your filters or search terms.</p>
        <button @click="clearAllFilters" class="btn btn-outline">
          Clear All Filters
        </button>
      </div>
  
      <!-- Transfers Table -->
      <div v-else class="table-container">
        <div class="table-wrapper">
          <table class="transfers-table">
            <thead>
              <tr>
                <th class="col-property">Property</th>
                <th class="col-transfer">Transfer Direction</th>
                <th class="col-date">Date</th>
                <th class="col-user">Transferred By</th>
                <th class="col-notes">Notes</th>
                <th class="col-actions">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="transfer in paginatedTransfers" 
                :key="transfer.id"
                class="transfer-row"
              >
                <!-- Property Info -->
                <td class="col-property">
                  <div class="property-info">
                    <div class="property-name">{{ transfer.property_name || 'Unknown Property' }}</div>
                    <div class="property-code">{{ transfer.property_code || 'N/A' }}</div>
                  </div>
                </td>
  
                <!-- Transfer Direction -->
                <td class="col-transfer">
                  <div class="transfer-direction">
                    <div class="dept-from">
                      <span class="dept-label">From:</span>
                      <span class="dept-name">{{ transfer.from_department_name || 'Unknown' }}</span>
                    </div>
                    <div class="arrow">→</div>
                    <div class="dept-to">
                      <span class="dept-label">To:</span>
                      <span class="dept-name">{{ transfer.to_department_name || 'Unknown' }}</span>
                    </div>
                  </div>
                </td>
  
                <!-- Transfer Date -->
                <td class="col-date">
                  <div class="date-info">
                    <div class="date-main">{{ formatDate(transfer.transfer_date) }}</div>
                    <div class="date-time">{{ formatTime(transfer.transfer_date) }}</div>
                  </div>
                </td>
  
                <!-- Transferred By -->
                <td class="col-user">
                  <div class="user-info">
                    <span class="user-icon">👤</span>
                    <span class="user-name">{{ transfer.transferred_by_name || 'Unknown' }}</span>
                  </div>
                </td>
  
                <!-- Notes -->
                <td class="col-notes">
                  <div class="notes-content">
                    <span v-if="transfer.notes" class="notes-text" :title="transfer.notes">
                      {{ truncateText(transfer.notes, 50) }}
                    </span>
                    <span v-else class="no-notes">—</span>
                  </div>
                </td>
  
                <!-- Actions -->
                <td class="col-actions">
                  <div class="action-buttons">
                    <button 
                      @click="viewTransferDetails(transfer)" 
                      class="action-btn view-btn"
                      title="View Details"
                    >
                      👁️
                    </button>
                    <button 
                      @click="editTransfer(transfer)" 
                      class="action-btn edit-btn"
                      title="Edit Transfer"
                    >
                      ✏️
                    </button>
                    <button 
                      @click="deleteTransfer(transfer)" 
                      class="action-btn delete-btn"
                      title="Delete Transfer"
                    >
                      🗑️
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-container">
          <div class="pagination-info">
            Showing {{ startIndex + 1 }}-{{ endIndex }} of {{ filteredTransfers.length }} transfers
          </div>
          
          <div class="pagination-controls">
            <!-- Items per page -->
            <div class="per-page-control">
              <label class="per-page-label">Show:</label>
              <select v-model="itemsPerPage" class="per-page-select">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
              <span class="per-page-suffix">per page</span>
            </div>
  
            <!-- Page Navigation -->
            <div class="page-navigation">
              <button 
                @click="goToPage(1)" 
                :disabled="currentPage === 1"
                class="page-btn"
                title="First Page"
              >
                ⏮️
              </button>
              <button 
                @click="goToPage(currentPage - 1)" 
                :disabled="currentPage === 1"
                class="page-btn"
                title="Previous Page"
              >
                ◀️
              </button>
              
              <div class="page-numbers">
                <button 
                  v-for="page in visiblePages" 
                  :key="page"
                  @click="goToPage(page)"
                  :class="['page-number', { active: page === currentPage }]"
                >
                  {{ page }}
                </button>
              </div>
              
              <button 
                @click="goToPage(currentPage + 1)" 
                :disabled="currentPage === totalPages"
                class="page-btn"
                title="Next Page"
              >
                ▶️
              </button>
              <button 
                @click="goToPage(totalPages)" 
                :disabled="currentPage === totalPages"
                class="page-btn"
                title="Last Page"
              >
                ⏭️
              </button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Transfer Details Modal -->
      <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Transfer Details</h3>
            <button @click="closeDetailsModal" class="modal-close">✕</button>
          </div>
          <div class="modal-body">
            <div v-if="selectedTransfer" class="transfer-details">
              <div class="detail-row">
                <span class="detail-label">Property:</span>
                <span class="detail-value">{{ selectedTransfer.property_name }} ({{ selectedTransfer.property_code }})</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">From Department:</span>
                <span class="detail-value">{{ selectedTransfer.from_department_name }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">To Department:</span>
                <span class="detail-value">{{ selectedTransfer.to_department_name }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Transfer Date:</span>
                <span class="detail-value">{{ formatFullDate(selectedTransfer.transfer_date) }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Transferred By:</span>
                <span class="detail-value">{{ selectedTransfer.transferred_by_name }}</span>
              </div>
              <div v-if="selectedTransfer.notes" class="detail-row">
                <span class="detail-label">Notes:</span>
                <span class="detail-value">{{ selectedTransfer.notes }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  
  // Stores
  const authStore = useAuthStore()
  
  // Data
  const allTransfers = ref([])
  const departments = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // Search & Filters
  const searchQuery = ref('')
  const filters = ref({
    fromDepartment: '',
    toDepartment: '',
    dateFrom: '',
    dateTo: ''
  })
  
  // Sorting
  const sortBy = ref('transfer_date')
  const sortOrder = ref('desc')
  
  // Pagination
  const currentPage = ref(1)
  const itemsPerPage = ref(25)
  
  // Modal
  const showDetailsModal = ref(false)
  const selectedTransfer = ref(null)
  
  // Computed Properties
  const hasActiveFilters = computed(() => {
    return searchQuery.value || 
           filters.value.fromDepartment || 
           filters.value.toDepartment || 
           filters.value.dateFrom || 
           filters.value.dateTo
  })
  
  const filteredTransfers = computed(() => {
    let result = [...allTransfers.value]
  
    // Search filter
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(transfer => 
        (transfer.property_name && transfer.property_name.toLowerCase().includes(query)) ||
        (transfer.property_code && transfer.property_code.toLowerCase().includes(query)) ||
        (transfer.notes && transfer.notes.toLowerCase().includes(query)) ||
        (transfer.from_department_name && transfer.from_department_name.toLowerCase().includes(query)) ||
        (transfer.to_department_name && transfer.to_department_name.toLowerCase().includes(query))
      )
    }
  
    // Department filters
    if (filters.value.fromDepartment) {
      result = result.filter(transfer => transfer.from_department === parseInt(filters.value.fromDepartment))
    }
    
    if (filters.value.toDepartment) {
      result = result.filter(transfer => transfer.to_department === parseInt(filters.value.toDepartment))
    }
  
    // Date range filter
    if (filters.value.dateFrom) {
      result = result.filter(transfer => {
        const transferDate = new Date(transfer.transfer_date).toISOString().split('T')[0]
        return transferDate >= filters.value.dateFrom
      })
    }
    
    if (filters.value.dateTo) {
      result = result.filter(transfer => {
        const transferDate = new Date(transfer.transfer_date).toISOString().split('T')[0]
        return transferDate <= filters.value.dateTo
      })
    }
  
    // Sorting
    result.sort((a, b) => {
      let aValue = a[sortBy.value] || ''
      let bValue = b[sortBy.value] || ''
      
      // Special handling for dates
      if (sortBy.value === 'transfer_date') {
        aValue = new Date(aValue)
        bValue = new Date(bValue)
      } else {
        aValue = aValue.toString().toLowerCase()
        bValue = bValue.toString().toLowerCase()
      }
      
      if (sortOrder.value === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0
      }
    })
  
    return result
  })
  
  const totalPages = computed(() => {
    return Math.ceil(filteredTransfers.value.length / itemsPerPage.value)
  })
  
  const startIndex = computed(() => {
    return (currentPage.value - 1) * itemsPerPage.value
  })
  
  const endIndex = computed(() => {
    return Math.min(startIndex.value + itemsPerPage.value, filteredTransfers.value.length)
  })
  
  const paginatedTransfers = computed(() => {
    return filteredTransfers.value.slice(startIndex.value, endIndex.value)
  })
  
  const visiblePages = computed(() => {
    const total = totalPages.value
    const current = currentPage.value
    const delta = 2 // Number of pages to show on each side of current page
    
    let pages = []
    
    if (total <= 7) {
      // Show all pages if total is small
      for (let i = 1; i <= total; i++) {
        pages.push(i)
      }
    } else {
      // Show smart pagination
      const start = Math.max(1, current - delta)
      const end = Math.min(total, current + delta)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
    }
    
    return pages
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
      allTransfers.value = data.results || data
      
    } catch (err) {
      console.error('❌ Error fetching transfers:', err)
      error.value = 'Failed to load transfers. Please try again.'
    } finally {
      loading.value = false
    }
  }
  
  const fetchDepartments = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/departments/', {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
          'Content-Type': 'application/json'
        }
      })
  
      if (response.ok) {
        const data = await response.json()
        departments.value = data.results || data
      }
    } catch (err) {
      console.error('❌ Error fetching departments:', err)
    }
  }
  
  const clearSearch = () => {
    searchQuery.value = ''
  }
  
  const clearAllFilters = () => {
    searchQuery.value = ''
    filters.value = {
      fromDepartment: '',
      toDepartment: '',
      dateFrom: '',
      dateTo: ''
    }
    currentPage.value = 1
  }
  
  const toggleSortOrder = () => {
    sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  }
  
  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }
  
  const viewTransferDetails = (transfer) => {
    selectedTransfer.value = transfer
    showDetailsModal.value = true
  }
  
  const closeDetailsModal = () => {
    showDetailsModal.value = false
    selectedTransfer.value = null
  }
  
  const editTransfer = (transfer) => {
    // Implement edit functionality
    console.log('Edit transfer:', transfer)
    // You can navigate to edit page or open edit modal
  }
  
  const deleteTransfer = async (transfer) => {
    if (!confirm(`Are you sure you want to delete this transfer?\n\nProperty: ${transfer.property_name}\nFrom: ${transfer.from_department_name}\nTo: ${transfer.to_department_name}`)) {
      return
    }
    
    try {
      const response = await fetch(`http://localhost:8000/api/transfers/${transfer.id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
        }
      })
  
      if (response.ok) {
        // Remove from local array
        const index = allTransfers.value.findIndex(t => t.id === transfer.id)
        if (index > -1) {
          allTransfers.value.splice(index, 1)
        }
        alert('Transfer deleted successfully!')
      } else {
        throw new Error('Failed to delete transfer')
      }
    } catch (err) {
      console.error('❌ Error deleting transfer:', err)
      alert('Error deleting transfer: ' + err.message)
    }
  }
  
  // Utility functions
  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date'
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    } catch {
      return 'Invalid date'
    }
  }
  
  const formatTime = (dateString) => {
    if (!dateString) return ''
    try {
      return new Date(dateString).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return ''
    }
  }
  
  const formatFullDate = (dateString) => {
    if (!dateString) return 'Unknown date'
    try {
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return 'Invalid date'
    }
  }
  
  const truncateText = (text, maxLength) => {
    if (!text) return ''
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
  }
  
  // Debounced search
  let searchTimeout = null
  const debouncedSearch = () => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      currentPage.value = 1 // Reset to first page when searching
    }, 300)
  }
  
  // Watchers
  watch([filters, sortBy, sortOrder], () => {
    currentPage.value = 1 // Reset to first page when filters change
  }, { deep: true })
  
  watch(itemsPerPage, () => {
    currentPage.value = 1 // Reset to first page when changing items per page
  })
  
  // Lifecycle
  onMounted(async () => {
    await Promise.all([fetchTransfers(), fetchDepartments()])
  })
  </script>
  
  <style scoped>
  .all-transfers {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
    background: #f8fafc;
    min-height: 100vh;
  }
  
  /* Header */
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e2e8f0;
  }
  
  .header-content h1 {
    margin: 0 0 0.5rem 0;
    color: #1e293b;
    font-size: 2rem;
    font-weight: 700;
  }
  
  .page-subtitle {
    margin: 0;
    color: #64748b;
    font-size: 1rem;
  }
  
  .header-actions {
    display: flex;
    gap: 1rem;
  }
  
  /* Buttons */
  .btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .btn-primary {
    background: #667eea;
    color: white;
  }
  
  .btn-primary:hover {
    background: #5a67d8;
    transform: translateY(-1px);
  }
  
  .btn-outline {
    background: white;
    color: #374151;
    border: 1px solid #d1d5db;
  }
  
  .btn-outline:hover:not(:disabled) {
    background: #f9fafb;
    border-color: #9ca3af;
  }
  
  .btn-outline:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  /* Controls Section */
  .controls-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .filters-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: flex-end;
    margin-bottom: 1rem;
  }
  
  .search-group {
    flex: 2;
    min-width: 300px;
  }
  
  .search-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }
  
  .search-icon {
    position: absolute;
    left: 12px;
    color: #9ca3af;
    font-size: 16px;
  }
  
  .search-input {
    width: 100%;
    padding: 12px 12px 12px 40px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.2s ease;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  .clear-search-btn {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    font-size: 16px;
    padding: 4px;
  }
  
  .clear-search-btn:hover {
    color: #374151;
  }
  
  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .filter-label {
    font-size: 12px;
    font-weight: 600;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .filter-select,
  .date-input {
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    background: white;
    min-width: 150px;
  }
  
  .filter-select:focus,
  .date-input:focus {
    outline: none;
    border-color: #667eea;
  }
  
  .date-range {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .date-separator {
    color: #9ca3af;
    font-size: 12px;
  }
  
  .results-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }
  
  .results-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
    font-size: 14px;
  }
  
  .filter-indicator {
    background: #fef3c7;
    color: #92400e;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
  }
  
  .sort-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .sort-label {
    font-size: 14px;
    color: #374151;
  }
  
  .sort-select {
    padding: 6px 10px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
  }
  
  .sort-order-btn {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 6px 10px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.2s ease;
  }
  
  .sort-order-btn:hover {
    background: #e5e7eb;
  }
  
  /* Loading, Error, Empty States */
  .loading-container,
  .error-container,
  .empty-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e5e7eb;
    border-top: 3px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .error-icon,
  .empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }
  
  .error-container h3,
  .empty-container h3 {
    margin: 0 0 0.5rem 0;
    color: #374151;
    font-size: 1.5rem;
  }
  
  .error-container p,
  .empty-container p {
    margin: 0 0 1.5rem 0;
    color: #6b7280;
  }
  
  /* Table */
  .table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .table-wrapper {
    overflow-x: auto;
  }
  
  .transfers-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .transfers-table th {
    background: #f8fafc;
    padding: 1rem 0.75rem;
    text-align: left;
    font-weight: 600;
    color: #374151;
    font-size: 14px;
    border-bottom: 1px solid #e5e7eb;
    white-space: nowrap;
  }
  
  .transfers-table td {
    padding: 1rem 0.75rem;
    border-bottom: 1px solid #f3f4f6;
    vertical-align: top;
  }
  
  .transfer-row {
    transition: background-color 0.2s ease;
  }
  
  .transfer-row:hover {
    background: #fafbfc;
  }
  
  /* Table Columns */
  .col-property {
    min-width: 200px;
  }
  
  .col-transfer {
    min-width: 300px;
  }
  
  .col-date {
    min-width: 140px;
  }
  
  .col-user {
    min-width: 150px;
  }
  
  .col-notes {
    min-width: 200px;
    max-width: 250px;
  }
  
  .col-actions {
    min-width: 120px;
  }
  
  /* Property Info */
  .property-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .property-name {
    font-weight: 600;
    color: #1e293b;
    font-size: 14px;
  }
  
  .property-code {
    background: #f1f5f9;
    color: #64748b;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 12px;
    font-family: monospace;
    width: fit-content;
  }
  
  /* Transfer Direction */
  .transfer-direction {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .dept-from,
  .dept-to {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    min-width: 0;
  }
  
  .dept-label {
    font-size: 10px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .dept-name {
    font-size: 13px;
    font-weight: 500;
    word-wrap: break-word;
  }
  
  .dept-from .dept-name {
    color: #dc2626;
  }
  
  .dept-to .dept-name {
    color: #059669;
  }
  
  .arrow {
    color: #667eea;
    font-weight: bold;
    font-size: 16px;
    flex-shrink: 0;
  }
  
  /* Date Info */
  .date-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .date-main {
    font-weight: 500;
    color: #374151;
    font-size: 14px;
  }
  
  .date-time {
    color: #9ca3af;
    font-size: 12px;
  }
  
  /* User Info */
  .user-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .user-icon {
    font-size: 14px;
    color: #9ca3af;
  }
  
  .user-name {
    font-size: 14px;
    color: #374151;
  }
  
  /* Notes */
  .notes-content {
    font-size: 14px;
    line-height: 1.4;
  }
  
  .notes-text {
    color: #374151;
  }
  
  .no-notes {
    color: #9ca3af;
    font-style: italic;
  }
  
  /* Action Buttons */
  .action-buttons {
    display: flex;
    gap: 0.5rem;
  }
  
  .action-btn {
    background: none;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.5rem;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .view-btn:hover {
    background: #dbeafe;
    border-color: #3b82f6;
  }
  
  .edit-btn:hover {
    background: #fef3c7;
    border-color: #f59e0b;
  }
  
  .delete-btn:hover {
    background: #fee2e2;
    border-color: #ef4444;
  }
  
  /* Pagination */
  .pagination-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-top: 1px solid #e5e7eb;
    background: #fafbfc;
  }
  
  .pagination-info {
    color: #6b7280;
    font-size: 14px;
  }
  
  .pagination-controls {
    display: flex;
    align-items: center;
    gap: 2rem;
  }
  
  .per-page-control {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 14px;
    color: #374151;
  }
  
  .per-page-select {
    padding: 4px 8px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .page-navigation {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  
  .page-btn {
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 0.5rem;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .page-btn:hover:not(:disabled) {
    background: #f9fafb;
    border-color: #9ca3af;
  }
  
  .page-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .page-numbers {
    display: flex;
    gap: 0.25rem;
    margin: 0 0.5rem;
  }
  
  .page-number {
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
    min-width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .page-number:hover {
    background: #f9fafb;
    border-color: #9ca3af;
  }
  
  .page-number.active {
    background: #667eea;
    border-color: #667eea;
    color: white;
  }
  
  /* Modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow: hidden;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .modal-header h3 {
    margin: 0;
    font-size: 1.25rem;
    color: #1e293b;
  }
  
  .modal-close {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #9ca3af;
    padding: 0.5rem;
  }
  
  .modal-close:hover {
    color: #374151;
  }
  
  .modal-body {
    padding: 1.5rem;
    overflow-y: auto;
  }
  
  .transfer-details {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .detail-row {
    display: flex;
    gap: 1rem;
  }
  
  .detail-label {
    font-weight: 600;
    color: #374151;
    min-width: 140px;
    flex-shrink: 0;
  }
  
  .detail-value {
    color: #6b7280;
    word-wrap: break-word;
  }
  
  /* Responsive Design */
  @media (max-width: 1200px) {
    .filters-row {
      flex-direction: column;
      align-items: stretch;
    }
    
    .search-group {
      flex: none;
    }
    
    .filter-group {
      flex: 1;
    }
  }
  
  @media (max-width: 768px) {
    .all-transfers {
      padding: 1rem;
    }
    
    .page-header {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }
    
    .results-row {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }
    
    .transfer-direction {
      flex-direction: column;
      gap: 0.5rem;
      align-items: stretch;
    }
    
    .arrow {
      transform: rotate(90deg);
      align-self: center;
    }
    
    .pagination-container {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }
    
    .pagination-controls {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }
    
    .page-navigation {
      justify-content: center;
    }
    
    .action-buttons {
      justify-content: center;
    }
  }
  
  @media (max-width: 480px) {
    .transfers-table th,
    .transfers-table td {
      padding: 0.5rem;
    }
    
    .page-numbers {
      display: none;
    }
  }
  </style>
  