<template>
  <div class="template-section card">
    <h2 class="section-title">Template</h2>
    <div class="template-header">
      <input
        v-model="title"
        placeholder="Enter template title..."
        class="input title-input"
      />
      <div class="changes-summary" v-if="detectedChanges.length">
        <h4 class="group-title">Detected Changes:</h4>
        <ul>
          <li v-for="(change, index) in detectedChanges" :key="index">{{ change }}</li>
        </ul>
      </div>
    </div>
    <textarea 
      :value="modelValue"
      @input="updateTemplate"
      placeholder="Enter your template here..."
      class="input template-input"
    ></textarea>
    <div class="template-actions">
      <button @click="saveTemplate" class="button">Save Template</button>
      <button @click="saveVersion" v-if="currentTemplateId" class="button">Save New Version</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TemplateEditor',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    variables: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      title: '',
      currentTemplateId: null,
      previousVersion: null,
      detectedChanges: []
    }
  },
  methods: {
    updateTemplate(event) {
      this.$emit('update:modelValue', event.target.value)
      this.processTemplate()
      this.detectChanges()
    },
    async processTemplate() {
      try {
        const response = await axios.post('/api/templates/process', {
          template: this.modelValue,
          variables: this.variables
        })
        this.$emit('update:result', response.data.result.replace(/\n/g, '<br>'))
        this.$emit('update:errors', response.data.errors || [])
      } catch (error) {
        console.error('Error processing template:', error)
        this.$emit('update:errors', ['Error processing template'])
      }
    },
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
    async saveTemplate() {
      if (!this.title.trim()) {
        this.$emit('update:errors', ['Please enter a title for the template'])
        return
      }
      try {
        const response = await axios.post('/api/templates', {
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
          
        await axios.post(`/api/templates/${this.currentTemplateId}/versions`, {
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
  watch: {
    modelValue: {
      immediate: true,
      handler(newValue) {
        if (!this.previousVersion) {
          this.previousVersion = newValue
        }
      }
    },
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
.template-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 100%;
}

.template-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.title-input {
  font-size: 1.125rem;
  font-weight: 500;
}

.template-input {
  flex: 1;
  min-height: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
  line-height: 1.5;
  resize: none;
}

.changes-summary {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
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

.template-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.button {
  flex: 1;
}
</style> 