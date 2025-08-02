def perform_example_operation(data: str) -> str:
    """
    Performs a simple example operation on the input data.
    This function is intended to be called by an MCP tool.
    """
    return data.upper().strip() + "_PROCESSED"
