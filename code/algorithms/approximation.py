import time

class ApproximationAlgorithm:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    def ratio_greedy(self, capacity, value_weight, record):
        """Calculate the ratio greedy algorithm"""
        """take value / weight ratio, sort them, and always takes the large one first until meeting the limit"""
        vw_ratios = []
        for i, item in enumerate(value_weight): # get the value and the weight respectively
            vw_ratios.append([i, item[0] / item[1]])
        vw_ratios.sort(key=lambda x: x[1], reverse=True) # based on the value_weight ratio, sort from large to small
        total_value = 0
        total_weight = 0
        
        for i, ratio in vw_ratios: 
            if total_weight + value_weight[i][1] <= capacity: # can still add
                total_weight += value_weight[i][1]
                total_value += value_weight[i][0]
                record[i] = 1 
            
        return total_value, total_weight, record

    def value_greedy(self, capacity, value_weight, record):
        """Calculate the value greedy algorithm"""
        """take value only, sort them, and always takes the large one first until meeting the limit"""
        vw = [] # get the value and the weight respectively
        for i, item in enumerate(value_weight):
            vw.append([i, item[0], item[1]])
        vw.sort(key=lambda x: x[1], reverse=True) # based on the value, sort from large to small
        total_value = 0
        total_weight = 0
        
        for i, value, weight in vw:
            if total_weight + weight <= capacity: # can still add
                total_weight += weight
                total_value += value
                record[i] = 1 
            
        return total_value, total_weight, record

    def solve(self, cut_off_time):
        start_time = time.time()
        trace = []
        value_weight = []
        for l in self.items: # get the input 
            value_weight.append([l['value'], l['weight']])
        number = len(self.items)

        record = [0] * number 
        total_value_1, total_weight_1, record_ratio_1 = self.ratio_greedy(self.capacity, value_weight, record) # first method : value weight density (ratio greedy)
        total_value_2, total_weight_2, record_ratio_2 = self.value_greedy(self.capacity, value_weight, record) # second method : value (value greedy)
        if total_value_1 > total_value_2: # 2 - approximation method : take the sol. that has higher value
            res_record = record_ratio_1
            res_total_value = total_value_1
        else:
            res_record = record_ratio_2
            res_total_value = total_value_2

        elapsed_time = time.time() - start_time
        trace.append((elapsed_time, res_total_value))    
        solution = {'selected_items': res_record, 'quality': res_total_value}
        return solution, trace