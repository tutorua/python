# Fisher-Yates algorithm shuffle array in (O(n)) time complexity


def shuffle(a: list[int]) -> list[int]:
    """Shuffle a list in place using the Fisher-Yates algorithm."""
    import random
    n = len(a)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        a[i], a[j] = a[j], a[i]
    return a

if __name__ == "__main__":
    # Example usage
    original_list = [1, 2, 3, 4, 5]
    shuffled_list = shuffle(original_list.copy())
    print("Original list:", original_list)
    print("Shuffled list:", shuffled_list)
