# Email Template Editor

A modern web application for creating, managing, and previewing email templates with version control.

## Features

- **Template Editor**: Create and edit email templates with a user-friendly interface
- **Version Control**: Track changes to templates with detailed version history
- **Variable Support**: Use dynamic variables in templates (e.g., `/user.firstName`)
- **Live Preview**: See how your template looks with sample data
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, intuitive interface with smooth animations

## Tech Stack

- **Frontend**:
  - Vue.js 3
  - Vite
  - Tailwind CSS
  - Inter font

- **Backend**:
  - Python
  - Flask
  - SQLite
  - SQLAlchemy

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MessagesAPI
   ```

2. Install frontend dependencies:
   ```bash
   cd client
   npm install
   ```

3. Install backend dependencies:
   ```bash
   cd ../server
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using run_dev.py (Recommended)

The easiest way to start both the frontend and backend servers is to use the `run_dev.py` script:

```bash
python run_dev.py
```

This will:
1. Start the Flask backend server on `http://localhost:5000`
2. Start the Vite development server on `http://localhost:3000`
3. Automatically open your default browser to `http://localhost:3000`

### Option 2: Manual Start

If you prefer to start the servers manually:

1. Start the backend server:
   ```bash
   cd server
   python main.py
   ```
   The server will start on `http://localhost:5000`

2. Start the frontend development server:
   ```bash
   cd client
   npm run dev
   ```
   The frontend will start on `http://localhost:5173`

3. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
MessagesAPI/
├── client/                 # Frontend Vue.js application
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── App.vue        # Main application component
│   │   └── main.js        # Application entry point
│   └── index.html         # HTML template
│
├── server/                # Backend Flask application
│   ├── main.py           # Main server file
│   ├── models.py         # Database models
│   └── templates.db      # SQLite database
│
└── run_dev.py            # Development server script
```

## Key Components

### Frontend

- **App.vue**: Main application layout and routing
- **TemplateEditor.vue**: Template editing interface
- **HistorySection.vue**: Version history and management
- **PreviewSection.vue**: Template preview with sample data
- **VariableEditor.vue**: Variable management interface

### Backend

- **main.py**: Flask server with API endpoints
- **models.py**: SQLAlchemy database models
- **templates.db**: SQLite database file
- **run_dev.py**: Development server script for easy startup

## API Endpoints

- `POST /api/templates`: Create a new template
- `POST /api/templates/<id>/versions`: Create a new version
- `GET /api/templates/<id>/versions`: Get all versions
- `POST /api/templates/process`: Process template with variables

## Usage

1. **Creating a Template**:
   - Enter a title and template content
   - Use variables in the format `{variable.path}` (e.g., `{user.firstName}`)
   - Click "Save Template" to create the initial version

2. **Editing a Template**:
   - Make changes to the template content
   - Add a description of the changes
   - Click "Save Version" to create a new version

3. **Viewing History**:
   - Browse through previous versions
   - See when each version was created
   - View descriptions of changes
   - Load any previous version

4. **Previewing Templates**:
   - Enter sample data for variables
   - See how the template looks with the data
   - Check for any missing variables

## Development

### Frontend Development

- The frontend uses Vue 3 with the Composition API
- Styling is done with Tailwind CSS
- Components are organized by feature
- State management is handled through Vue's reactivity system

### Backend Development

- The backend uses Flask for the API server
- SQLAlchemy for database operations
- SQLite for data storage
- CORS enabled for frontend communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
