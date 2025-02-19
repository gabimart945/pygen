import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import api from "../api";
import VetForm from '../components/VetForm';

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

describe('VetForm Component Tests', () => {
    it('renders loading state when fetching data', async () => {
        api.get.mockResolvedValueOnce({ data: { name: 'John Doe' } });

        render(<VetForm id={1} />);
        expect(screen.getByText(/Loading/i)).toBeInTheDocument();

        await waitFor(() => {
            expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument();
        });
    });

    it('renders error state on API failure', async () => {
        api.get.mockRejectedValueOnce(new Error('Error fetching data'));

        render(<VetForm id={1} />);
        await waitFor(() => {
            expect(screen.getByText(/Error:/i)).toBeInTheDocument();
        });
    });

    it('updates form fields correctly', () => {
        render(<VetForm />);
        
        const input1 = screen.getByLabelText(/first_name/i);
        fireEvent.change(input1, {
            target: {
                value: "Test Value"
            }
        });
        expect(input1.value).toBe("Test Value");
        
        const input2 = screen.getByLabelText(/last_name/i);
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

        render(<VetForm onSuccess={mockOnSuccess} />);
        
        const input1 = screen.getByLabelText(/first_name/i);
        fireEvent.change(input1, { target: { value: 'Test Value 1' } });
        
        const input2 = screen.getByLabelText(/last_name/i);
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
                
                "first_name": "example_1",
                
                "last_name": "example_2",
                
            },
        ];
        api.get.mockResolvedValueOnce({ data: mockData });
        api.put.mockResolvedValueOnce({ data: { id: 1 } });
        const mockOnSuccess = jest.fn();

        render(<VetForm id={1} onSuccess={mockOnSuccess} />);
        
        const input1 = screen.getByLabelText(/first_name/i);
        fireEvent.change(input1, { target: { value: 'Updated Value 1' } });
        
        const input2 = screen.getByLabelText(/last_name/i);
        fireEvent.change(input2, { target: { value: 'Updated Value 2' } });
        

        fireEvent.click(screen.getByText(/Update/i));

        await waitFor(() => {
            expect(mockOnSuccess).toHaveBeenCalled();
        });
    });
    */
});