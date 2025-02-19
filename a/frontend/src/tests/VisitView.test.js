import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import api from "../api";
import VisitView from '../views/VisitView';

// Mockear Axios
jest.mock('axios', () => ({
    create: jest.fn(() => ({
        interceptors: {
            request: {
                use: jest.fn(), // Simula el método 'use' del interceptor
            },
        },
        get: jest.fn(),
        post: jest.fn(),
        put: jest.fn(),
        delete: jest.fn(),
    })),
}));


jest.mock('../api'); // Mock axios to avoid real HTTP requests

describe('Visit View Tests', () => {
    it('renders the main view without crashing', () => {
        const mockData = [
            {
                
                "visit_date": "2023-01-1",
                
                "description": "example_2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<VisitView />);
        expect(screen.getByText(/Visit View/i)).toBeInTheDocument();
    });

    it('renders the main table', () => {
        const mockData = [
            {
                
                "visit_date": "2023-01-1",
                
                "description": "example_2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<VisitView />);
        expect(screen.getByText(/Actions/i)).toBeInTheDocument();
    });


    it('opens the form modal on Add New click', () => {
        const mockData = [
            {
                
                "visit_date": "2023-01-1",
                
                "description": "example_2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<VisitView />);
        fireEvent.click(screen.getByText(/Add New Visit/i));
        expect(screen.getByText(/Create Visit/i)).toBeInTheDocument();
    });

    
    
    
    
    

});