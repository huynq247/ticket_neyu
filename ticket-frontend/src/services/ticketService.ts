import axios from 'axios';
import { Ticket, TicketCreateRequest, TicketUpdateRequest } from '@/types';

// For development, we'll use a fixed URL. In production, this would be set in .env
const API_URL = 'http://localhost:8080/api';

// Get auth token from local storage
const getAuthHeader = () => {
  const token = localStorage.getItem('token');
  return { Authorization: `Bearer ${token}` };
};

// Get all tickets with optional filters
export const getTickets = async (filters?: Record<string, any>) => {
  try {
    const response = await axios.get(`${API_URL}/tickets`, {
      headers: getAuthHeader(),
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching tickets:', error);
    throw error;
  }
};

// Get a single ticket by ID
export const getTicketById = async (id: string) => {
  try {
    const response = await axios.get(`${API_URL}/tickets/${id}`, {
      headers: getAuthHeader(),
    });
    return response.data;
  } catch (error) {
    console.error(`Error fetching ticket ${id}:`, error);
    throw error;
  }
};

// Create a new ticket
export const createTicket = async (ticket: TicketCreateRequest) => {
  try {
    const response = await axios.post(`${API_URL}/tickets`, ticket, {
      headers: getAuthHeader(),
    });
    return response.data;
  } catch (error) {
    console.error('Error creating ticket:', error);
    throw error;
  }
};

// Update an existing ticket
export const updateTicket = async (id: string, ticketData: TicketUpdateRequest) => {
  try {
    const response = await axios.put(`${API_URL}/tickets/${id}`, ticketData, {
      headers: getAuthHeader(),
    });
    return response.data;
  } catch (error) {
    console.error(`Error updating ticket ${id}:`, error);
    throw error;
  }
};

// Delete a ticket
export const deleteTicket = async (id: string) => {
  try {
    const response = await axios.delete(`${API_URL}/tickets/${id}`, {
      headers: getAuthHeader(),
    });
    return response.data;
  } catch (error) {
    console.error(`Error deleting ticket ${id}:`, error);
    throw error;
  }
};

// Update ticket status
export const updateTicketStatus = async (id: string, status: string) => {
  try {
    const response = await axios.patch(
      `${API_URL}/tickets/${id}/status`,
      { status },
      { headers: getAuthHeader() }
    );
    return response.data;
  } catch (error) {
    console.error(`Error updating ticket ${id} status:`, error);
    throw error;
  }
};

// Add a comment to a ticket
export const addTicketComment = async (ticketId: string, content: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/tickets/${ticketId}/comments`,
      { content },
      { headers: getAuthHeader() }
    );
    return response.data;
  } catch (error) {
    console.error(`Error adding comment to ticket ${ticketId}:`, error);
    throw error;
  }
};

// Upload attachment to a ticket
export const uploadTicketAttachment = async (ticketId: string, file: File) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
      `${API_URL}/tickets/${ticketId}/attachments`,
      formData,
      {
        headers: {
          ...getAuthHeader(),
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error(`Error uploading attachment to ticket ${ticketId}:`, error);
    throw error;
  }
};

// Get ticket statistics for dashboard
export const getTicketStatistics = async (timeRange?: string) => {
  try {
    const response = await axios.get(`${API_URL}/tickets/statistics`, {
      headers: getAuthHeader(),
      params: { timeRange },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching ticket statistics:', error);
    throw error;
  }
};