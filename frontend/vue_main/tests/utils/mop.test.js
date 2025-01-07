import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import axios from 'axios';
import { TokenVerifier } from '../../src/utils/mop';
import { CachedTestsVerifier } from '../../src/utils/mop';


vi.mock('axios');

describe('TokenVerifier', () => {
    describe('checkToken', () => {
        afterEach(() => {
            vi.clearAllMocks();
        });

        it('should return 401 when token or refresh is null', async () => {
            const result = await TokenVerifier.checkToken(null, null);
            expect(result).toEqual({ status: 401, new_token: null });
        });

        it('should return 200 when token is valid', async () => {
            axios.get.mockResolvedValueOnce({ status: 200 });

            const result = await TokenVerifier.checkToken('valid_token', 'refresh_token');

            expect(axios.get).toHaveBeenCalledWith('http://127.0.0.1:8000/api/auth/me', {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer valid_token`,
                },
            });
            expect(result).toEqual({ status: 200, new_token: null });
        });

        it('should return 200 with new token when refresh succeeds after token fails', async () => {
            axios.get
                .mockRejectedValueOnce(new Error('Token expired')) 
                .mockResolvedValueOnce({
                    status: 200,
                    data: { refresh_token: 'new_token' },
                });

            const result = await TokenVerifier.checkToken('expired_token', 'valid_refresh');

            expect(axios.get).toHaveBeenCalledTimes(2);
            expect(result).toEqual({ status: 200, new_token: 'new_token' });
        });

        it('should return 401 when both token and refresh fail', async () => {
            axios.get.mockRejectedValueOnce(new Error('Token expired'));
            axios.get.mockRejectedValueOnce(new Error('Refresh failed'));

            const result = await TokenVerifier.checkToken('expired_token', 'invalid_refresh');

            expect(axios.get).toHaveBeenCalledTimes(2);
            expect(result).toEqual({ status: 401, new_token: null });
        });
    });
});

describe('CachedTestsVerifier', () => {
    describe('getTest', () => {
        afterEach(() => {
            vi.clearAllMocks();
        });

        it('should return test data when request is successful', async () => {
            const mockTestData = { title: 'Quiz 000', questions: [] };
            axios.post.mockResolvedValueOnce({ data: mockTestData });

            const result = await CachedTestsVerifier.getTest('valid_token', 'easy');

            expect(axios.post).toHaveBeenCalledWith(
                'http://127.0.0.1:8000/api/auth/login',
                {
                    title: 'Quiz 000',
                    description: 'This test is auto-generated',
                    quiz_type: 'std',
                    difficulty: 'easy',
                },
                {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'uthorization': `Bearer valid_token`,
                    },
                }
            );
            expect(result).toEqual(mockTestData);
        });

        it('should return 401 when request fails', async () => {
            axios.post.mockRejectedValueOnce({ status: 401 });

            const result = await CachedTestsVerifier.getTest('invalid_token', 'easy');

            expect(result).toEqual(401);
        });
    });

    describe('checkCashedTests', () => {
        let localStorageMock;

        beforeEach(() => {
            localStorageMock = {
                getItem: vi.fn(),
                setItem: vi.fn(),
            };
            global.localStorage = localStorageMock;
            vi.spyOn(CachedTestsVerifier, 'getTest').mockResolvedValue({
                questions: [{ question: 'Sample question?', answers: [] }],
            });
        });

        afterEach(() => {
            vi.clearAllMocks();
        });

        it('should fetch and store test if not in localStorage', async () => {
            localStorageMock.getItem.mockReturnValueOnce(null);

            await CachedTestsVerifier.checkCashedTests('valid_token');

            expect(localStorageMock.getItem).toHaveBeenCalledTimes(3);
            expect(localStorageMock.setItem).toHaveBeenCalledTimes(3);
            expect(CachedTestsVerifier.getTest).toHaveBeenCalledTimes(3);
        });

        it('should not fetch test if already present in localStorage', async () => {
            localStorageMock.getItem.mockReturnValueOnce(JSON.stringify({ completed: false }));

            await CachedTestsVerifier.checkCashedTests('valid_token');

            expect(localStorageMock.getItem).toHaveBeenCalledTimes(3);
            
        });
    });

    describe('deleteStoredTests', () => {
        let localStorageMock;

        beforeEach(() => {
            localStorageMock = {
                setItem: vi.fn(),
            };
            global.localStorage = localStorageMock;
        });

        it('should reset all stored tests to null', () => {
            CachedTestsVerifier.deleteStoredTests();

            expect(localStorageMock.setItem).toHaveBeenCalledTimes(3);
            expect(localStorageMock.setItem).toHaveBeenCalledWith('easy', 'null');
            expect(localStorageMock.setItem).toHaveBeenCalledWith('medium', 'null');
            expect(localStorageMock.setItem).toHaveBeenCalledWith('hard', 'null');
        });
    });
});
