/**
 * Example JavaScript code file for testing CodeSage
 * Demonstrates various JavaScript features
 */

class Calculator {
  /**
   * Create a new Calculator instance
   */
  constructor() {
    this.history = [];
  }

  /**
   * Add two numbers
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {number} Sum of a and b
   */
  add(a, b) {
    const result = a + b;
    this.history.push({ operation: 'add', a, b, result });
    return result;
  }

  /**
   * Multiply two numbers
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {number} Product of a and b
   */
  multiply(a, b) {
    const result = a * b;
    this.history.push({ operation: 'multiply', a, b, result });
    return result;
  }

  /**
   * Get calculation history
   * @returns {Array} Array of calculation records
   */
  getHistory() {
    return this.history;
  }

  /**
   * Clear calculation history
   */
  clearHistory() {
    this.history = [];
  }
}

// Arrow function example
const greet = (name) => {
  return `Hello, ${name}!`;
};

// Async function example
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user data:', error);
    throw error;
  }
}

// Higher-order function
function createMultiplier(factor) {
  return (number) => number * factor;
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Calculator, greet, fetchUserData, createMultiplier };
}

