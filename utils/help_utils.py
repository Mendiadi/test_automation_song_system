def my_origin():
    """Get the file::function name
    using inspect to get the last call in the stack before this
    call executed."""
    import inspect
    origin = inspect.stack()[1]
    filename = origin.filename.split("\\")[-1]
    return f"{filename}::def {origin.function}(...)::line {origin.lineno}"

