from query_validator import QueryValidator

# Test it
validator = QueryValidator()

# Test valid queries
print("Testing: 'Best places in Delhi'")
result = validator.is_valid("Best places in Delhi")
print(f"Valid: {result}")  # Should be True
print()

# Test invalid queries
print("Testing: 'walk my pet'")
result = validator.is_valid("walk my pet")
print(f"Valid: {result}")  # Should be False