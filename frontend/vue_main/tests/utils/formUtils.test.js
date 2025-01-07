import { describe, it, expect } from 'vitest'
import { validatePassword } from '../../src/utils/formUtils'

describe('Password Validation Function', () => {
  describe('Minimum Length Validation', () => {
    it('should return an error for passwords shorter than 8 characters', () => {
      const errors = validatePassword('short', 'short')
      expect(errors).toContain('Password must be at least 8 characters long')
    })

    it('should not return length error for passwords 8 characters or longer', () => {
      const errors = validatePassword('longEnough1!', 'longEnough1!')
      expect(errors).not.toContain('Password must be at least 8 characters long')
    })
  })

  describe('Uppercase Letter Validation', () => {
    it('should return an error if no uppercase letter is present', () => {
      const errors = validatePassword('nouppercase1!', 'nouppercase1!')
      expect(errors).toContain('Password must contain at least one uppercase letter')
    })

    it('should not return uppercase error if an uppercase letter is present', () => {
      const errors = validatePassword('Uppercase1!', 'Uppercase1!')
      expect(errors).not.toContain('Password must contain at least one uppercase letter')
    })
  })

  describe('Lowercase Letter Validation', () => {
    it('should return an error if no lowercase letter is present', () => {
      const errors = validatePassword('NOLOWERCASE1!', 'NOLOWERCASE1!')
      expect(errors).toContain('Password must contain at least one lowercase letter')
    })

    it('should not return lowercase error if a lowercase letter is present', () => {
      const errors = validatePassword('Lowercase1!', 'Lowercase1!')
      expect(errors).not.toContain('Password must contain at least one lowercase letter')
    })
  })

  describe('Number Validation', () => {
    it('should return an error if no number is present', () => {
      const errors = validatePassword('NoNumberHere!', 'NoNumberHere!')
      expect(errors).toContain('Password must contain at least one number')
    })

    it('should not return number error if a number is present', () => {
      const errors = validatePassword('Number1!', 'Number1!')
      expect(errors).not.toContain('Password must contain at least one number')
    })
  })

  describe('Special Character Validation', () => {
    it('should return an error if no special character is present', () => {
      const errors = validatePassword('NoSpecialChar1', 'NoSpecialChar1')
      expect(errors).toContain('Password must contain at least one special character')
    })

    it('should not return special character error if a special character is present', () => {
      const errors = validatePassword('Special1!', 'Special1!')
      expect(errors).not.toContain('Password must contain at least one special character')
    })
  })

  describe('Space Validation', () => {
    it('should return an error if spaces are present', () => {
      const errors = validatePassword('Space 1!Test', 'Space 1!Test')
      expect(errors).toContain('Password must not contain spaces')
    })

    it('should not return space error if no spaces are present', () => {
      const errors = validatePassword('NoSpaces1!', 'NoSpaces1!')
      expect(errors).not.toContain('Password must not contain spaces')
    })
  })

  describe('Consecutive Characters Validation', () => {
    it('should return an error for three or more consecutive identical characters', () => {
      const errors = validatePassword('Password111!', 'Password111!')
      expect(errors).toContain('Password must not contain three or more consecutive identical characters')
    })

    it('should not return consecutive characters error for less than three consecutive characters', () => {
      const errors = validatePassword('Password11!', 'Password11!')
      expect(errors).not.toContain('Password must not contain three or more consecutive identical characters')
    })
  })

  describe('Password Matching Validation', () => {
    it('should return an error if passwords do not match', () => {
      const errors = validatePassword('Password1!', 'DifferentPassword1!')
      expect(errors).toContain('Passwords do not match')
    })

    it('should not return password mismatch error if passwords match', () => {
      const errors = validatePassword('MatchingPassword1!', 'MatchingPassword1!')
      expect(errors).not.toContain('Passwords do not match')
    })
  })

  describe('Valid Password Scenario', () => {
    it('should return no errors for a valid password', () => {
      const errors = validatePassword('ValidPass1!', 'ValidPass1!')
      expect(errors).toHaveLength(0)
    })
  })
})