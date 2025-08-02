# src/security.py

def validate_sql_query(sql: str) -> dict:
    """Validates a SQL query to prevent basic injection attacks."""
    trimmed_sql = sql.strip().lower()
    
    if not trimmed_sql:
        return {"is_valid": False, "error": "SQL query cannot be empty"}
    
    dangerous_patterns = [
        ";", "drop", "truncate", "alter", "create", "grant", "revoke",
        "xp_cmdshell", "sp_executesql"
    ]
    
    for pattern in dangerous_patterns:
        if pattern in trimmed_sql:
            return {"is_valid": False, "error": f"Query contains potentially dangerous pattern: {pattern}"}
    
    return {"is_valid": True}

def is_write_operation(sql: str) -> bool:
    """Checks if a SQL query is a write operation."""
    trimmed_sql = sql.strip().lower()
    write_keywords = [
        "insert", "update", "delete", "create", "drop", "alter",
        "truncate", "grant", "revoke", "commit", "rollback"
    ]
    
    return any(trimmed_sql.startswith(keyword) for keyword in write_keywords)
