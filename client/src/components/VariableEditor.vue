<template>
    <div class="variable-editor card">
        <h2 class="section-title">Variables</h2>
        <div class="variable-groups">
            <div class="variable-group">
                <h3 class="group-title">User Information</h3>
                <div class="input-group">
                    <label>First Name</label>
                    <input 
                        v-model="variables.user.firstName" 
                        class="input" 
                        :class="{ 'input-error': errors.user.firstName }"
                        @input="validateName('user.firstName', $event)"
                    />
                    <div v-if="errors.user.firstName" class="error-message">{{ errors.user.firstName }}</div>
                </div>
                <div class="input-group">
                    <label>Street</label>
                    <input 
                        v-model="variables.user.address.street" 
                        class="input"
                        :class="{ 'input-error': errors.user.address.street }"
                        @input="validateAddress('user.address.street', $event)"
                    />
                    <div v-if="errors.user.address.street" class="error-message">{{ errors.user.address.street }}</div>
                </div>
                <div class="input-group">
                    <label>City</label>
                    <input 
                        v-model="variables.user.address.city" 
                        class="input"
                        :class="{ 'input-error': errors.user.address.city }"
                        @input="validateCity('user.address.city', $event)"
                    />
                    <div v-if="errors.user.address.city" class="error-message">{{ errors.user.address.city }}</div>
                </div>
                <div class="input-group">
                    <label>State</label>
                    <input 
                        v-model="variables.user.address.state" 
                        class="input"
                        :class="{ 'input-error': errors.user.address.state }"
                        @input="validateState('user.address.state', $event)"
                        maxlength="2"
                    />
                    <div v-if="errors.user.address.state" class="error-message">{{ errors.user.address.state }}</div>
                </div>
                <div class="input-group">
                    <label>ZIP</label>
                    <input 
                        v-model="variables.user.address.zip" 
                        class="input"
                        :class="{ 'input-error': errors.user.address.zip }"
                        @input="validateZip('user.address.zip', $event)"
                        maxlength="5"
                    />
                    <div v-if="errors.user.address.zip" class="error-message">{{ errors.user.address.zip }}</div>
                </div>
            </div>

            <div class="variable-group">
                <h3 class="group-title">Company Information</h3>
                <div class="input-group">
                    <label>Company Name</label>
                    <input 
                        v-model="variables.company.name" 
                        class="input"
                        :class="{ 'input-error': errors.company.name }"
                        @input="validateCompanyName('company.name', $event)"
                    />
                    <div v-if="errors.company.name" class="error-message">{{ errors.company.name }}</div>
                </div>
                <div class="input-group">
                    <label>City</label>
                    <input 
                        v-model="variables.company.address.city" 
                        class="input"
                        :class="{ 'input-error': errors.company.address.city }"
                        @input="validateCity('company.address.city', $event)"
                    />
                    <div v-if="errors.company.address.city" class="error-message">{{ errors.company.address.city }}</div>
                </div>
            </div>

            <div class="variable-group">
                <h3 class="group-title">Meeting Information</h3>
                <div class="input-group">
                    <label>Date</label>
                    <input 
                        v-model="variables.meeting.date" 
                        class="input"
                        :class="{ 'input-error': errors.meeting.date }"
                        @input="validateDate('meeting.date', $event)"
                        type="datetime-local"
                    />
                    <div v-if="errors.meeting.date" class="error-message">{{ errors.meeting.date }}</div>
                </div>
            </div>

            <div class="variable-group">
                <h3 class="group-title">Sender Information</h3>
                <div class="input-group">
                    <label>Name</label>
                    <input 
                        v-model="variables.sender.name" 
                        class="input"
                        :class="{ 'input-error': errors.sender.name }"
                        @input="validateName('sender.name', $event)"
                    />
                    <div v-if="errors.sender.name" class="error-message">{{ errors.sender.name }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VariableEditor',
    props: {
        variables: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            errors: {
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
            }
        }
    },
    methods: {
        validateName(path, event) {
            const value = event.target.value
            const regex = /^[a-zA-Z\s-']+$/
            if (!regex.test(value)) {
                this.setError(path, 'Only letters, spaces, hyphens, and apostrophes are allowed')
            } else {
                this.clearError(path)
            }
            this.updateVariables()
        },
        validateAddress(path, event) {
            const value = event.target.value
            const regex = /^[a-zA-Z0-9\s.,#-]+$/
            if (!regex.test(value)) {
                this.setError(path, 'Only letters, numbers, spaces, and common punctuation are allowed')
            } else {
                this.clearError(path)
            }
            this.updateVariables()
        },
        validateCity(path, event) {
            const value = event.target.value
            const regex = /^[a-zA-Z\s-']+$/
            if (!regex.test(value)) {
                this.setError(path, 'Only letters, spaces, hyphens, and apostrophes are allowed')
            } else {
                this.clearError(path)
            }
            this.updateVariables()
        },
        validateState(path, event) {
            const value = event.target.value.toUpperCase()
            const stateCodes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
            if (!stateCodes.includes(value)) {
                this.setError(path, 'Please enter a valid 2-letter state code')
            } else {
                this.clearError(path)
            }
            this.updateVariables()
        },
        validateZip(path, event) {
            const value = event.target.value
            const regex = /^\d{5}$/
            if (!regex.test(value)) {
                this.setError(path, 'Please enter a valid 5-digit ZIP code')
            } else {
                this.clearError(path)
            }
            this.updateVariables()
        },
        validateCompanyName(path, event) {
            const value = event.target.value
            const regex = /^[a-zA-Z0-9\s.,&'-]+$/
            if (!regex.test(value)) {
                this.setError(path, 'Only letters, numbers, spaces, and common business characters are allowed')
            } else {
                this.clearError(path)
            }
            this.updateVariables()
        },
        validateDate(path, event) {
            const value = event.target.value
            if (!value) {
                this.clearError(path)
                return
            }
            const date = new Date(value)
            if (isNaN(date.getTime())) {
                this.setError(path, 'Please enter a valid date and time')
            } else {
                this.clearError(path)
            }
            this.updateVariables()
        },
        setError(path, message) {
            const pathParts = path.split('.')
            let current = this.errors
            for (let i = 0; i < pathParts.length - 1; i++) {
                current = current[pathParts[i]]
            }
            current[pathParts[pathParts.length - 1]] = message
        },
        clearError(path) {
            const pathParts = path.split('.')
            let current = this.errors
            for (let i = 0; i < pathParts.length - 1; i++) {
                current = current[pathParts[i]]
            }
            current[pathParts[pathParts.length - 1]] = ''
        },
        updateVariables() {
            this.$emit('update:variables', this.variables)
        }
    }
}
</script>

<style scoped>
.variable-editor {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.variable-groups {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.variable-group {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.group-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-color);
}

.input-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.input-error {
    border-color: var(--error-color);
    box-shadow: 0 0 0 1px var(--error-color);
}

.error-message {
    color: var(--error-color);
    font-size: 0.75rem;
    margin-top: 0.25rem;
}

label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
}
</style>