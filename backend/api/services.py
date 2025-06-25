from collections import deque
from django.db.models import Q
from .models import Comparison, Product, Category

def path_exists(user, category, src_product, dest_product):
    # Build an adjacency list for the comparisons
    queryset = Comparison.objects.filter(user=user, category=category)
    adj = {}
    for comparison in queryset:
        if comparison.result == "More":
            adj.setdefault(comparison.product1, []).append(comparison.product2)
        elif comparison.result == "Less":
            adj.setdefault(comparison.product2, []).append(comparison.product1)

    # Perform BFS to check if a path exists
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


def compute_rankings():
    categories = Category.objects.all()
    products = Product.objects.all()
    rankings = {}

    # Calculate score for each product in each category using Copeland's method
    for category in categories:
        rankings[category] = [{'Product': product, 'Score': 0} for product in products]
        for i in range(len(products)):
            for j in range(i + 1, len(products)):
                product1 = products[i]
                product2 = products[j]
                result = get_pair_result(category, product1, product2)
                if result == 'Product1':
                    rankings[category][i]['Score'] += 1
                elif result == 'Product2':
                    rankings[category][j]['Score'] += 1
                else:
                    rankings[category][i]['Score'] += 0.5
                    rankings[category][j]['Score'] += 0.5

    # Sort products by score and assign ranks
    for category, product_scores in rankings.items():
        rankings[category] = sorted(product_scores, key=lambda x: x['Score'], reverse=True)
        for i in range(len(rankings[category])):
            if i > 0 and rankings[category][i]['Score'] == rankings[category][i - 1]['Score']:
                rankings[category][i]['Rank'] = rankings[category][i - 1]['Rank']
            else:
                rankings[category][i]['Rank'] = i + 1
    
    return rankings
