import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import api from "../api";
import PetView from '../views/PetView';

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

describe('Pet View Tests', () => {
    it('renders the main view without crashing', () => {
        const mockData = [
            {
                
                "name": "example_1",
                
                "birth_date": "2023-01-2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<PetView />);
        expect(screen.getByText(/Pet View/i)).toBeInTheDocument();
    });

    it('renders the main table', () => {
        const mockData = [
            {
                
                "name": "example_1",
                
                "birth_date": "2023-01-2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<PetView />);
        expect(screen.getByText(/Actions/i)).toBeInTheDocument();
    });


    it('opens the form modal on Add New click', () => {
        const mockData = [
            {
                
                "name": "example_1",
                
                "birth_date": "2023-01-2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<PetView />);
        fireEvent.click(screen.getByText(/Add New Pet/i));
        expect(screen.getByText(/Create Pet/i)).toBeInTheDocument();
    });

    
    
    
    
    it('renders related entity tabs for Visit', () => {
        const mockData = [
            {
                
                "name": "example_1",
                
                "birth_date": "2023-01-2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<PetView />);
        expect(screen.getAllByText(/Visit/i).length).toBeGreaterThan(1);
    });
    
    

});