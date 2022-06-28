from doctest import BLANKLINE_MARKER
from email import parser
from queue import PriorityQueue
from internet import Internet
from typing import List
from collections import deque
import random
import re
class Parser:

    @staticmethod
    def get_links_in_page(html: str) -> List[str]:
        """
        In this method, we should parse a page's HTML and return a list of links in the page.
        Be sure not to return any link with a DISALLOWED character.
        All links should be of the form "/wiki/<page name>", as to not follow external links
        """
        links = []
        disallowed = Internet.DISALLOWED
        # links = re.findall("(?i)<a([^>]+)>",html)
        links_ = re.findall("<a\s+(?:[^>]*?\s+)?href=\"([^\"]+wiki/?[^\"]+)",html)

        for l in links_:
            if any(i in l[6:] for i in Internet.DISALLOWED) or l in links:
                pass
            else:
                if l[:6] == '/wiki/':
                    links.append(l)

        # YOUR CODE HERE
        # You can look into using regex, or just use Python's find methods to find the <a> tags or any other identifiable features
        # A good starting place is to print out `html` and look for patterns before/after the links that you can string.find().
        # Make sure your list doesn't have duplicates. Return the list in the same order as they appear in the HTML.
        # This function will be stress tested so make it efficient!

        return links

# In these methods, we are given a source page and a goal page, and we should return
#  the shortest path between the two pages. Be careful! Wikipedia is very large.

# These are all very similar algorithms, so it is advisable to make a global helper function that does all of the work, and have
#  each of these call the helper with a different data type (stack, queue, priority queue, etc.)

class BFSProblem:
    def __init__(self):
        self.internet = Internet()
    # Example in/outputs:
    #  bfs(source = "/wiki/Computer_science", goal = "/wiki/Computer_science") == ["/wiki/Computer_science", "/wiki/Computer_science"]
    #  bfs(source = "/wiki/Computer_science", goal = "/wiki/Computation") == ["/wiki/Computer_science", "/wiki/Computation"]
    # Find more in the test case file.

    # Do not try to make fancy optimizations here. The autograder depends on you following standard BFS and will check all of the pages you download.
    # Links should be inserted into the queue as they are located in the page, and should be obtained using Parser's get_links_in_page.
    # Be very careful not to add things to the "visited" set of pages too early. You must wait for them to come out of the queue first. See if you can figure out why.
    #  This applies for bfs, dfs, and dijkstra's.
    # Download a page with self.internet.get_page().
    def bfs(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):
        path = {}
        path[source] = [source]
        Q = deque([source])
        while len(Q) != 0:
            # look at next page in queue of pages to visit, get wikilinks on that page
            page = Q.popleft()
            links = Parser.get_links_in_page(self.internet.get_page(page))
    
            # look at each link on the page
            for link in links:
                # if link is our destination, we're done!
                if link == goal:
                    print("No of Downloads: "+str(len(self.internet.requests)))
                    return path[page] + [link]

                # if not, check if we already have a record of the shortest path from the start page to this link- if we don't, we need to record the path and add the link to our queue of pages to explore
                if (link not in path) and (link != page):
                    path[link] = path[page] + [link]
                    Q.append(link)
        return None # if no path exists, return None

class DFSProblem:
    def __init__(self):
        self.internet = Internet()
    # Links should be inserted into a stack as they are located in the page. Do not add things to the visited list until they are taken out of the stack.
    def dfs(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):
        path = {}
        path[source] = [source]
        Q = deque([source])
        while len(Q) != 0:
            # look at next page in queue of pages to visit, get wikilinks on that page
            page = Q.popleft()
            links = Parser.get_links_in_page(self.internet.get_page(page))

            # look at each link on the page
            #in DFS, always last links are iterated first
            for link in links[::-1]:
                # if link is our destination, we're done!
                if link == goal:
                    print("No of Downloads: "+str(len(self.internet.requests)))
                    return path[page] + [link]


                # if not, check if we already have a record of the shortest path from the start page to this link- if we don't, we need to record the path and add the link to our queue of pages to explore
                if (link not in path) and (link != page):
                    path[link] = path[page] + [link]
                    Q.append(link)
        return path # if no path exists, return None

class DijkstrasProblem:
    def __init__(self):
        self.internet = Internet()
    # Links should be inserted into the heap as they are located in the page.
    # By default, the cost of going to a link is the length of a particular destination link's name. For instance,
    #  if we consider /wiki/a -> /wiki/ab, then the default cost function will have a value of 8.
    # This cost function is overridable and your implementation will be tested on different cost functions. Use costFn(node1, node2)
    #  to get the cost of a particular edge.
    # You should return the path from source to goal that minimizes the total cost. Assume cost > 0 for all edges.
    def dijkstras(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia", costFn = lambda x, y: len(y)):
        path = {}
        path[source] = [source]
        visited = set()
        cost ={source:0}
        parent = {source:None}
        pQ = PriorityQueue()

        pQ.put((0,source))

        while not pQ.empty():
            while not pQ.empty():
                # get lowest cost vertex
                #initially, source node
                _, vertex = pQ.get()
                if vertex not in visited:
                    break
            else: # if todo ran out
                break # quit main loop
            #found least cost vertex
            links = Parser.get_links_in_page(self.internet.get_page(vertex))
            #mark node as visited
            visited.add(vertex)
            # visiting vertex is destination
            if vertex == goal:
                print("No of Downloads: "+str(len(self.internet.requests)))
                return path[vertex]
            #visit each neighbour of vertex and update their weights from source
            for link in links:
                if link not in visited:
                    old_cost = cost.get(link,float('inf'))
                    new_cost = cost[vertex] + costFn(vertex,link)
                    if new_cost < old_cost:
                        #put updated weights into priorityQueue
                        pQ.put((new_cost,link))
                        cost[link] = new_cost
                        if (link != vertex) and (link not in path):
                            path[link] = path[vertex]+[link] 

class WikiracerProblem:
    goal_links = []
    def __init__(self):
        self.internet = Internet()

    # Time for you to have fun! Using what you know, try to efficiently find the shortest path between two wikipedia pages.
    # Your only goal here is to minimize the total amount of pages downloaded from the Internet, as that is the dominating time-consuming action.

    # Your answer doesn't have to be perfect by any means, but we want to see some creative ideas.
    # One possible starting place is to get the links in `goal`, and then search for any of those from the source page, hoping that those pages lead back to goal.

    # Note: a BFS implementation with no optimizations will not get credit, and it will suck.
    # You may find Internet.get_random() useful, or you may not.

    def wikiracer(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):
        path = [source]
        self.goal_links = Parser.get_links_in_page(self.internet.get_page(goal))
        """
        Solution 2: Modifiying Dijisktra Implementation
        Steps:
            1) Dijisktra can be made efficient by giving effective cost function
                How to prioritize?
                Answer:
                    --> In costFn, we will calculate the level of similarity between two nodes's links.
                    intersection of "current visiting page links" and "goal page links"
            Pages having similar links have same kind of nature. 
            Like if we are at America's page then it can lead us obama's page and both pages will have similar links
            
        """
        return self.modifiedDijkstras(source,goal)


    # costFn function to priotize the substrings of goal link
    #kind of fitness function
    #matches no of similar links
    def costFn(self,link):
        obj = Internet()
        page_links = Parser.get_links_in_page(obj.get_page(link))
        common_links = list(set(page_links) & set(self.goal_links))
        return len(common_links) * -1



    def modifiedDijkstras(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):
        path = {}
        path[source] = [source]
        visited = set()
        cost ={source:0}
        parent = {source:None}
        pQ = PriorityQueue()

        pQ.put((0,source))

        while not pQ.empty():
            while not pQ.empty():
                # get lowest cost vertex
                #initially, source node
                _, vertex = pQ.get()
                if vertex not in visited:
                    break
            else: # if todo ran out
                break # quit main loop
            #found least cost vertex
            links = Parser.get_links_in_page(self.internet.get_page(vertex))
            #mark node as visited
            visited.add(vertex)
            # visiting vertex is destination
            if vertex == goal:
                print("No of Downloads: "+str(len(self.internet.requests)))
                return path[vertex]
            #visit each neighbour of vertex and update their weights from source
            for link in links:
                if link not in visited:
                    old_cost = cost.get(link,float('inf'))
                    #identify matching links of curr_link and goal
                    #matching links will be the weight of curr_link
                    new_cost = cost[vertex] + self.costFn(link)
                    if new_cost < old_cost:
                        #put updated weights into priorityQueue
                        pQ.put((new_cost,link))
                        cost[link] = new_cost
                        if (link != vertex) and (link not in path):
                            path[link] = path[vertex]+[link] 
        return None
    



# KARMA
class FindInPageProblem:
    word_list = []
    def __init__(self):
        self.internet = Internet()
    # This Karma problem is a little different. In this, we give you a source page, and then ask you to make up some heuristics that will allow you to efficiently
    #  find a page containing all of the words in `query`. Again, optimize for the fewest number of internet downloads, not for the shortest path.

    def find_in_page(self, source = "/wiki/Calvin_Li", query = ["ham", "cheese"]):

        self.word_list = query
        

        # find a path to a page that contains ALL of the words in query in any place within the page
        # path[-1] should be the page that fulfills the query.
        # YOUR CODE HERE


        return self.modifiedDijkstras(source,query)

    # to extract text from the dirty html file
    def clean_html(self,html):
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        return cleaned.strip()
    # costFn function to priotize the pages that have most no of matched words
    #matches no of similar words
    def costFn(self,link):
        obj = Internet()
        html = self.clean_html(obj.get_page(link))
        matched = 0
        for word in self.word_list:
            spaced_word = "( "+word+")|"+"( "+word+" )|"+"("+word+" )"
            x = re.search(spaced_word, str(html))
            if x:
                matched+=1
        return matched * -1




    def modifiedDijkstras(self, source,query):
        path = {}
        path[source] = [source]
        visited = set()
        cost ={source:0}
        parent = {source:None}
        pQ = PriorityQueue()
        pQ.put((0,source))

        while not pQ.empty():
            while not pQ.empty():
                # get lowest cost vertex
                #initially, source node
                _, vertex = pQ.get()
                if vertex not in visited:
                    break
            else: # if todo ran out
                break # quit main loop
            #found least cost vertex
            links = Parser.get_links_in_page(self.internet.get_page(vertex))
            #mark node as visited
            visited.add(vertex)
            # visiting vertex is destination
            if (self.costFn(vertex)*-1) == len(query):
                print("No of Downloads: "+str(len(self.internet.requests)))
                return path[vertex]
            #visit each neighbour of vertex and update their weights from source
            for link in links:
                if link not in visited:
                    old_cost = cost.get(link,float('inf'))
                    #identify matching links of curr_link and goal
                    #matching links will be the weight of curr_link
                    new_cost = cost[vertex] + self.costFn(link)
                    if new_cost < old_cost:
                        #put updated weights into priorityQueue
                        pQ.put((new_cost,link))
                        cost[link] = new_cost
                        if (link != vertex) and (link not in path):
                            path[link] = path[vertex]+[link] 
        return None
