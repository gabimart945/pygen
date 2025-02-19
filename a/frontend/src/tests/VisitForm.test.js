import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import api from "../api";
import VisitForm from '../components/VisitForm';

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

describe('VisitForm Component Tests', () => {
    it('renders loading state when fetching data', async () => {
        api.get.mockResolvedValueOnce({ data: { name: 'John Doe' } });

        render(<VisitForm id={1} />);
        expect(screen.getByText(/Loading/i)).toBeInTheDocument();

        await waitFor(() => {
            expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument();
        });
    });

    it('renders error state on API failure', async () => {
        api.get.mockRejectedValueOnce(new Error('Error fetching data'));

        render(<VisitForm id={1} />);
        await waitFor(() => {
            expect(screen.getByText(/Error:/i)).toBeInTheDocument();
        });
    });

    it('updates form fields correctly', () => {
        render(<VisitForm />);
        
        const input1 = screen.getByLabelText(/visit_date/i);
        fireEvent.change(input1, {
            target: {
                value: "2023-01-01"
            }
        });
        expect(input1.value).toBe("2023-01-01");
        
        const input2 = screen.getByLabelText(/description/i);
        fireEvent.change(input2, {
            target: {
                value: "Test Value"
            }
        });
        expect(input2.value).toBe("Test Value");
        
    });


    it('submits the form with correct data', async () => {
        api.post.mockResolvedValueOnce({ data: { id: 1 } });
        const mockOnSuccess = jest.fn();

        render(<VisitForm onSuccess={mockOnSuccess} />);
        
        const input1 = screen.getByLabelText(/visit_date/i);
        fireEvent.change(input1, { target: { value: 'Test Value 1' } });
        
        const input2 = screen.getByLabelText(/description/i);
        fireEvent.change(input2, { target: { value: 'Test Value 2' } });
        

        fireEvent.click(screen.getByText(/Create/i));

        await waitFor(() => {
            expect(mockOnSuccess).toHaveBeenCalled();
        });
    });

    /*
    it('handles update correctly', async () => {
        const mockData = [
            {
                
                "visit_date": "2023-01-2",
                
                "description": "example_2",
                
            },
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        api.put.mockResolvedValueOnce({ data: { id: 1 } });
        const mockOnSuccess = jest.fn();

        render(<VisitForm id={1} onSuccess={mockOnSuccess} />);
        
        const input1 = screen.getByLabelText(/visit_date/i);
        fireEvent.change(input1, { target: { value: 'Updated Value 1' } });
        
        const input2 = screen.getByLabelText(/description/i);
        fireEvent.change(input2, { target: { value: 'Updated Value 2' } });
        

        fireEvent.click(screen.getByText(/Update/i));

        await waitFor(() => {
            expect(mockOnSuccess).toHaveBeenCalled();
        });
    });
    */
});