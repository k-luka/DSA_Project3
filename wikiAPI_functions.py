import wikipediaapi
import re
from collections import Counter

def get_wikipedia_page_links(page_title):
    # Configuration for Wikipedia API access
    config = {
        "language": "en",
        "user_agent": "MyWikiCrawler/1.0 (your-email@example.com)"
    }

    # Initialize the Wikipedia API with configuration
    wiki_wiki = wikipediaapi.Wikipedia(**config)

    # Fetch the page for the given title
    page = wiki_wiki.page(page_title)

    # Check if the page exists
    if not page.exists():
        return "Page not found"

    # List to store titles of linked pages
    links_titles = []

    # Loop through the links on the page
    for link in page.links.values():
        # Append the title of each linked page to the list
        links_titles.append(link.title)

    return links_titles

def get_wikipedia_page_text(page_title):
    # Configure the user agent for Wikipedia API access
    config = {
        "language": "en",
        "user_agent": "MyWikiCrawler/1.0 (kirilldenisluka@gmail.com)"
    }

    # Initialize the Wikipedia API with configuration
    wiki_wiki = wikipediaapi.Wikipedia(**config)

    # Fetch the page for the given title
    page = wiki_wiki.page(page_title)

    # Check if the page exists
    if page.exists():
        # Return the text of the page
        return page.text
    else:
        return "Page not found"


def get_word_frequency(page_title):
    # List of common stop words to exclude
    stop_words = set([
        "the", "and", "a", "an", "in", "on", "at", "for", "with", "about", "as", "to", "of", "it",
        "by", "from", "that", "this", "but", "up", "down", "out", "or", "when", "which", "who",
        "what", "is", "are", "was", "were", "be", "being", "been", "have", "has", "had", "do",
        "does", "did", "will", "would", "shall", "should", "can", "could", "may", "might", "must", "ought",
        "also", "s", "its", "such", "than", "many", "much"
    ])

    # Get the text of the page using the previously defined function
    text = get_wikipedia_page_text(page_title)

    # Check if the page was found
    if text == "Page not found":
        return "Page not found"

    # Clean and split the text into words, lowercasing to standardize
    words = re.findall(r'\w+', text.lower())

    # Create a Counter to count occurrences of each word, excluding stop words
    word_counts = Counter(word for word in words if word not in stop_words)

    # Return sorted dictionary of words by decreasing frequency
    return dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

def get_prioritized_titles(target_page, current_page):
    # List to store titles that contain any word found in the target page's word frequency list
    prioritized_titles = []

    # Creates word frequency dictionary of the target page
    word_frequency = get_word_frequency(target_page)

    # Retrieves linked titles from the current page and splits each title into words
    title_words = {title: title.split() for title in get_wikipedia_page_links(current_page)}

    # If target page is in links of current page then the page is found!!!
    if target_page in get_wikipedia_page_links(current_page):
        prioritized_titles.append(target_page)

    # Iterates over each title and its words
    for title, words in title_words.items():
        # Check if any word in the title is in the target page's frequency dictionary
        if any(word in word_frequency for word in words):
            # If at least one word matches, append the title to the prioritized list, if not already added
            if title not in prioritized_titles:
                prioritized_titles.append(title)

    return prioritized_titles

# Example usage
'''
page_title = "University of Florida"

page_text = get_wikipedia_page_text(page_title)
print(page_text)

linked_pages = get_wikipedia_page_links(page_title)
print(linked_pages)

frequencies = get_word_frequency(page_title)
print(frequencies)
'''