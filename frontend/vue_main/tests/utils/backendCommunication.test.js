import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import axios from 'axios'
import { AccountService, UserInfo, QuizInfo , AuthService} from '../../src/utils/backendCommunication'

vi.mock('axios')


// Mock global fetch
global.fetch = vi.fn()

describe('AccountService', () => {
  // Cleanup after each test
  afterEach(() => {
    vi.resetAllMocks()
  })

  // Successful account creation scenario
  describe('createAccount - Success', () => {
    it('should create an account successfully', async () => {
      // Prepare mock data
      const mockUserData = {
        name: 'testuser',
        email: 'test@example.com',
        password: 'ValidPassword123!'
      }

      // Mock successful fetch response
      const mockSuccessResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({ 
          id: '123', 
          username: 'testuser', 
          email: 'test@example.com' 
        })
      }
      global.fetch.mockResolvedValue(mockSuccessResponse)

      // Call the method
      const result = await AccountService.createAccount(mockUserData)

      // Assertions
      expect(global.fetch).toHaveBeenCalledOnce()
      expect(global.fetch).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/api/auth/register',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: mockUserData.name,
            email: mockUserData.email,
            password: mockUserData.password,
            institution: "UAIC",
            year_of_study: 2
          })
        }
      )
      expect(result).toEqual({
        id: '123', 
        username: 'testuser', 
        email: 'test@example.com'
      })
    })
  })

  // Failed account creation scenario
  describe('createAccount - Failure', () => {
    it('should handle registration error', async () => {
      // Prepare mock data
      const mockUserData = {
        name: 'testuser',
        email: 'test@example.com',
        password: 'ValidPassword123!'
      }

      // Mock error response
      const mockErrorResponse = {
        ok: false,
        json: vi.fn().mockResolvedValue({ 
          errors: [{ 
            message: 'Email already exists' 
          }] 
        })
      }
      global.fetch.mockResolvedValue(mockErrorResponse)

      // Call the method
      const result = await AccountService.createAccount(mockUserData)

      // Assertions
      expect(global.fetch).toHaveBeenCalledOnce()
      expect(result).toEqual({
        message: ['Email already exists']
      })
    })
  })

  // Network error scenario
  describe('createAccount - Network Error', () => {
    it('should throw an error on network failure', async () => {
      // Prepare mock data
      const mockUserData = {
        name: 'testuser',
        email: 'test@example.com',
        password: 'ValidPassword123!'
      }

      // Mock network error
      global.fetch.mockRejectedValue(new Error('Network failure'))

      // Assertions
      await expect(AccountService.createAccount(mockUserData))
        .rejects
        .toThrow('Network failure')
    })
  })

  // Edge case: empty or invalid input
  describe('createAccount - Input Validation', () => {
    it('should handle empty input data', async () => {
      // Prepare mock data
      const mockUserData = {}

      // Mock fetch to prevent actual network call
      global.fetch.mockResolvedValue({
        ok: false,
        json: vi.fn().mockResolvedValue({ 
          errors: [{ 
            message: 'Invalid input data' 
          }] 
        })
      })

      // Call the method
      const result = await AccountService.createAccount(mockUserData)

      // Assertions
      expect(global.fetch).toHaveBeenCalledOnce()
      expect(result).toEqual({
        message: ['Invalid input data']
      })
    })
  })
})


describe('UserInfo Service', () => {
    const mockToken = 'test-token-123'
  
    // Cleanup after each test
    afterEach(() => {
      vi.resetAllMocks()
    })
  
    // Successful user info retrieval
    describe('getUserInfo - Success', () => {
      it('should retrieve user information successfully', async () => {
        // Prepare mock successful response
        const mockUserResponse = {
          data: {
            id: '123',
            username: 'testuser',
            email: 'test@example.com'
          }
        }
        
        // Mock axios get method
        axios.get.mockResolvedValue(mockUserResponse)
  
        // Call the method
        const result = await UserInfo.getUserInfo(mockToken)
  
        // Assertions
        expect(axios.get).toHaveBeenCalledOnce()
        expect(axios.get).toHaveBeenCalledWith('http://127.0.0.1:8000/api/auth/me', {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${mockToken}`
          }
        })
        expect(result.data).toEqual(mockUserResponse.data)
      })
    })
  
    // Failed user info retrieval
    describe('getUserInfo - Failure', () => {
      it('should throw an error when authentication fails', async () => {
        // Mock axios to throw an error
        const mockError = new Error('Authentication failed')
        mockError.response = {
          status: 401,
          data: { message: 'Invalid token' }
        }
        axios.get.mockRejectedValue(mockError)
  
        // Assertions
        await expect(UserInfo.getUserInfo(mockToken))
          .rejects
          .toThrow('Authentication failed')
  
        expect(axios.get).toHaveBeenCalledOnce()
      })
    })
  })
  
  describe('QuizInfo Service', () => {
    const mockToken = 'test-token-123'
  
    // Cleanup after each test
    afterEach(() => {
      vi.resetAllMocks()
    })
  
    // Successful quiz info retrieval
    describe('getQuizInfo - Success', () => {
      it('should retrieve quiz information successfully', async () => {
        // Prepare mock successful response
        const mockQuizResponse = {
          data: {
            quizzes: [
              { id: '1', title: 'Math Quiz', status: 'active' },
              { id: '2', title: 'Science Quiz', status: 'pending' }
            ]
          }
        }
        
        // Mock axios get method
        axios.get.mockResolvedValue(mockQuizResponse)
  
        // Call the method
        const result = await QuizInfo.getQuizInfo(mockToken)
  
        // Assertions
        expect(axios.get).toHaveBeenCalledOnce()
        expect(axios.get).toHaveBeenCalledWith('http://127.0.0.1:8000/api/quiz/', {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${mockToken}`
          }
        })
        expect(result.data).toEqual(mockQuizResponse.data)
      })
    })
  
    // Failed quiz info retrieval
    describe('getQuizInfo - Failure', () => {
      it('should throw an error when quiz retrieval fails', async () => {
        // Mock axios to throw an error
        const mockError = new Error('Quiz retrieval failed')
        mockError.response = {
          status: 403,
          data: { message: 'Not authorized to access quizzes' }
        }
        axios.get.mockRejectedValue(mockError)
  
        // Assertions
        await expect(QuizInfo.getQuizInfo(mockToken))
          .rejects
          .toThrow('Quiz retrieval failed')
  
        expect(axios.get).toHaveBeenCalledOnce()
      })
    })
  
    // Edge case: empty or invalid token
    describe('getQuizInfo - Token Validation', () => {
      it('should handle empty token', async () => {
        // Mock axios to throw an error
        const mockError = new Error('Invalid token')
        mockError.response = {
          status: 401,
          data: { message: 'Token is required' }
        }
        axios.get.mockRejectedValue(mockError)
  
        // Assertions
        await expect(QuizInfo.getQuizInfo(''))
          .rejects
          .toThrow('Invalid token')
  
        expect(axios.get).toHaveBeenCalledOnce()
      })
    })
  })
  
vi.mock('axios')

describe('AuthService', () => {
  // Cleanup after each test
  afterEach(() => {
    vi.resetAllMocks()
  })

  // Successful login scenario
  describe('getToken - Successful Login', () => {
    it('should successfully retrieve token for valid credentials', async () => {
      // Prepare mock data
      const mockEmail = 'test@example.com'
      const mockPassword = 'validPassword123!'

      // Mock successful axios response
      const mockSuccessResponse = {
        data: {
          access_token: 'mock-jwt-token',
          token_type: 'Bearer'
        },
        status: 200
      }
      axios.post.mockResolvedValue(mockSuccessResponse)

      // Call the method
      const result = await AuthService.getToken(mockEmail, mockPassword)

      // Assertions
      expect(axios.post).toHaveBeenCalledOnce()
      expect(axios.post).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/api/auth/login', 
        {
          username: mockEmail,
          password: mockPassword
        },
        {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )
      expect(result).toEqual(mockSuccessResponse)
    })
  })

  // Failed login scenario
  describe('getToken - Failed Login', () => {
    it('should return 401 for invalid credentials', async () => {
      // Prepare mock data
      const mockEmail = 'invalid@example.com'
      const mockPassword = 'wrongPassword'

      // Mock failed axios response
      const mockErrorResponse = new Error('Authentication failed')
      mockErrorResponse.response = {
        status: 401,
        data: { message: 'Invalid credentials' }
      }
      axios.post.mockRejectedValue(mockErrorResponse)

      // Call the method
      const result = await AuthService.getToken(mockEmail, mockPassword)

      // Assertions
      expect(axios.post).toHaveBeenCalledOnce()
      expect(result).toBe(401)
    })
  })

  // Network error scenario
  describe('getToken - Network Error', () => {
    it('should handle network errors', async () => {
      // Prepare mock data
      const mockEmail = 'test@example.com'
      const mockPassword = 'validPassword123!'

      // Mock network error
      const mockNetworkError = new Error('Network error')
      mockNetworkError.response = {
        status: 500
      }
      axios.post.mockRejectedValue(mockNetworkError)

      // Call the method
      const result = await AuthService.getToken(mockEmail, mockPassword)

      // Assertions
      expect(axios.post).toHaveBeenCalledOnce()
      expect(result).toBe(401)
    })
  })

  // Edge case: empty input
  describe('getToken - Input Validation', () => {
    it('should handle empty input credentials', async () => {
      // Mock axios to prevent actual network call
      axios.post.mockRejectedValue(new Error('Invalid input'))

      // Call the method with empty credentials
      const result = await AuthService.getToken('', '')

      // Assertions
      expect(axios.post).toHaveBeenCalledOnce()
      expect(result).toBe(401)
    })
  })
})