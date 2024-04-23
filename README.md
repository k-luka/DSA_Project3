# Wikibot

Wikibot is a Wikipedia speedrun bot that finds a path from a given starting page to a given target page using text body links.
To find the target page, two algorithms can be used: BFS and Greedy Search. The links can be given a relation score based on the following criteria: the number of times the words of the linked title appear on the target page multiplied by the log of how uncommon that word is in the English language.

BFS (kinda greedy): Since the average page links to 200 others, pure BFS would be unfeasible. Because of this our BFS only looks at N best links from each page. Where N is the Breadth space which can be set by the user. Our greedy BFS can find the shorter path between pages at the expense of being much slower.

Greedy Search: Greedy search is similar however instead of going equally in every direction, it makes a max heap of the pages with N best relation scores and picks the highest-rated page at each step. Therefore Greedy Search visits far fewer pages and is much faster than BFS.

## Usage

Run wikibot.py located in the wikibot directory. Enter the desired starting and target page, customize the options, and click the green button. A graph showing the visited pages will appear. To re-run click the yellow button. To close the program, click the red exit button. A sample run is shown in the image below.

<img src="https://github.com/k-luka/DSA_Project3/assets/106494914/ae26677e-d2ac-4e4f-a4a8-cece6f0acee9" width="600" alt="alt text">

The path to the target is highlighted in yellow and the unused visited nodes are in grey.


## Dependancies

To run, install the following libraries:
- Wikipedia-API
- regex
- PyGLM
- wordfreq
- moderngl
- numpy
- pygame
- math
- collections
- heapq
- wordfreq


## Maintainers

- Kirill Luka - [k-luka](https://github.com/k-luka)
- Nathan Bailey - [Kudeau](https://github.com/Kudeau)
- Ramsey Makan - [rambomario15](https://github.com/rambomario15)

