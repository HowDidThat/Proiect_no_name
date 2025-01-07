import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import axios from 'axios'
import { AccountService, UserInfo, QuizInfo , AuthService} from '../../src/utils/backendCommunication'

vi.mock('axios')


global.fetch = vi.fn()

describe('AccountService', () => {

  afterEach(() => {
    vi.resetAllMocks()
  })


  describe('createAccount - Success', () => {
    it('should create an account successfully', async () => {

      const mockUserData = {
        name: 'testuser',
        email: 'test@example.com',
        password: 'ValidPassword123!'
      }

      const mockSuccessResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({ 
          id: '123', 
          username: 'testuser', 
          email: 'test@example.com' 
        })
      }
      global.fetch.mockResolvedValue(mockSuccessResponse)

      const result = await AccountService.createAccount(mockUserData)

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

  describe('createAccount - Failure', () => {
    it('should handle registration error', async () => {

      const mockUserData = {
        name: 'testuser',
        email: 'test@example.com',
        password: 'ValidPassword123!'
      }

      const mockErrorResponse = {
        ok: false,
        json: vi.fn().mockResolvedValue({ 
          errors: [{ 
            message: 'Email already exists' 
          }] 
        })
      }
      global.fetch.mockResolvedValue(mockErrorResponse)

      const result = await AccountService.createAccount(mockUserData)

      expect(global.fetch).toHaveBeenCalledOnce()
      expect(result).toEqual({
        message: ['Email already exists']
      })
    })
  })

  describe('createAccount - Network Error', () => {
    it('should throw an error on network failure', async () => {

      const mockUserData = {
        name: 'testuser',
        email: 'test@example.com',
        password: 'ValidPassword123!'
      }


      global.fetch.mockRejectedValue(new Error('Network failure'))
      await expect(AccountService.createAccount(mockUserData))
        .rejects
        .toThrow('Network failure')
    })
  })

  describe('createAccount - Input Validation', () => {
    it('should handle empty input data', async () => {

      const mockUserData = {}

      global.fetch.mockResolvedValue({
        ok: false,
        json: vi.fn().mockResolvedValue({ 
          errors: [{ 
            message: 'Invalid input data' 
          }] 
        })
      })

      const result = await AccountService.createAccount(mockUserData)

      expect(global.fetch).toHaveBeenCalledOnce()
      expect(result).toEqual({
        message: ['Invalid input data']
      })
    })
  })
})


describe('UserInfo Service', () => {
    const mockToken = 'test-token-123'

    afterEach(() => {
      vi.resetAllMocks()
    })

    describe('getUserInfo - Success', () => {
      it('should retrieve user information successfully', async () => {

        const mockUserResponse = {
          data: {
            id: '123',
            username: 'testuser',
            email: 'test@example.com'
          }
        }

        axios.get.mockResolvedValue(mockUserResponse)

        const result = await UserInfo.getUserInfo(mockToken)

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

    describe('getUserInfo - Failure', () => {
      it('should throw an error when authentication fails', async () => {

        const mockError = new Error('Authentication failed')
        mockError.response = {
          status: 401,
          data: { message: 'Invalid token' }
        }
        axios.get.mockRejectedValue(mockError)

        await expect(UserInfo.getUserInfo(mockToken))
          .rejects
          .toThrow('Authentication failed')
  
        expect(axios.get).toHaveBeenCalledOnce()
      })
    })
  })
  
  describe('QuizInfo Service', () => {
    const mockToken = 'test-token-123'

    afterEach(() => {
      vi.resetAllMocks()
    })

    describe('getQuizInfo - Success', () => {
      it('should retrieve quiz information successfully', async () => {

        const mockQuizResponse = {
          data: {
            quizzes: [
              { id: '1', title: 'Math Quiz', status: 'active' },
              { id: '2', title: 'Science Quiz', status: 'pending' }
            ]
          }
        }

        axios.get.mockResolvedValue(mockQuizResponse)

        const result = await QuizInfo.getQuizInfo(mockToken)

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

    describe('getQuizInfo - Failure', () => {
      it('should throw an error when quiz retrieval fails', async () => {

        const mockError = new Error('Quiz retrieval failed')
        mockError.response = {
          status: 403,
          data: { message: 'Not authorized to access quizzes' }
        }
        axios.get.mockRejectedValue(mockError)

        await expect(QuizInfo.getQuizInfo(mockToken))
          .rejects
          .toThrow('Quiz retrieval failed')
  
        expect(axios.get).toHaveBeenCalledOnce()
      })
    })

    describe('getQuizInfo - Token Validation', () => {
      it('should handle empty token', async () => {
        const mockError = new Error('Invalid token')
        mockError.response = {
          status: 401,
          data: { message: 'Token is required' }
        }
        axios.get.mockRejectedValue(mockError)

        await expect(QuizInfo.getQuizInfo(''))
          .rejects
          .toThrow('Invalid token')
  
        expect(axios.get).toHaveBeenCalledOnce()
      })
    })
  })
  
vi.mock('axios')

describe('AuthService', () => {

  afterEach(() => {
    vi.resetAllMocks()
  })


  describe('getToken - Successful Login', () => {
    it('should successfully retrieve token for valid credentials', async () => {

      const mockEmail = 'test@example.com'
      const mockPassword = 'validPassword123!'

      const mockSuccessResponse = {
        data: {
          access_token: 'mock-jwt-token',
          token_type: 'Bearer'
        },
        status: 200
      }
      axios.post.mockResolvedValue(mockSuccessResponse)


      const result = await AuthService.getToken(mockEmail, mockPassword)

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

  describe('getToken - Failed Login', () => {
    it('should return 401 for invalid credentials', async () => {

      const mockEmail = 'invalid@example.com'
      const mockPassword = 'wrongPassword'

      const mockErrorResponse = new Error('Authentication failed')
      mockErrorResponse.response = {
        status: 401,
        data: { message: 'Invalid credentials' }
      }
      axios.post.mockRejectedValue(mockErrorResponse)

      const result = await AuthService.getToken(mockEmail, mockPassword)

      expect(axios.post).toHaveBeenCalledOnce()
      expect(result).toBe(401)
    })
  })

  describe('getToken - Network Error', () => {
    it('should handle network errors', async () => {

      const mockEmail = 'test@example.com'
      const mockPassword = 'validPassword123!'


      const mockNetworkError = new Error('Network error')
      mockNetworkError.response = {
        status: 500
      }
      axios.post.mockRejectedValue(mockNetworkError)

      const result = await AuthService.getToken(mockEmail, mockPassword)
      expect(axios.post).toHaveBeenCalledOnce()
      expect(result).toBe(401)
    })
  })

  describe('getToken - Input Validation', () => {
    it('should handle empty input credentials', async () => {
 
      axios.post.mockRejectedValue(new Error('Invalid input'))


      const result = await AuthService.getToken('', '')

      expect(axios.post).toHaveBeenCalledOnce()
      expect(result).toBe(401)
    })
  })
})