# MSS Frontend - React + Vite

Enterprise-grade React frontend for the MSS Financial Analysis Platform.

## Overview

The frontend provides a modern, responsive UI for financial document analysis with:
- Secure authentication and session management
- Drag-and-drop document upload
- PDF viewer with document inspection
- Real-time analysis dashboard
- Responsive design with Tailwind CSS

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.2+ | UI framework |
| **Vite** | 6.0+ | Build tool and dev server |
| **React Router** | 7.11+ | Routing and navigation |
| **Tailwind CSS** | 4.1+ | Utility-first styling |
| **Lucide React** | 0.562+ | Icon system |
| **React PDF** | 10.3+ | PDF viewer |
| **React Dropzone** | 14.3+ | File upload |

## Project Structure

```
src/
├── pages/
│   ├── Login.jsx          # Authentication page
│   └── Dashboard.jsx      # Main application dashboard
├── components/
│   ├── Layout.jsx         # Main layout wrapper
│   ├── Header.jsx         # Navigation header
│   ├── Sidebar.jsx        # Navigation sidebar
│   ├── FileUpload.jsx     # Document upload
│   ├── PDFViewer.jsx      # PDF visualization
│   ├── AnalysisDashboard.jsx  # Analysis display
│   └── ProtectedRoute.jsx # Auth guard
├── context/
│   └── AuthContext.jsx    # Global auth state
├── utils.js               # Helper functions
├── App.jsx                # Main app component
├── App.css                # Global styles
├── main.jsx               # Entry point
└── index.css              # Base styles
```

## Getting Started

### Prerequisites
- Node.js 18+
- npm 9+

### Development Setup

```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env.local

# Edit .env.local with API URL (default: http://localhost:8000)

# Start development server
npm run dev
```

The app will be available at http://localhost:5173

### Building for Production

```bash
# Build optimized bundle
npm run build

# Preview production build locally
npm run preview
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start dev server with hot reload |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint on codebase |

## Architecture

### Authentication Flow

```
1. User submits credentials on Login page
2. Frontend sends credentials to /api/v1/auth/login
3. Backend returns JWT token
4. Frontend stores token in localStorage and AuthContext
5. Protected routes check for valid token
6. All API requests include token in Authorization header
```

### Component Hierarchy

```
App
├── AuthContext (Provider)
├── ProtectedRoute
│   └── Layout
│       ├── Header
│       ├── Sidebar
│       └── Page Content
│           ├── FileUpload
│           ├── PDFViewer
│           └── AnalysisDashboard
└── Login (public route)
```

### State Management

- **AuthContext**: Global authentication state
- **Component Local State**: Form data, UI state
- **LocalStorage**: Persists auth token

## Development Guidelines

### Code Style

- Use functional components with React hooks
- Keep components focused and composable
- Use meaningful variable and component names
- Add comments for complex logic

### Component Best Practices

```jsx
// ✅ Good: Clear, focused component
function FileUpload({ onFileSelected }) {
  const [file, setFile] = useState(null)
  
  const handleDrop = (files) => {
    setFile(files[0])
    onFileSelected(files[0])
  }
  
  return (
    // JSX here
  )
}
```

## Testing

```bash
# Run ESLint
npm run lint
```

## Environment Variables

Required variables in `.env.local`:

```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=MSS Financial Analysis
VITE_APP_VERSION=0.1.0
```

## Security Considerations

- JWT Token stored in localStorage
- HTTPS required in production
- CORS configured on backend
- Input validation on client and server

## Contributing

1. Follow existing code style
2. Create feature branches from `develop`
3. Submit PR with description of changes
4. Ensure ESLint passes

## Future Improvements

- [ ] Add unit tests with Vitest
- [ ] Implement E2E tests with Playwright
- [ ] Add dark mode support
- [ ] Implement PWA capabilities
- [ ] Add offline support with Service Workers
