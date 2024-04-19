from wikiAPI_functions import *

def main():
    while True:
        print("\nWhat would you like to do?")
        print("1: Get Wikipedia page text")
        print("2: Get Wikipedia page links")
        print("3: Get word frequency on a page")
        print("0: Exit")
        choice = input("Enter your choice (0-3): ")

        if choice == "0":
            print("Exiting the program.")
            break

        page_title = input("Enter the Wikipedia page title: ")

        if choice == "1":
            print("\nFetching page text...")
            page_text = get_wikipedia_page_text(page_title)
            print(page_text)

        elif choice == "2":
            print("\nFetching page links...")
            linked_pages = get_wikipedia_page_links(page_title)
            print(linked_pages)

        elif choice == "3":
            print("\nCalculating word frequency...")
            frequencies = get_word_frequency(page_title)
            print(frequencies)

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()