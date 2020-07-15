from util import Stack, Queue

def earliest_ancestor(ancestors, starting_node):
    # create a Queue
    q = Queue()
    # add starting node to the path
    path = [starting_node]
    # enqueue the path AKA starting node
    q.enqueue(path)

    # While there is something is our Queue
    while q.size() > 0:
        # create a currentPath variable set to be our dequeued Queue
        currentPath = q.dequeue()
        # create a newPath list
        newPath = []
        # create a "changed" variable 
        changed = False

        # loop over the node in current path
        for node in currentPath:
            # loop through its ancestors
            for ancestor in ancestors:
                # if ancestor[1] == node:
                if ancestor[1] == node:
                    # append that ancestor to our newPath
                    newPath.append(ancestor[0])
                    # set it to be changed
                    changed = True
                    # enqueue that newPath we now have
                    q.enqueue(newPath)

        # if changed is False, so we didn't change it
        if changed is False:
            # if currentPath[0] == starting_node aka has no parents
            if currentPath[0] == starting_node:
                # return -1
                return -1
            else:
                return currentPath[0]