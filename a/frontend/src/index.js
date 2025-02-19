
        import React from 'react';
        import { createRoot } from 'react-dom/client';
        import App from './App';
        import 'bootstrap/dist/css/bootstrap.min.css';
        import './app.css';

        
        // Create the root element
        const container = document.getElementById('root');
        const root = createRoot(container);
        
        // Render the application
        root.render(
            <React.StrictMode>
                <App />
            </React.StrictMode>
        );

        