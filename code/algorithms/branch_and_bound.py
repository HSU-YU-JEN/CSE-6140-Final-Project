from collections import deque
import time

class BranchAndBound:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    class Node:
        def __init__(self, level, value, weight, items):
            self.level = level
            self.value = value
            self.weight = weight
            self.items = items[:]
        
        # Compute bound using greedy approach for fractional Knapsack
        def compute_bound(self, items_des, cap, n):
            if self.weight >= cap:
                return 0
            result = self.value
            totweight = self.weight
            j = self.level + 1
            while j < n and totweight + items_des[j][1] <= cap:
                totweight += items_des[j][1]
                result += items_des[j][0]
                j += 1
            if j < n:
                result += int((cap - totweight) * (items_des[j][0] / items_des[j][1]))
            return result

    def branch_and_bound(self):
        n = len(self.items)
        cap = self.capacity
        values = [item['value'] for item in self.items]
        weights = [item['weight'] for item in self.items]
        items = list(zip(values, weights))
        items_des = sorted(items, key=lambda x: x[0]/x[1], reverse=True)
        queue = deque([self.Node(-1, 0, 0, [0]*n)])
        max_value = 146888
        opt_items = []
        trace = []
        start_time = time.time()

        while queue:
            node_now = queue.popleft()

            if node_now.level == n-1:
                continue

            node_next_in = self.Node(node_now.level + 1, node_now.value + items_des[node_now.level+1][0],
                                     node_now.weight + items_des[node_now.level+1][1], node_now.items[:])
            node_next_in.items[node_now.level + 1] = 1

            if node_next_in.weight <= cap and node_next_in.value > max_value:
                max_value = node_next_in.value
                opt_items = node_next_in.items[:]
                trace.append((time.time() - start_time, max_value))

            node_next_in.bound = node_next_in.compute_bound(items_des, cap, n)
            if node_next_in.bound > max_value:
                queue.append(node_next_in)

            node_next_out = self.Node(node_now.level + 1, node_now.value, node_now.weight, node_now.items[:])
            node_next_out.bound = node_next_out.compute_bound(items_des, cap, n)
            if node_next_out.bound > max_value:
                queue.append(node_next_out)

        best_items = [0]*n
        for i in range(n):
            if opt_items[i] == 1:
                best_items[i] = 1

        return max_value, best_items, trace

    def solve(self, cut_off_time):
        opt_totvalue, sel_items, trace = self.branch_and_bound()
        solution = {'selected_items': sel_items, 'quality': opt_totvalue}
        return solution, trace
