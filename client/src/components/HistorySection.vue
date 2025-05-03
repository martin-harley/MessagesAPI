<!-- History section component for displaying template versions -->
<template>
  <div class="history-section card">
    <!-- Section title with gradient effect -->
    <h2 class="section-title">History</h2>
    
    <!-- List of template versions -->
    <div class="history-list">
      <!-- Empty state message -->
      <div v-if="versions.length === 0" class="no-history">
        No template versions yet
      </div>
      
      <!-- Version list items -->
      <div v-else v-for="version in versions" :key="version.id" class="history-item">
        <!-- Version header with date and load button -->
        <div class="version-header">
          <span class="version-date">{{ formatDate(version.created_at) }}</span>
          <button @click="loadVersion(version)" class="button load-button">Load</button>
        </div>
        
        <!-- Version title and description -->
        <div class="version-title group-title">{{ version.title }}</div>
        <div class="version-description">{{ version.description }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from '../config'

export default {
  name: 'HistorySection',
  // Component data
  data() {
    return {
      // List of template versions
      versions: []
    }
  },
  methods: {
    // Format date to a readable string
    formatDate(date) {
      if (!date) return 'No date'
      try {
        const parsedDate = new Date(date)
        if (isNaN(parsedDate.getTime())) {
          return 'Invalid date'
        }
        return parsedDate.toLocaleString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        console.error('Error formatting date:', error)
        return 'Invalid date'
      }
    },
    
    // Load a specific version of the template
    loadVersion(version) {
      this.$emit('load-version', version.content)
    },
    
    // Fetch versions for a specific template
    async fetchVersions(templateId) {
      if (!templateId) return
      try {
        const response = await axios.get(`${API_BASE_URL}/api/templates/${templateId}/versions`)
        this.versions = response.data
      } catch (error) {
        console.error('Error fetching versions:', error)
      }
    }
  }
}
</script>

<style scoped>
/* History section container */
.history-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Version list container with scrollbar */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Custom scrollbar styles */
.history-list::-webkit-scrollbar {
  width: 6px;
}

.history-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Empty state message */
.no-history {
  color: var(--text-secondary);
  text-align: center;
  padding: 2rem;
}

/* Version item container */
.history-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Version header with date and load button */
.version-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Version date styles */
.version-date {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* Load button styles */
.load-button {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

/* Version title styles */
.version-title {
  font-weight: 500;
  color: var(--text-color);
}

/* Version description styles */
.version-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  white-space: pre-wrap;
}
</style> 