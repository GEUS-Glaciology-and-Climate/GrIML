try:
    from importlib.metadata import version
except ImportError:  # For Python <3.8 compatibility
    from importlib_metadata import version

__version__ = version("griml")  # Replace with your actual package name
