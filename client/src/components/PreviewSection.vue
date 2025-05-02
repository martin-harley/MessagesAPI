<template>
  <div class="preview-section card">
    <h2 class="section-title">Preview</h2>
    <div class="preview-content" v-if="content">
      <div v-html="formatContent(content)"></div>
    </div>
    <div v-else class="no-content">
      Enter a template and variables to see the preview
    </div>
    <div v-if="errors.length" class="error-messages">
      <div v-for="(error, index) in errors" :key="index" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PreviewSection',
  props: {
    content: {
      type: String,
      default: ''
    },
    errors: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    formatContent(content) {
      // Replace ISO dates with formatted dates
      return content.replace(/(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})/g, (match) => {
        const date = new Date(match)
        if (isNaN(date.getTime())) return match
        return date.toLocaleString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: 'numeric',
          minute: '2-digit',
          hour12: true
        })
      })
    }
  }
}
</script>

<style scoped>
.preview-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preview-content {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1.5rem;
  min-height: 200px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.preview-content :deep(p) {
  margin-bottom: 1rem;
}

.preview-content :deep(p:last-child) {
  margin-bottom: 0;
}

.no-content {
  color: var(--text-secondary);
  text-align: center;
  padding: 2rem;
}

.error-messages {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style> 