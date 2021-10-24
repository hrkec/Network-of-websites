class ShortestPathNotFoundError(Exception):
    """Raised when there is no path between START_URL and END_URL"""
    pass


class WebsiteNotFoundError(Exception):
    """Raised when the website doesn't exist"""
    pass


class WebsiteNotFoundInDBError(WebsiteNotFoundError):
    """Raised when the website doesn't exist in Memgraph database """
    pass


class WebsiteNotFoundNetError(WebsiteNotFoundError):
    """Raised when the website doesn't exist while scraping for network"""
    pass
