from wikiracer import *

def main():
    obj = Internet()

    bffs = BFSProblem()
    dffs = DFSProblem()
    dijisktra = DijkstrasProblem()
    racer = WikiracerProblem()

    #BFS Algorithm
    print("BFS Search Results: ")
    print(bffs.bfs(source="/wiki/Computer_science", goal="/wiki/Richard_Soley"))
    #DFS Algorithm
    print("DFS Search Results: ")
    print(dffs.dfs(source="/wiki/Computer_science", goal="/wiki/Richard_Soley"))
    #Dijisktra Algorithm
    # worked but takes time, since dijisktra visits all node and cost function is extremely in-efficient
    print("Dijisktra Search Results: ")
    print(dijisktra.dijkstras(source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia", costFn = lambda y, x: len(x) * 1000 + x.count("a") * 100  + x.count("u") + x.count("h") * 5 - x.count("F")))
    # With better Hueristic function / costFn + Dijisktra/Uniform Cost Search (kind of A*)
    print("WikiRacer Search Results: ")
    print(racer.wikiracer(source="/wiki/Computer_science", goal="/wiki/Richard_Soley"))
    #Karma
    print("Karma Search Results: ")
    find = FindInPageProblem()
    print(find.find_in_page())
main()