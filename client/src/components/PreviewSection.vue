<!-- Preview section component for displaying the processed template -->
<template>
  <div class="preview-section card">
    <!-- Section title with gradient effect -->
    <h2 class="section-title">Preview</h2>
    
    <!-- Preview content with formatted dates -->
    <div class="preview-content" v-if="content">
      <div v-html="formatContent(content)"></div>
    </div>
    
    <!-- Empty state message -->
    <div v-else class="no-content">
      Enter a template and variables to see the preview
    </div>
    
    <!-- Error messages display -->
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
  // Component props
  props: {
    // The processed template content
    content: {
      type: String,
      default: ''
    },
    // Any errors that occurred during processing
    errors: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    // Format the content, specifically handling date formatting
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
/* Preview section container */
.preview-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Preview content container */
.preview-content {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1.5rem;
  min-height: 200px;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* Paragraph spacing in preview content */
.preview-content :deep(p) {
  margin-bottom: 1rem;
}

/* Remove margin from last paragraph */
.preview-content :deep(p:last-child) {
  margin-bottom: 0;
}

/* Empty state message */
.no-content {
  color: var(--text-secondary);
  text-align: center;
  padding: 2rem;
}

/* Error messages container */
.error-messages {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style> 