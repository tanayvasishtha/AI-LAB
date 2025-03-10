# A* Scheduler for Task Scheduling Problem

import heapq
from collections import defaultdict

class Task:
    def __init__(self, task_id, duration, predecessors):
        self.id = task_id
        self.duration = duration
        self.predecessors = predecessors
        self.successors = []
        self.est = 0  # Earliest start time
        self.lft = 0  # Latest finish time

class TaskGraph:
    def __init__(self):
        self.tasks = {}
        self.entry_node = None
    
    def add_task(self, task):
        self.tasks[task.id] = task
        if not task.predecessors:
            self.entry_node = task.id
    
    def build_successors(self):
        for task in self.tasks.values():
            for pred_id in task.predecessors:
                pred_task = self.tasks[pred_id]
                pred_task.successors.append(task.id)
    
    def compute_critical_path(self):
        # Forward pass for EST calculation
        topo_order = self._topological_sort()
        for task_id in topo_order:
            task = self.tasks[task_id]
            task.est = max([self.tasks[pred].est + self.tasks[pred].duration 
                          for pred in task.predecessors], default=0)
        
        # Backward pass for LFT calculation
        reverse_topo = list(reversed(topo_order))
        exit_node = next(t for t in reverse_topo if not self.tasks[t].successors)
        
        for task_id in reverse_topo:
            task = self.tasks[task_id]
            if not task.successors:
                task.lft = task.est + task.duration
            else:
                task.lft = min([self.tasks[succ].lft - self.tasks[succ].duration 
                              for succ in task.successors])
        
        # Identify critical path
        critical_path = []
        current = self.entry_node
        while current:
            critical_path.append(current)
            current = next((succ for succ in self.tasks[current].successors 
                           if self.tasks[succ].est == self.tasks[current].est + self.tasks[current].duration), None)
        return critical_path
    
    def _topological_sort(self):
        visited = set()
        order = []
        
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for succ in self.tasks[node].successors:
                dfs(succ)
            order.append(node)
        
        dfs(self.entry_node)
        return list(reversed(order))

class State:
    def __init__(self, scheduled, makespan, proc_times, parent=None):
        self.scheduled = scheduled  # {task_id: (start, end, proc)}
        self.makespan = makespan
        self.proc_times = proc_times  # [next_available_time per proc]
        self.parent = parent
        self.g = makespan
        self.h = 0
        self.f = self.g + self.h
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __hash__(self):
        return hash(frozenset(self.scheduled.items()))
    
    def __eq__(self, other):
        return self.scheduled == other.scheduled

class AStarScheduler:
    def __init__(self, task_graph, num_procs):
        self.graph = task_graph
        self.num_procs = num_procs
        self.critical_path = self.graph.compute_critical_path()
    
    def heuristic(self, state):
        remaining = [t for t in self.graph.tasks if t not in state.scheduled]
        return sum(self.graph.tasks[t].duration for t in self.critical_path if t in remaining)
    
    def get_successors(self, state):
        successors = []
        eligible = self._get_eligible_tasks(state)
        
        for task_id in eligible:
            task = self.graph.tasks[task_id]
            est = max([state.scheduled[p][1] for p in task.predecessors], default=0)
            
            for proc in range(self.num_procs):
                proc_available = state.proc_times[proc]
                start = max(est, proc_available)
                end = start + task.duration
                
                new_scheduled = state.scheduled.copy()
                new_scheduled[task_id] = (start, end, proc)
                new_proc_times = state.proc_times.copy()
                new_proc_times[proc] = end
                new_makespan = max(state.makespan, end)
                
                new_state = State(new_scheduled, new_makespan, new_proc_times, state)
                new_state.h = self.heuristic(new_state)
                new_state.f = new_state.g + new_state.h
                successors.append(new_state)
        
        return successors
    
    def _get_eligible_tasks(self, state):
        return [t for t in self.graph.tasks 
                if t not in state.scheduled 
                and all(p in state.scheduled for p in self.graph.tasks[t].predecessors)]
    
    def schedule(self):
        initial_proc_times = [0] * self.num_procs
        initial_state = State({}, 0, initial_proc_times)
        initial_state.h = self.heuristic(initial_state)
        initial_state.f = initial_state.g + initial_state.h
        
        heap = []
        heapq.heappush(heap, (initial_state.f, initial_state))
        visited = set()
        
        while heap:
            current_f, current = heapq.heappop(heap)
            
            if len(current.scheduled) == len(self.graph.tasks):
                return self._build_schedule(current)
            
            if hash(current) in visited:
                continue
            visited.add(hash(current))
            
            for successor in self.get_successors(current):
                heapq.heappush(heap, (successor.f, successor))
        
        return None
    
    def _build_schedule(self, state):
        schedule = {}
        while state:
            for task, (start, end, proc) in state.scheduled.items():
                if task not in schedule:
                    schedule[task] = (start, end, proc)
            state = state.parent
        
        proc_schedules = defaultdict(list)
        for task in sorted(schedule, key=lambda x: schedule[x][0]):
            start, end, proc = schedule[task]
            proc_schedules[proc].append((task, start, end))
        
        return dict(proc_schedules)

# Example execution
if __name__ == "__main__":
    # Create task graph from sample problem
    tg = TaskGraph()
    tasks = [
        Task('t1', 5, []),
        Task('t2', 3, ['t1']),
        Task('t3', 4, ['t1']),
        Task('t4', 2, ['t2']),
        Task('t5', 6, ['t3']),
        Task('t6', 3, ['t4', 't5']),
        Task('t7', 4, ['t5']),
        Task('t8', 5, ['t6']),
        Task('t9', 2, ['t7']),
        Task('t10', 3, ['t8', 't9'])
    ]
    for t in tasks:
        tg.add_task(t)
    tg.build_successors()
    
    # Execute scheduler
    scheduler = AStarScheduler(tg, num_procs=2)
    schedule = scheduler.schedule()
    
    # Output results
    if schedule:
        # Corrected makespan calculation
        all_ends = [end for proc_tasks in schedule.values() 
                   for _, _, end in proc_tasks]  # Fixed unpacking
        makespan = max(all_ends)
        
        print(f"Optimal Schedule (Makespan: {makespan})")
        for proc in sorted(schedule):
            print(f"\nProcessor {proc + 1}:")
            for task, start, end in sorted(schedule[proc], key=lambda x: x[1]):
                print(f"  Task {task}: {start:02d}-{end:02d} (Duration: {end - start})")
    else:
        print("No valid schedule found")
