import wikipediaapi
import re
from collections import Counter, deque
import heapq
import wordfreq
import math

class WikiApi:
    '''
    class WikiPage:
        def __init__(self):
            self.text = ""
            self.links = []
            self.parent = ""
            self.similarity_index = 0
    '''
    def __init__(self, word_uniqueness = True, neighbors_checked = 5):
        # Initialize the Wikipedia API
        self.wiki = wikipediaapi.Wikipedia('DSA_Project3', 'en')
        # List of common stop words to exclude
        self.stop_words = {"the", "and", "a", "an", "in", "on", "at", "for", "with", "about", "as", "to", "of", "it", "by",
                      "from", "that", "this", "but", "up", "down", "out", "or", "when", "which", "who", "what", "is", "are",
                      "was", "were", "be", "being", "been", "have", "has", "had", "do", "does", "did", "will", "would",
                      "shall", "should", "can", "could", "may", "might", "must", "ought", "also", "s", "its", "such",
                      "than", "many", "much"}
        self.stop_words = [word.upper() for word in self.stop_words]
        self.adjust_for_word_uniqueness = word_uniqueness
        self.neighbors_to_check = neighbors_checked

    def reverse_adjust_for_word_uniqueness(self):
        self.adjust_for_word_uniqueness = not self.adjust_for_word_uniqueness

    def set_neighbors_to_check(self, n):
        self.neighbors_to_check = int(n)

    def get_adjust_for_word_uniqueness(self):
        return self.adjust_for_word_uniqueness

    def get_neighbors_to_check(self):
        return self.neighbors_to_check

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
        words = re.findall(r'\w+', text.upper())

        # Create a Counter to count occurrences of each word, excluding stop words
        word_counts = Counter(word for word in words if word not in self.stop_words)

        # Return sorted dictionary of words by decreasing frequency
        return dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

    def split(self, title):
        return [word for word in title.split() if word not in self.stop_words]

    def get_word_uniqueness(self, word):
        return -1 * math.log10(wordfreq.word_frequency(word, "en")) - 1

    def get_n_first_similarity_index_of_links(self, current_page, target_page, n):
        # List to store titles that contain any word found in the target page's word frequency list
        links_and_indices = {}

        # Creates word frequency dictionary of the target page
        word_frequency = self.get_word_frequency(target_page)
        #if target_page == "Ukraine": print(word_frequency)
        # Creates list of linked pages in current page
        pageLinks = self.get_wikipedia_page_links(current_page)

        # Retrieves linked titles from the current page and splits each title into words
        title_words = {title: self.split(title.upper()) for title in pageLinks}

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
                    # Add word times its uniqueness weight
                    totalFreq += word_frequency[word] * self.get_word_uniqueness(word)
            totalFreq /= len(words)
            links_and_indices[title] = totalFreq
        links_and_indices = dict(sorted(links_and_indices.items(), key=lambda item: item[1], reverse=True))
        return {x: links_and_indices[x] for x in list(links_and_indices)[:n]}

    def bfs_search(self, starting_page, target_page, n):
        queue = deque([starting_page])  # Queue to manage the frontier pages
        visited = set()  # Set to keep track of visited pages to avoid cycles
        levels = 0

        while queue:
            current_page = queue.popleft()

            # Skip revisiting pages
            if current_page in visited:
                continue
            visited.add(current_page)

            completedLevelsSize = sum([n**i for i in range(0, levels+1)])
            if len(visited) - 1 == completedLevelsSize:
                levels += 1

            # Get the top 'n' similar linked pages from the current page
            try:
                related_links = self.get_n_first_similarity_index_of_links(current_page, target_page, n)
                # Check if the current page is the target page
                print(str(current_page) + " links to " + str(related_links))
                if target_page.upper() in [word.upper() for word in related_links.keys()]:
                    return f"Target page '{target_page}' found starting from '{starting_page}'. Distance = {levels+1}"


            except Exception as e:
                print(f"Failed to retrieve or process links for {current_page}: {e}")
                continue

            # Enqueue unvisited linked pages
            for page, similarity_index in related_links.items():
                if page not in visited:
                    queue.append(page)

        return "Target page not found within the connected pages."

    def greedy_search(self, starting_page, target_page, n):
        # Max heap representing our nodes to visit. Similarity indices will be inserted as
        # negative values so the min heap returns the values with actually the most similarity
        priorityQueue = []
        heapq.heappush(priorityQueue, (0, starting_page))
        visited = set()  # Set to keep track of visited pages to avoid cycles
        levels = 0

        while priorityQueue:
            current_page = heapq.heappop(priorityQueue)[1]

            # Skip revisiting pages
            if current_page in visited:
                continue
            visited.add(current_page)

            #completedLevelsSize = sum([n**i for i in range(0, levels+1)])
            #if len(visited) - 1 == completedLevelsSize:
            #    levels += 1

            # Get the top 'n' similar linked pages from the current page
            try:
                related_links = self.get_n_first_similarity_index_of_links(current_page, target_page, n)
                # Check if the current page is the target page
                print(str(current_page) + " links to " + str(related_links))
                if target_page.upper() in [word.upper() for word in related_links.keys()]:
                    return f"Target page '{target_page}' found starting from '{starting_page}'. Distance = {levels+1}"

            except Exception as e:
                print(f"Failed to retrieve or process links for {current_page}: {e}")
                continue

            # Enqueue unvisited linked pages
            for page, similarity_index in related_links.items():
                if page not in visited:
                    heapq.heappush(priorityQueue, (-1 * similarity_index, page))

        return "Target page not found within the connected pages."

wikiInstance = WikiApi()
#print(wikiInstance.get_proportion_of_common_categories("University of Georgia", "Bulldog"))
#print(wikiInstance.bfs_search("Mars", "Moon", 4))
print(wikiInstance.greedy_search("International Olympic Committee", "Android (operating system)", 5))

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