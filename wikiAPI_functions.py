import wikipediaapi
import re
from collections import Counter

class wikiApi:
    def __init__(self):
        # Initialize the Wikipedia API
        self.wiki = wikipediaapi.Wikipedia('DSA_Project3', 'en')
        # List of common stop words to exclude
        self.stop_words = {"the", "and", "a", "an", "in", "on", "at", "for", "with", "about", "as", "to", "of", "it", "by",
                      "from", "that", "this", "but", "up", "down", "out", "or", "when", "which", "who", "what", "is", "are",
                      "was", "were", "be", "being", "been", "have", "has", "had", "do", "does", "did", "will", "would",
                      "shall", "should", "can", "could", "may", "might", "must", "ought", "also", "s", "its", "such",
                      "than", "many", "much"}

    def get_wikipedia_page_links(self, page_title):
        # Fetch the page for the given title
        page = self.wiki.page(page_title)

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


    def get_wikipedia_page_text(self, page_title):
        # Fetch the page for the given title
        page = self.wiki.page(page_title)

        # Check if the page exists
        if page.exists():
            # Return the text of the page
            return page.text
        else:
            return "Page not found"


    def get_word_frequency(self, page_title):
        # Get the text of the page using the previously defined function
        text = self.get_wikipedia_page_text(page_title)

        # Check if the page was found
        if text == "Page not found":
            return "Page not found"

        # Clean and split the text into words, lowercasing to standardize
        words = re.findall(r'\w+', text.lower())

        # Create a Counter to count occurrences of each word, excluding stop words
        word_counts = Counter(word for word in words if word not in self.stop_words)

        # Return sorted dictionary of words by decreasing frequency
        return dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

    def split(self, title):
        return [word for word in title.split() if word not in self.stop_words]

    def get_n_first_similarity_index_of_links(self, current_page, target_page, n):
        # List to store titles that contain any word found in the target page's word frequency list
        links_and_indices = {}

        # Creates word frequency dictionary of the target page
        word_frequency = self.get_word_frequency(target_page)
        # Creates list of linked pages in current page
        pageLinks = self.get_wikipedia_page_links(current_page)

        # Retrieves linked titles from the current page and splits each title into words
        title_words = {title: self.split(title) for title in pageLinks}

        # If target page is in links of current page then the page is found!!!
        #if target_page in pageLinks:
        #    links_and_indices.append(target_page)

        # Iterates over each title and its words
        for title, words in title_words.items():
            # Check if any word in the title is in the target page's frequency dictionary
            totalFreq = 0
            for word in words:
                if word in word_frequency.keys():
                    #print(word)
                    totalFreq += word_frequency[word]
            totalFreq /= len(words)
            links_and_indices[title] = totalFreq
        links_and_indices = dict(sorted(links_and_indices.items(), key=lambda item: item[1], reverse=True))
        return {x: links_and_indices[x] for x in list(links_and_indices)[:n]}

    # New functions
    def get_categories(self, page):
        # Fetch the page for the given title
        pageEx = self.wiki.page(page)
        categories = pageEx.categories
        '''
        for title in sorted(categories.keys()):
            print(title)
        print(len(categories))
        '''
        return set(categories.keys())

    def get_summary(self, page):
        pageObj = self.wiki.page(page)
        return pageObj.summary

    '''
    def get_proportion_of_common_categories(self, sourcePage, targetPage):
        sourceCategories = self.get_categories(sourcePage)
        targetCategories = self.get_categories(targetPage)
        if len(targetCategories) == 0: return 0
        return len(sourceCategories & targetCategories) / len(targetCategories)
    
    def get_links_sorted_by_common_categories_with_target(self, page, target):
        links = self.get_wikipedia_page_links(page)
        targetCategories = self.get_categories(target)
        linksAndProportions = {}
        for link in links:
            sourceCategories = self.get_categories(link)
            proportion = 0
            if (len(targetCategories) > 0):
                for category in targetCategories:
                    if category in sourceCategories: proportion += 1
                proportion /= len(targetCategories)
            linksAndProportions[link] = proportion
            # print(str(link) + " : " + str(len(sourceCategories)))
        return dict(sorted(linksAndProportions.items(), key=lambda item: item[1], reverse=True))
    '''


wikiInstance = wikiApi()
#print(wikiInstance.get_proportion_of_common_categories("University of Georgia", "Bulldog"))
print(wikiInstance.get_n_first_similarity_index_of_links("School", "Statistics", 10))
'''
# Example usage

page_title = "University of Florida"

page_text = get_wikipedia_page_text(page_title)
print(page_text)

linked_pages = get_wikipedia_page_links(page_title)
print(linked_pages)

frequencies = get_word_frequency(page_title)
print(frequencies)
'''