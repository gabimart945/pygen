import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import api from "../api";
import OwnerTable from '../components/OwnerTable';

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

describe('OwnerTable Component Tests', () => {
    it('renders loading state initially', () => {
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            },
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        render(<OwnerTable />);
        expect(screen.getByText(/Loading/i)).toBeInTheDocument();
    });

    it('renders error state on API failure', async () => {
        api.get.mockRejectedValueOnce(new Error('Error fetching data'));
        render(<OwnerTable />);
        await waitFor(() => {
            expect(screen.getByText(/Error:/i)).toBeInTheDocument();
        });
    });

    it('renders data correctly when passed as props', () => {
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            }
        ];
        render(<OwnerTable data={mockData} />);
        
        expect(screen.getByText("example_1")).toBeInTheDocument();
        
        expect(screen.getByText("example_2")).toBeInTheDocument();
        
    });

    it('fetches data when no props are provided', async () => {
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            },
        ];
        api.get.mockResolvedValueOnce({ data: mockData });

        render(<OwnerTable />);
        await waitFor(() => {
            
            expect(screen.getByText("example_1")).toBeInTheDocument();
            
            expect(screen.getByText("example_2")).toBeInTheDocument();
            
        });
    });

    it('triggers onEdit callback when Edit is clicked', () => {
        const mockEdit = jest.fn();
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            },
        ];
        render(<OwnerTable data={mockData} onEdit={mockEdit} />);
        fireEvent.click(screen.getByText(/Edit/i));
        expect(mockEdit).toHaveBeenCalledWith(mockData[0]);
    });

    it('triggers onDelete callback when Delete is clicked', () => {
        const mockDelete = jest.fn();
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            },
        ];
        render(<OwnerTable data={mockData} onDelete={mockDelete} />);
        fireEvent.click(screen.getByText(/Delete/i));
        expect(mockDelete).toHaveBeenCalledWith(mockData[0].id);
    });

    it('triggers onSelect callback when a row is clicked', () => {
        const mockSelect = jest.fn();
        const mockData = [
            {
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            },
        ];
        render(<OwnerTable data={mockData} onSelect={mockSelect} />);
        fireEvent.click(screen.getByText(/example_1/i));
        expect(mockSelect).toHaveBeenCalledWith(mockData[0]);
    });
});