<!-- Main application component that serves as the root of the application -->
<template>
  <div class="app">
    <!-- Application header with the main title -->
    <header class="app-header">
      <h1>Email Template Editor</h1>
    </header>

    <!-- Main editor container with two columns on larger screens -->
    <div class="editor-container">
      <!-- Left column: Template editor component -->
      <template-editor
        ref="templateEditor"
        v-model="templateContent"
        :variables="variables"
        @update:result="processedResult = $event"
        @update:errors="errors = $event"
        @template-id-change="handleTemplateIdChange"
        @version-saved="handleVersionSaved"
      />

      <!-- Right column: Variable editor, preview, and history sections -->
      <div class="right-column">
        <!-- Variable editor for managing template variables -->
        <variable-editor
          v-model:variables="variables"
          @update:variables="handlerVariablesUpdate"
        />

        <!-- Preview section showing the processed template -->
        <preview-section
          :content="processedResult"
          :errors="errors"
        />

        <!-- History section showing template versions -->
        <history-section
          ref="historySection"
          @load-version="loadVersion"
        />
      </div>
    </div>
  </div>
</template>

<script>
// Import all necessary components
import TemplateEditor from './components/TemplateEditor.vue'
import VariableEditor from './components/VariableEditor.vue'
import PreviewSection from './components/PreviewSection.vue'
import HistorySection from './components/HistorySection.vue'

export default {
  name: 'App',
  // Register all child components
  components: {
    TemplateEditor,
    VariableEditor,
    PreviewSection,
    HistorySection
  },
  // Initialize component data
  data() {
    return {
      // Current template content
      templateContent: '',
      // Default variables structure for the template
      variables: {
        user: {
          firstName: '',
          address: {
            street: '',
            city: '',
            state: '',
            zip: ''
          }
        },
        company: {
          name: '',
          address: {
            city: ''
          }
        },
        meeting: {
          date: ''
        },
        sender: {
          name: ''
        }
      },
      // Processed template result with variables replaced
      processedResult: '',
      // Any errors that occur during template processing
      errors: []
    }
  },
  methods: {
    // Handle variable updates and reprocess the template
    handlerVariablesUpdate(newVariables) {
      this.variables = newVariables
      if (this.$refs.templateEditor) {
        this.$refs.templateEditor.processTemplate()
      }
    },
    // Load a specific version of the template
    loadVersion(template) {
      this.templateContent = template
      // Ensure template processing happens after the next tick
      this.$nextTick(() => {
        if (this.$refs.templateEditor) {
          this.$refs.templateEditor.processTemplate()
        }
      })
    },
    // Handle template ID changes and fetch versions
    handleTemplateIdChange(templateId) {
      if (this.$refs.historySection) {
        this.$refs.historySection.fetchVersions(templateId)
      }
    },
    // Handle version saves and refresh the history
    handleVersionSaved(templateId) {
      if (this.$refs.historySection) {
        this.$refs.historySection.fetchVersions(templateId)
      }
    }
  },
  // Add watcher for template content changes
  watch: {
    templateContent: {
      immediate: true,
      handler() {
        this.$nextTick(() => {
          if (this.$refs.templateEditor) {
            this.$refs.templateEditor.processTemplate()
          }
        })
      }
    }
  }
}
</script>

<style>
/* CSS variables for consistent theming throughout the application */
:root {
  --primary-color: #1a2238;
  --secondary-color: #2d3748;
  --accent-color: #4299e1;
  --text-color: #e9ecef;
  --text-secondary: #a0aec0;
  --border-color: #4a5568;
  --success-color: #48bb78;
  --error-color: #f56565;
  --background-color: #1a2238;
  --card-background: #2d3748;
  --input-background: #2d3748;
  --hover-color: #3182ce;
}

/* Reset default styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Base styles for the entire application */
body {
  margin: 0;
  padding: 0;
  background-color: var(--background-color);
  color: var(--text-color);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.6;
  min-height: 100vh;
}

/* Main application container */
.app {
  max-width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

/* Header styles with gradient text effect */
.app-header {
  margin-bottom: 3rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.app-header h1 {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--text-color);
  letter-spacing: -0.025em;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background: linear-gradient(45deg, var(--accent-color), #9f7aea, var(--accent-color));
  background-size: 200% 200%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientFlow 8s ease infinite;
  position: relative;
  display: inline-block;
}

/* Header underline animation */
.app-header h1::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
  animation: shimmer 2s ease-in-out infinite;
}

/* Gradient animation for the header */
@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Shimmer animation for the header underline */
@keyframes shimmer {
  0% {
    opacity: 0.3;
    transform: translateX(-100%);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.3;
    transform: translateX(100%);
  }
}

/* Main editor container layout */
.editor-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
  min-height: calc(100vh - 200px);
}

/* Responsive layout for larger screens */
@media (min-width: 1024px) {
  .editor-container {
    grid-template-columns: 1fr 1fr;
  }
}

/* Right column layout */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  height: 100%;
}

/* Common card styles for all components */
.card {
  background-color: var(--card-background);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Common input styles */
.input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--input-background);
  color: var(--text-color);
  font-size: 1rem;
  transition: all 0.2s;
}

.input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

/* Common button styles */
.button {
  padding: 0.75rem 1.5rem;
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button:hover {
  background-color: var(--hover-color);
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0);
}

/* Section title styles */
.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--text-color);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background: linear-gradient(45deg, var(--accent-color), #9f7aea);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -0.25rem;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
}

/* Error message styles */
.error-message {
  color: var(--error-color);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Success message styles */
.success-message {
  color: var(--success-color);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
</style>