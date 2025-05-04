<!-- Template editor component for creating and editing email templates -->
<template>
  <div class="template-section card">
    <!-- Section title with gradient effect -->
    <h2 class="section-title">Template</h2>
    
    <!-- Template header with title input and changes summary -->
    <div class="template-header">
      <!-- Title input field -->
      <input
        v-model="title"
        placeholder="Enter template title..."
        class="input title-input"
      />
      <!-- Changes summary section that shows when changes are detected -->
      <div class="changes-summary" v-if="detectedChanges.length">
        <h4 class="group-title">Detected Changes:</h4>
        <ul>
          <li v-for="(change, index) in detectedChanges" :key="index">{{ change }}</li>
        </ul>
      </div>
    </div>

    <!-- Main template textarea -->
    <textarea 
      :value="modelValue"
      @input="updateTemplate"
      placeholder="Enter your template here..."
      class="input template-input"
    ></textarea>

    <!-- Action buttons for saving template and versions -->
    <div class="template-actions">
      <button @click="saveTemplate" class="button">Save Template</button>
      <button @click="saveVersion" v-if="currentTemplateId" class="button">Save New Version</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from '../config'

export default {
  name: 'TemplateEditor',
  // Component props
  props: {
    // The current template content
    modelValue: {
      type: String,
      default: ''
    },
    // Variables to be used in the template
    variables: {
      type: Object,
      required: true
    }
  },
  // Component data
  data() {
    return {
      // Template title
      title: '',
      // Current template ID (null if not saved)
      currentTemplateId: null,
      // Previous version for change detection
      previousVersion: null,
      // List of detected changes
      detectedChanges: [],
      // Default template with slash-based variables
      defaultTemplate: `Dear /user.firstName,

Thanks for your interest in /company.name. Our representative at /company.address.city 
will contact you on /meeting.date.

Your package will be delivered to:
/user.address.street,
/user.address.city, 
/user.address.state,
/user.address.zip

Best regards,
/sender.name`
    }
  },
  created() {
    // Initialize the template with default content if none is provided
    if (!this.modelValue) {
      this.$emit('update:modelValue', this.defaultTemplate);
    }
  },
  mounted() {
    // Process template when component is mounted
    this.processTemplate();
  },
  methods: {
    // Update template content and trigger processing
    updateTemplate(event) {
      this.$emit('update:modelValue', event.target.value)
      this.$nextTick(() => {
        this.processTemplate()
        this.detectChanges()
      })
    },

    // Process the template with variables
    async processTemplate() {
      try {
        // Convert slash-based variables to curly braces for processing
        // Match variables that start with / and end with a word character (no trailing dots)
        const templateWithBraces = this.modelValue.replace(/\/([a-zA-Z0-9.]+[a-zA-Z0-9])/g, (match, variable) => {
          // Ensure we're not matching partial variables
          if (match.endsWith('.')) return match;
          return `{${variable}}`;
        });
        
        const response = await axios.post(`${API_BASE_URL}/api/templates/process`, {
          template: templateWithBraces,
          variables: this.variables
        })
        
        // Convert the result back to slash-based variables for display
        const resultWithSlashes = response.data.result.replace(/\{([^}]+)\}/g, '/$1');
        this.$emit('update:result', resultWithSlashes.replace(/\n/g, '<br>'))
        this.$emit('update:errors', response.data.errors || [])
      } catch (error) {
        console.error('Error processing template:', error)
        this.$emit('update:errors', ['Error processing template'])
      }
    },

    // Detect changes between current and previous version
    async detectChanges() {
      if (!this.previousVersion) {
        this.previousVersion = this.modelValue
        return
      }
      
      const currentLines = this.modelValue.split('\n')
      const previousLines = this.previousVersion.split('\n')
      
      this.detectedChanges = []
      
      // Compare line by line
      for (let i = 0; i < Math.max(currentLines.length, previousLines.length); i++) {
        const currentLine = currentLines[i] || ''
        const previousLine = previousLines[i] || ''
        
        if (currentLine !== previousLine) {
          if (i < previousLines.length && i < currentLines.length) {
            this.detectedChanges.push(`Line ${i + 1} changed: "${previousLine}" → "${currentLine}"`)
          } else if (i >= previousLines.length) {
            this.detectedChanges.push(`Added line ${i + 1}: "${currentLine}"`)
          } else {
            this.detectedChanges.push(`Removed line ${i + 1}: "${previousLine}"`)
          }
        }
      }
    },

    // Save a new template
    async saveTemplate() {
      if (!this.title.trim()) {
        this.$emit('update:errors', ['Please enter a title for the template'])
        return
      }
      try {
        const response = await axios.post(`${API_BASE_URL}/api/templates`, {
          template: this.modelValue,
          title: this.title,
          description: 'Initial version'
        })
        this.currentTemplateId = response.data.id
        this.previousVersion = this.modelValue
        this.detectedChanges = []
        this.$emit('template-id-change', response.data.id)
      } catch (error) {
        console.error('Error saving template:', error)
        this.$emit('update:errors', ['Error saving template'])
      }
    },

    // Save a new version of an existing template
    async saveVersion() {
      if (!this.currentTemplateId) return
      if (!this.title.trim()) {
        this.$emit('update:errors', ['Please enter a title for the version'])
        return
      }
      try {
        const description = this.detectedChanges.length 
          ? `Changes:\n${this.detectedChanges.join('\n')}`
          : 'No changes detected'
          
        await axios.post(`${API_BASE_URL}/api/templates/${this.currentTemplateId}/versions`, {
          template: this.modelValue,
          title: this.title,
          description: description
        })
        this.previousVersion = this.modelValue
        this.detectedChanges = []
        this.$emit('version-saved', this.currentTemplateId)
      } catch (error) {
        console.error('Error saving version:', error)
        this.$emit('update:errors', ['Error saving version'])
      }
    }
  },
  // Component watchers
  watch: {
    // Watch for template content changes
    modelValue: {
      immediate: true,
      handler(newValue) {
        if (!this.previousVersion) {
          this.previousVersion = newValue
        }
      }
    },
    // Watch for variable changes
    variables: {
      deep: true,
      handler() {
        this.processTemplate()
      }
    }
  }
}
</script>

<style scoped>
/* Template section container */
.template-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 100%;
  min-height: 100%;
}

/* Template header styles */
.template-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Title input field styles */
.title-input {
  font-size: 1.125rem;
  font-weight: 500;
}

/* Template input textarea styles */
.template-input {
  flex: 1;
  min-height: 300px;
  height: 100%;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
  line-height: 1.5;
  resize: none;
  overflow-y: auto;
}

/* Changes summary section styles */
.changes-summary {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
  max-height: 200px;
  overflow-y: auto;
}

.changes-summary h4 {
  color: var(--text-color);
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 600;
}

.changes-summary ul {
  margin: 0;
  padding-left: 1.25rem;
}

.changes-summary li {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

/* Template action buttons container */
.template-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.button {
  flex: 1;
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .template-section {
    min-height: 100vh;
  }
  
  .template-input {
    min-height: 400px;
  }
}
</style> 