# crypto_helper_scripts.py #

class OsintHelper:
    
    """
    _summary_
    A class to encapsulate helper functions specifically for OSINT'ing ;)
    """
    
    @staticmethod
    def defang_url(url):
        """
        Function to 'defang' a URL to prevent it from being clickable to prevent accidental OPSEC challenges.
        
        Args:
            url (_type_): any url (with or without 'http/https')
        """
        