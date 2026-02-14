# https://pypi.org/project/pyShortUrl/


import pyshorteners


def shorten_url(url: str) -> str:
    """
    Shortens a given URL using the shortener module.

    Args:
        url (str): The URL to be shortened.

    Returns:
        str: The shortened URL.
    """
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

if __name__ == "__main__":
    url = input("Enter the URL to shorten: ")
    shortened_url = shorten_url(url)
    print(f"Shortened URL: {shortened_url}")
