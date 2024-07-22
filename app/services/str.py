# app/services/str.py
import re

class STR:
    @staticmethod
    def slug(string, separator = '_'):
        # Convert to lower case and remove leading/trailing whitespace
        string = string.strip().lower()
        # Replace spaces, hyphens, and invalid characters with underscores
        string = re.sub(r'[^\w\s-]', '', string.replace('-', separator))
        string = re.sub(r'[\s]+', separator, string)
        return string

    @staticmethod
    def pascal(string):
        # Convert to title case and remove invalid characters
        string = re.sub(r'[^\w\s]', '', string.title())
        # Remove spaces and underscores
        string = re.sub(r'[\s_]+', '', string)
        return string
