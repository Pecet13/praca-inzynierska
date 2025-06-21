from collections import deque
from .models import Comparison

def check_cycle(user, category, src_product, dest_product):
    queryset = Comparison.objects.filter(user=user, category=category)
    adj = {}
    for comparison in queryset:
        if comparison.result == "More":
            adj.setdefault(comparison.product1, []).append(comparison.product2)
        elif comparison.result == "Less":
            adj.setdefault(comparison.product2, []).append(comparison.product1)

    print(adj)
    visited = []
    queue = deque([src_product])
    while queue:
        print(queue)
        node = queue.popleft()
        if node == dest_product:
            return True
        if node in visited:
            continue
        visited.append(node)
        for neighbor in adj.get(node, []):
            print(neighbor)
            queue.append(neighbor)
    
    return False
