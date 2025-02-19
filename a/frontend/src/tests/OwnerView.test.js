import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import api from "../api";
import OwnerView from '../views/OwnerView';

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

describe('Owner View Tests', () => {
    it('renders the main view without crashing', () => {
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<OwnerView />);
        expect(screen.getByText(/Owner View/i)).toBeInTheDocument();
    });

    it('renders the main table', () => {
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<OwnerView />);
        expect(screen.getByText(/Actions/i)).toBeInTheDocument();
    });


    it('opens the form modal on Add New click', () => {
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<OwnerView />);
        fireEvent.click(screen.getByText(/Add New Owner/i));
        expect(screen.getByText(/Create Owner/i)).toBeInTheDocument();
    });

    
    
    it('renders related entity tabs for Pet', () => {
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            }
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<OwnerView />);
        expect(screen.getAllByText(/Pet/i).length).toBeGreaterThan(1);
    });
    
    

});