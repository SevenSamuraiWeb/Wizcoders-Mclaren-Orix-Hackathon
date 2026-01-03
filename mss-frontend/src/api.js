/**
 * API Client Utilities
 *
 * Provides reusable HTTP client functions with built-in error handling,
 * authentication, and request/response interceptors.
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Get authorization headers with JWT token
 * @returns {Object} Headers object with authorization
 */
export const getAuthHeaders = () => {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  }
}

/**
 * Fetch wrapper with error handling and auth
 * @param {string} endpoint - API endpoint (e.g., '/api/v1/docs')
 * @param {Object} options - Fetch options
 * @returns {Promise<Object>} Response data
 */
export const apiFetch = async (endpoint, options = {}) => {
  const url = `${API_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      headers: getAuthHeaders(),
      ...options,
    })

    // Handle 401 - unauthorized (token expired/invalid)
    if (response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
      throw new Error('Session expired. Please login again.')
    }

    // Parse response
    const data = await response.json()

    // Handle error responses
    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    return data
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error.message)
    throw error
  }
}

/**
 * POST request helper
 * @param {string} endpoint - API endpoint
 * @param {Object} body - Request body
 * @returns {Promise<Object>} Response data
 */
export const apiPost = (endpoint, body) => {
  return apiFetch(endpoint, {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

/**
 * GET request helper
 * @param {string} endpoint - API endpoint
 * @returns {Promise<Object>} Response data
 */
export const apiGet = (endpoint) => {
  return apiFetch(endpoint, {
    method: 'GET',
  })
}

/**
 * PUT request helper
 * @param {string} endpoint - API endpoint
 * @param {Object} body - Request body
 * @returns {Promise<Object>} Response data
 */
export const apiPut = (endpoint, body) => {
  return apiFetch(endpoint, {
    method: 'PUT',
    body: JSON.stringify(body),
  })
}

/**
 * DELETE request helper
 * @param {string} endpoint - API endpoint
 * @returns {Promise<Object>} Response data
 */
export const apiDelete = (endpoint) => {
  return apiFetch(endpoint, {
    method: 'DELETE',
  })
}

/**
 * Upload file with progress tracking
 * @param {string} endpoint - API endpoint
 * @param {File} file - File to upload
 * @param {Function} onProgress - Progress callback
 * @returns {Promise<Object>} Response data
 */
export const apiUploadFile = async (endpoint, file, onProgress) => {
  const url = `${API_URL}${endpoint}`
  const formData = new FormData()
  formData.append('file', file)

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()

    // Track upload progress
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable && onProgress) {
        const percentComplete = (e.loaded / e.total) * 100
        onProgress(percentComplete)
      }
    })

    // Handle completion
    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve(response)
        } catch (error) {
          reject(new Error('Failed to parse response'))
        }
      } else {
        reject(new Error(`Upload failed: ${xhr.status}`))
      }
    })

    // Handle error
    xhr.addEventListener('error', () => {
      reject(new Error('Upload failed'))
    })

    // Set headers and send
    const token = localStorage.getItem('token')
    xhr.open('POST', url)
    if (token) {
      xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    }
    xhr.send(formData)
  })
}

/**
 * Authentication API calls
 */
export const authAPI = {
  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<Object>} Token and user info
   */
  login: async (email, password) => {
    const response = await apiPost('/api/v1/auth/login', { email, password })
    return response
  },

  /**
   * Get current user info
   * @returns {Promise<Object>} User information
   */
  getCurrentUser: async () => {
    return apiGet('/api/v1/auth/me')
  },

  /**
   * Logout user
   */
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
}

/**
 * Document API calls
 */
export const documentAPI = {
  /**
   * Upload document
   * @param {File} file - File to upload
   * @param {Function} onProgress - Progress callback
   * @returns {Promise<Object>} Upload result
   */
  upload: async (file, onProgress) => {
    return apiUploadFile('/api/v1/docs/upload', file, onProgress)
  },

  /**
   * Get document analysis
   * @param {string} documentId - Document ID
   * @returns {Promise<Object>} Analysis result
   */
  getAnalysis: async (documentId) => {
    return apiGet(`/api/v1/docs/${documentId}/analysis`)
  },

  /**
   * List user documents
   * @returns {Promise<Array>} List of documents
   */
  list: async () => {
    return apiGet('/api/v1/docs')
  },

  /**
   * Delete document
   * @param {string} documentId - Document ID
   * @returns {Promise<Object>} Delete result
   */
  delete: async (documentId) => {
    return apiDelete(`/api/v1/docs/${documentId}`)
  },
}

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
  try {
    return await apiGet('/health')
  } catch (error) {
    return null
  }
}
