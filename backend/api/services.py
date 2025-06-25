from collections import deque
from django.db.models import Q
from .models import Comparison

def path_exists(user, category, src_product, dest_product):
    # build an adjacency list for the comparisons
    queryset = Comparison.objects.filter(user=user, category=category)
    adj = {}
    for comparison in queryset:
        if comparison.result == "More":
            adj.setdefault(comparison.product1, []).append(comparison.product2)
        elif comparison.result == "Less":
            adj.setdefault(comparison.product2, []).append(comparison.product1)

    # perform BFS to check if a path exists
    visited = []
    queue = deque([src_product])
    while queue:
        node = queue.popleft()
        if node == dest_product:
            return True
        if node in visited:
            continue
        visited.append(node)
        for neighbor in adj.get(node, []):
            queue.append(neighbor)
    
    return False


def get_pair_result(category, product1, product2):
    comparisons = Comparison.objects.filter(category=category, product1__in=[product1, product2], product2__in=[product1, product2])
    wins1 = comparisons.filter(Q(product1=product1, result='More') | Q(product2=product1, result='Less')).count()
    wins2 = comparisons.filter(Q(product1=product2, result='More') | Q(product2=product2, result='Less')).count()

    if wins1 > wins2:
        return 'Product1'
    elif wins2 > wins1:
        return 'Product2'
    return 'Draw'
