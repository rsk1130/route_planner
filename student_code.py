import math

class MinHeap:
    def __init__(self):
        self.heap_list = [None]
        self.count = 0

    def parent_index(self, index):
        return index // 2

    def left_child_index(self, index):
        return index * 2

    def right_child_index(self, index):
        return index * 2 + 1

    def child_present(self, index):
        return self.left_child_index(index) <= self.count

    def retrieve_min(self):
        if self.count == 0:
            print("No items in heap")
            return None

        min = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.count]
        self.count -= 1
        self.heap_list.pop()
        self.heapify_down()
        return min

    def add(self, element):
        self.count += 1
        self.heap_list.append(element)
        self.heapify_up()

    def get_smaller_child_index(self, index):
        if self.right_child_index(index) > self.count:
            return self.left_child_index(index)
        else:
            left_child = self.heap_list[self.left_child_index(index)]
            right_child = self.heap_list[self.right_child_index(index)]
            if left_child < right_child:
                return self.left_child_index(index)
            else:
                return self.right_child_index(index)

    def heapify_up(self):
        index = self.count
        swap_count = 0
        while self.parent_index(index) > 0:
            if self.heap_list[self.parent_index(index)][0] > self.heap_list[index][0]:
                swap_count += 1
                temp = self.heap_list[self.parent_index(index)]
                self.heap_list[self.parent_index(index)] = self.heap_list[index]
                self.heap_list[index] = temp
            index = self.parent_index(index)

    def heapify_down(self):
        index = 1
        swap_count = 1
        while self.child_present(index):
            smaller_child_index = self.get_smaller_child_index(index)
            if self.heap_list[index][0] > self.heap_list[smaller_child_index][0]:
                swap_count += 1
                temp = self.heap_list[smaller_child_index]
                self.heap_list[smaller_child_index] = self.heap_list[index]
                self.heap_list[index] = temp
            index = smaller_child_index


def edge_weight(M, vertex_1, vertex_2):
    
    horizontal = abs(M.intersections[vertex_1][0] - M.intersections[vertex_2][0])
    vertical = abs(M.intersections[vertex_1][1] - M.intersections[vertex_2][1])
    edge_weight = math.sqrt((horizontal * horizontal) + (vertical * vertical))
    
    return edge_weight


def heuristic(M, start, goal):
    
    x_distance = abs(M.intersections[start][0] - M.intersections[goal][0])
    y_distance = abs(M.intersections[start][1] - M.intersections[goal][1])
    heuristic = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
    
    return heuristic


def shortest_path(M, start, goal):
    
    distance_dict = {}

    explore_heap = MinHeap()
    explore_heap.add((0, start))
    
    for vertex in M.intersections:
        distance_dict[vertex] = [float('inf'), [vertex]]
       
    distance_dict[start][0] = 0
    
    while explore_heap.count > 0 and distance_dict[goal][0] == float('inf'):
        current_distance, current_vertex = explore_heap.retrieve_min()
        for neighbor in M.roads[current_vertex]:
            new_distance = current_distance + edge_weight(M, current_vertex, neighbor) + heuristic(M, neighbor, goal)
            new_path = distance_dict[current_vertex][1] + [neighbor]
            
            if new_distance < distance_dict[neighbor][0]:
                distance_dict[neighbor][0] = new_distance
                distance_dict[neighbor][1] = new_path
                explore_heap.add((new_distance, neighbor))
        
    if distance_dict[goal][0] == float('inf'):
        print("No available path from {} to {}. Sorry!\n".format(start, goal))
        
        return distance_dict[goal][1]
    
    else: 
        print("Shortest path from {} to {} is:".format(start, goal))
        for i in range(len(distance_dict[goal][1])-1):
              print(str(distance_dict[goal][1][i]) + " -->")
        print(str(distance_dict[goal][1][-1]))
        print("Total distance of the path is {}.\n".format(distance_dict[goal][0]))
        
        return distance_dict[goal][1]

    