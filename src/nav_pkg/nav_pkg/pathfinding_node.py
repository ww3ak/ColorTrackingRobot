# Dijkstra's Algorithm for robot to use for pathfinding algorithm
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
import heapq
import sys

class PathfindingNode(Node):
    def __init__(self):
        super().__init__('pathfinding_node')

        self.graph = {}
        self.num_nodes = 0

        self.node_positions = {} #stores node pos
        self.current_node = 0 # curr robot position

        self.create_subscription(PoseStamped, '/goal_pose', self.pose_callback, 10) # sub. to goal
        self.path_pub = self.create_publisher(Path, '/planned_path', 10) # pub. planned path
        self.get_logger().info("Pathfinding node started")

    # How do we get the graph/map from the robot's world?

    def dijkstra(self, adj, start):
        V = len(adj)
        dist = [sys.maxsize] * V
        prev = {}
        visited = set()
        dist[start] = 0

        priority_queue = [(0, start)]
        while priority_queue:
            curr_dist, curr_node = heapq.heappop(priority_queue)

            if curr_node in visited:
                continue

            visited.add(curr_node)

            if curr_node not in self.graph: # Check all neighbors
                continue

            for neighbor, weight in self.graph[curr_node]:
                if neighbor in visited:
                    continue

                new_dist = curr_dist + weight

                if new_dist < dist[neighbor]: # short path found
                    dist[neighbor] = new_dist
                    prev[neighbor] = curr_node
                    heapq.heappush(priority_queue, (new_dist, neighbor))
        return dist, prev
    
    def get_shortest_path(self, start, end, prev):

        if end not in prev and end != start:
            return None
        
        path = []
        curr = end

        while curr != start:
            path.append(curr)
            curr = prev.get(curr)
            if curr not in prev:
                return None
            
        path.append(start)
        path.reverse()

        return path
