from wikiAPI_functions import *

def main():
    while True:
        start_title = input("Enter the starting Wikipedia page title: ")
        target_title = input("Enter the target Wikipedia page title: ")
        wiki = WikiApi(start_title, target_title)
        print("\n-------------------------")
        print("What would you like to do?")
        print("1: Get target page text")
        print("2: Get starting page links")
        print("3: Get word frequency of target page")
        print("4: Get top 5 most similar links to target")
        print("5: Perform BFS")
        print("6: Perform Greedy search")
        print("0: Exit")
        print("-------------------------")
        choice = input("Enter your choice (0-5): ")

        if choice == "0":
            print("Exiting the program.")
            break

        if choice == "1":
            print("\nFetching page text...")

            print()

        elif choice == "2":
            print("\nFetching page links...")
            linked_pages = wiki.get_wikipedia_page_links()
            print(linked_pages)

        elif choice == "3":
            print("\nCalculating word frequency...")
            frequencies = wiki.get_word_frequency()
            print(frequencies)
            # ex

        elif choice == "4":
            print("\nCalculating word frequency...")
            prioritized_frequencies = wiki.get_most_similar_links_to_target(start_title)
            print(prioritized_frequencies)

        elif choice == "5":
            target_page = input("Enter the target page: ")
            N = int(input("Enter the number titles you want to know the index of: "))
            print("\nCalculating similarity index of links...")
            wikiInstance = WikiApi()
            print(wikiInstance.get_n_first_similarity_index_of_links(start_title, N))
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()