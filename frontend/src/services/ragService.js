/**
 * @file ragService.js
 * @description Service layer for all RAG pipeline API calls.
 *              Connects React frontend to the 16 RAG pipelines
 *              running on the FastAPI backend.
 *              Follows Single Responsibility Principle — only RAG calls here.
 */
import api from './api'

// ─── RAG Service ─────────────────────────────────────────────────────────────
const ragService = {

  /**
   * Query the RAG pipeline with a question
   * @param {string} question - Student's question
   * @param {string} pipeline - RAG type (naive, hyde, fusion, etc.)
   * @returns {Promise} - AI generated answer
   */
  async query(question, pipeline = 'naive') {
    try {
      const response = await api.post('/rag/query', {
        question,
        pipeline_type: pipeline,
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'RAG query failed')
    }
  },

  /**
   * Get list of all available RAG pipelines
   * @returns {Promise} - List of 16 RAG pipeline names
   */
  async getPipelines() {
    try {
      const response = await api.get('/rag/pipelines')
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch pipelines')
    }
  },

  /**
   * Get RAG query history for current user
   * @returns {Promise} - List of past queries and answers
   */
  async getHistory() {
    try {
      const response = await api.get('/rag/history')
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch history')
    }
  },
}

export default ragService