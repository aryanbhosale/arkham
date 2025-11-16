"""
Example Python code file for testing CodeSage
This file demonstrates various Python features for code analysis
"""

from typing import List, Dict, Optional
import json
from datetime import datetime


class User:
    """Represents a user in the system"""
    
    def __init__(self, name: str, email: str, age: Optional[int] = None):
        """
        Initialize a new user
        
        Args:
            name: User's full name
            email: User's email address
            age: User's age (optional)
        """
        self.name = name
        self.email = email
        self.age = age
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, any]:
        """Convert user to dictionary"""
        return {
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'created_at': self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        return f"User(name={self.name}, email={self.email})"


def calculate_fibonacci(n: int) -> List[int]:
    """
    Calculate Fibonacci sequence up to n terms
    
    Args:
        n: Number of terms to calculate
        
    Returns:
        List of Fibonacci numbers
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    return sequence


def process_users(users: List[User]) -> Dict[str, int]:
    """
    Process a list of users and return statistics
    
    Args:
        users: List of User objects
        
    Returns:
        Dictionary with statistics
    """
    if not users:
        return {'total': 0, 'with_age': 0}
    
    stats = {
        'total': len(users),
        'with_age': sum(1 for u in users if u.age is not None)
    }
    
    return stats


def main():
    """Main function to demonstrate the code"""
    # Create some users
    users = [
        User("Alice", "alice@example.com", 25),
        User("Bob", "bob@example.com"),
        User("Charlie", "charlie@example.com", 30)
    ]
    
    # Process users
    stats = process_users(users)
    print(f"Statistics: {json.dumps(stats, indent=2)}")
    
    # Calculate Fibonacci
    fib = calculate_fibonacci(10)
    print(f"Fibonacci sequence: {fib}")


if __name__ == "__main__":
    main()

