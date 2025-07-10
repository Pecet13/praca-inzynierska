from collections import deque
from django.db import transaction
from django.db.models import Q
from .models import Comparison, Product, Category, Ranking, User

def user_path_exists(user, category, src_product_id, dest_product_id):
    # Build an adjacency list for the comparisons
    queryset = Comparison.objects.filter(user=user, category=category)
    adj = {}
    for comparison in queryset:
        if comparison.result == "More":
            adj.setdefault(comparison.product1.id, set()).add(comparison.product2.id)
        elif comparison.result == "Less":
            adj.setdefault(comparison.product2.id, set()).add(comparison.product1.id)

    # Perform BFS to check if a path exists
    visited = set()
    queue = deque([src_product_id])
    while queue:
        node = queue.popleft()
        if node == dest_product_id:
            return True
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adj.get(node, ()):
            queue.append(neighbor)
    
    return False


def get_pair_result(category, product1, product2, user=None):
    if user is None:
        ai_users = User.objects.filter(id__in=[1, 2])
        comparisons = Comparison.objects.filter(category=category, product1__in=[product1, product2], product2__in=[product1, product2]).exclude(user__in=ai_users)
    else:
        comparisons = Comparison.objects.filter(category=category, product1__in=[product1, product2], product2__in=[product1, product2], user=user)
    wins1 = comparisons.filter(Q(product1=product1, result='More') | Q(product2=product1, result='Less')).count()
    wins2 = comparisons.filter(Q(product1=product2, result='More') | Q(product2=product2, result='Less')).count()

    if wins1 > wins2:
        return 'Product1'
    elif wins2 > wins1:
        return 'Product2'
    elif wins1 == wins2 and comparisons.exists():
        return 'Draw'
    return None


def compute_rankings(user=None):
    categories = Category.objects.all()
    rankings = {}

    if user is not None:
        user = User.objects.get(id=user)

    for category in categories:
        products = Product.objects.filter(product_type=category.product_type)
        rankings[category] = [{'Product': product, 'Score': 0, 'User': user} for product in products]
        
        # Get score for direct comparisons
        direct = {}
        for i in range(len(products)):
            for j in range(i + 1, len(products)):
                product1 = products[i]
                product2 = products[j]
                result = get_pair_result(category, product1, product2, user)
                if result == 'Product1':
                    direct [(i, j)] = 1
                elif result == 'Product2':
                    direct [(j, i)] = 1
                elif result == 'Draw':
                    direct [(i, j)] = direct [(j, i)] = 0.5

        # Build an adjacency list for the direct comparisons
        adj = {}
        for (p1, p2), score in direct.items():
            if score == 1:
                adj.setdefault(p1, set()).add(p2)

        # Compute transitive closure using BFS
        reachable = {i: set() for i in range(len(products))}
        for src in range(len(products)):
            queue = deque([src])
            while queue:
                node = queue.popleft()
                for neighbor in adj.get(node, ()):
                    if neighbor not in reachable[src]:
                        reachable[src].add(neighbor)
                        queue.append(neighbor)

        # Infer score for indirect comparisons
        for i in range(len(products)):
            for j in range(len(products)):
                if i == j or (i, j) in direct or (j, i) in direct:
                    continue
                if j in reachable[i]:
                    direct[(i, j)] = 1
                elif i in reachable[j]:
                    direct[(j, i)] = 1
                else:
                    direct[(i, j)] = direct[(j, i)] = 0.5

        # Calculate score for each product using Copeland's method
        for (p1, p2), score in direct.items():
            rankings[category][p1]['Score'] += score

    # Sort products by score and assign ranks
    for category, product_scores in rankings.items():
        rankings[category] = sorted(product_scores, key=lambda x: x['Score'], reverse=True)
        for i in range(len(rankings[category])):
            if i > 0 and rankings[category][i]['Score'] == rankings[category][i - 1]['Score']:
                rankings[category][i]['Rank'] = rankings[category][i - 1]['Rank']
            else:
                rankings[category][i]['Rank'] = i + 1
    
    return rankings


@transaction.atomic
def update_rankings():
    users = [None]
    ai_users = User.objects.filter(id__in=[1, 2])

    # Check if rankings for ChatGPT and Gemini exist
    for ai_user in ai_users:
        if not Ranking.objects.filter(user=ai_user).exists():
            users.append(ai_user.id)
    
    for user in users:
        rankings = compute_rankings(user)
        for category, product_scores in rankings.items():
            for product_score in product_scores:
                product = product_score['Product']
                score = product_score['Score']
                rank = product_score['Rank']
                user = product_score['User']
                Ranking.objects.update_or_create(
                    category=category,
                    product=product,
                    user=user,
                    defaults={'score': score, 'rank': rank}
                )
    