def precision_at_k(recommended, gold, k=5):
    recommended_k = recommended[:k]
    correct = len([c for c in recommended_k if c in gold])
    return correct / k