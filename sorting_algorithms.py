"""
Assignment 1: Comparative Analysis of Sorting Algorithms in E-Commerce Data
Please refer to README.md for the detailed complexity and real-world analysis.
"""

import time
import random
import copy
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

# --- Dataset ---
Products = [
    (101, 250), (102, 120), (103, 450), (104, 300), (105, 200),
    (106, 150), (107, 500), (108, 320), (109, 280), (110, 100)
]


def get_prices(products):
    """Extract prices from product tuples for display."""
    return [p[1] for p in products]


# --- TASK 1 & 2: Sorting Algorithm Implementations with Step-by-Step Tracing ---

# --- MERGE SORT ---
def merge_sort_trace(arr, depth=0, label=""):
    """Merge Sort with detailed step-by-step tracing."""
    indent = "  " * depth
    prices = get_prices(arr)
    
    if len(arr) <= 1:
        print(f"{indent}Base case reached: {prices}")
        return arr
    
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    print(f"{indent}Splitting {prices}")
    print(f"{indent}  Left:  {get_prices(left_half)}")
    print(f"{indent}  Right: {get_prices(right_half)}")
    
    # Recursive splitting
    left_sorted = merge_sort_trace(left_half, depth + 1, "Left")
    right_sorted = merge_sort_trace(right_half, depth + 1, "Right")
    
    # Merging
    merged = merge(left_sorted, right_sorted)
    print(f"{indent}Merging {get_prices(left_sorted)} + {get_prices(right_sorted)} -> {get_prices(merged)}")
    
    return merged


def merge(left, right):
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    """Merge Sort without tracing (for timing)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


# --- QUICK SORT ---
def quick_sort_trace(arr, depth=0):
    """Quick Sort with detailed step-by-step tracing."""
    indent = "  " * depth
    prices = get_prices(arr)
    
    if len(arr) <= 1:
        if arr:
            print(f"{indent}Base case: {prices}")
        return arr
    
    pivot = arr[-1]  # Last element as pivot
    print(f"{indent}Array: {prices}")
    print(f"{indent}Pivot selected: {pivot[1]} (Product {pivot[0]})")
    
    left = [x for x in arr[:-1] if x[1] <= pivot[1]]
    right = [x for x in arr[:-1] if x[1] > pivot[1]]
    
    print(f"{indent}Partitioning around pivot {pivot[1]}:")
    print(f"{indent}  Left  (<= {pivot[1]}): {get_prices(left)}")
    print(f"{indent}  Pivot:           [{pivot[1]}]")
    print(f"{indent}  Right (> {pivot[1]}): {get_prices(right)}")
    
    sorted_left = quick_sort_trace(left, depth + 1)
    sorted_right = quick_sort_trace(right, depth + 1)
    
    result = sorted_left + [pivot] + sorted_right
    print(f"{indent}Combined: {get_prices(result)}")
    return result


def quick_sort(arr):
    """Quick Sort without tracing (for timing)."""
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x[1] <= pivot[1]]
    right = [x for x in arr[:-1] if x[1] > pivot[1]]
    return quick_sort(left) + [pivot] + quick_sort(right)


# --- HEAP SORT ---
def heap_sort_trace(arr):
    """Heap Sort with detailed step-by-step tracing."""
    arr = list(arr)  # Make a copy
    n = len(arr)
    
    print(f"Initial array (prices): {get_prices(arr)}")
    print()
    
    # Phase 1: Build Max-Heap
    print("=" * 50)
    print("Phase 1: Building Max-Heap")
    print("=" * 50)
    for i in range(n // 2 - 1, -1, -1):
        print(f"\nHeapify at index {i} (price={arr[i][1]}):")
        heapify_trace(arr, n, i)
        print(f"  Heap state: {get_prices(arr)}")
    
    print(f"\nMax-Heap built: {get_prices(arr)}")
    print()
    
    # Phase 2: Extract elements
    print("=" * 50)
    print("Phase 2: Extracting elements from heap")
    print("=" * 50)
    for i in range(n - 1, 0, -1):
        print(f"\nStep {n - i}: Swap root ({arr[0][1]}) with last unsorted ({arr[i][1]})")
        arr[0], arr[i] = arr[i], arr[0]
        print(f"  After swap: {get_prices(arr)}")
        print(f"  Sorted portion: {get_prices(arr[i:])}")
        print(f"  Heapifying remaining {i} elements...")
        heapify_trace(arr, i, 0)
        print(f"  Heap state: {get_prices(arr[:i])} | Sorted: {get_prices(arr[i:])}")
    
    print(f"\nFinal sorted array: {get_prices(arr)}")
    return arr


def heapify_trace(arr, n, i):
    """Heapify subtree rooted at index i with tracing."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left][1] > arr[largest][1]:
        largest = left
    if right < n and arr[right][1] > arr[largest][1]:
        largest = right
    
    if largest != i:
        print(f"  Swap {arr[i][1]} with {arr[largest][1]} (index {i} <-> {largest})")
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_trace(arr, n, largest)


def heap_sort(arr):
    """Heap Sort without tracing (for timing)."""
    arr = list(arr)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


def heapify(arr, n, i):
    """Heapify subtree rooted at index i (no tracing)."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left][1] > arr[largest][1]:
        largest = left
    if right < n and arr[right][1] > arr[largest][1]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


# --- TASK 3: Complexity Analysis ---
def print_complexity_table():
    """Display complexity comparison table."""
    headers = ["Algorithm", "Best Case", "Average Case", "Worst Case", "Space Complexity", "Stable?"]
    table = [
        ["Merge Sort",  "O(n log n)", "O(n log n)", "O(n log n)", "O(n)",      "Yes"],
        ["Quick Sort",  "O(n log n)", "O(n log n)", "O(n^2)",    "O(log n)",   "No"],
        ["Heap Sort",   "O(n log n)", "O(n log n)", "O(n log n)", "O(1)",      "No"],
    ]
    print(tabulate(table, headers=headers, tablefmt="grid"))


# --- TASK 4: Experimental Evaluation ---
def generate_synthetic_data(n):
    """Generate synthetic product data with n elements."""
    return [(i, random.randint(10, 100000)) for i in range(1, n + 1)]


def measure_time(sort_func, data, runs=3):
    """Measure average execution time of a sorting function over multiple runs."""
    times = []
    for _ in range(runs):
        data_copy = copy.deepcopy(data)
        start = time.perf_counter()
        sort_func(data_copy)
        end = time.perf_counter()
        times.append(end - start)
    return np.mean(times)


def experimental_evaluation():
    """Run experimental evaluation and return results."""
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    results = {"Merge Sort": [], "Quick Sort": [], "Heap Sort": []}
    
    print("\nRunning experimental evaluation...")
    print("(This may take a minute for large datasets)\n")
    
    for n in sizes:
        print(f"  Testing n = {n:>7,}...", end=" ", flush=True)
        data = generate_synthetic_data(n)
        
        # Merge Sort
        t = measure_time(merge_sort, data)
        results["Merge Sort"].append(t)
        
        # Quick Sort
        t = measure_time(quick_sort, data)
        results["Quick Sort"].append(t)
        
        # Heap Sort
        t = measure_time(heap_sort, data)
        results["Heap Sort"].append(t)
        
        print(f"Done  (M: {results['Merge Sort'][-1]:.5f}s, "
              f"Q: {results['Quick Sort'][-1]:.5f}s, "
              f"H: {results['Heap Sort'][-1]:.5f}s)")
    
    return sizes, results


def print_timing_table(sizes, results):
    """Print execution times in a formatted table."""
    headers = ["n (elements)", "Merge Sort (s)", "Quick Sort (s)", "Heap Sort (s)"]
    table = []
    for i, n in enumerate(sizes):
        table.append([
            f"{n:,}",
            f"{results['Merge Sort'][i]:.6f}",
            f"{results['Quick Sort'][i]:.6f}",
            f"{results['Heap Sort'][i]:.6f}",
        ])
    print(tabulate(table, headers=headers, tablefmt="grid"))


def plot_results(sizes, results, save_path="sorting_comparison.png"):
    """Generate and save comparison graph."""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = {"Merge Sort": "#2196F3", "Quick Sort": "#FF5722", "Heap Sort": "#4CAF50"}
    markers = {"Merge Sort": "o", "Quick Sort": "s", "Heap Sort": "^"}
    
    # --- Linear Scale ---
    ax1 = axes[0]
    for algo, times in results.items():
        ax1.plot(sizes, times, marker=markers[algo], color=colors[algo],
                 linewidth=2, markersize=8, label=algo)
    ax1.set_xlabel("Number of Elements (n)", fontsize=12)
    ax1.set_ylabel("Execution Time (seconds)", fontsize=12)
    ax1.set_title("Sorting Algorithm Comparison (Linear Scale)", fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # --- Log-Log Scale ---
    ax2 = axes[1]
    for algo, times in results.items():
        ax2.plot(sizes, times, marker=markers[algo], color=colors[algo],
                 linewidth=2, markersize=8, label=algo)
    ax2.set_xlabel("Number of Elements (n)", fontsize=12)
    ax2.set_ylabel("Execution Time (seconds)", fontsize=12)
    ax2.set_title("Sorting Algorithm Comparison (Log-Log Scale)", fontsize=14, fontweight='bold')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')

    print(f"\nGraph saved to: {save_path}")


# --- TASK 5: Real-World Decision Analysis ---
def print_real_world_analysis():
    """Print real-world decision analysis."""
    analysis = """
+============================================================================+
|                     TASK 5: REAL-WORLD DECISION ANALYSIS                   |
+============================================================================+
| Please refer to the README.md file for the complete, detailed real-world   |
| decision analysis, including performance trade-offs, space complexities,   |
| and use-case recommendations.                                              |
+============================================================================+
"""
    print(analysis)


# --- MAIN ---
def main():
    separator = "\n" + "=" * 70 + "\n"
    
    # ---- TASK 1 & 2: Implementations with Step-by-Step Trace ----
    print(separator)
    print("DATASET")
    print(separator)
    print("Products (Product_ID, Price in ETB):")
    for p in Products:
        print(f"  Product {p[0]}: {p[1]} ETB")
    print(f"\nPrices: {get_prices(Products)}")
    
    # --- Merge Sort ---
    print(separator)
    print("TASK 1 & 2: MERGE SORT - Step-by-Step Trace")
    print(separator)
    print(f"Input (prices): {get_prices(Products)}\n")
    merge_result = merge_sort_trace(copy.deepcopy(Products))
    print(f"\n[OK] Merge Sort Result: {[(p[0], p[1]) for p in merge_result]}")
    print(f"  Sorted prices: {get_prices(merge_result)}")
    
    # --- Quick Sort ---
    print(separator)
    print("TASK 1 & 2: QUICK SORT - Step-by-Step Trace")
    print(separator)
    print(f"Input (prices): {get_prices(Products)}\n")
    quick_result = quick_sort_trace(copy.deepcopy(Products))
    print(f"\n[OK] Quick Sort Result: {[(p[0], p[1]) for p in quick_result]}")
    print(f"  Sorted prices: {get_prices(quick_result)}")
    
    # --- Heap Sort ---
    print(separator)
    print("TASK 1 & 2: HEAP SORT - Step-by-Step Trace")
    print(separator)
    heap_result = heap_sort_trace(copy.deepcopy(Products))
    print(f"\n[OK] Heap Sort Result: {[(p[0], p[1]) for p in heap_result]}")
    print(f"  Sorted prices: {get_prices(heap_result)}")
    
    # ---- TASK 3: Complexity Analysis ----
    print(separator)
    print("TASK 3: COMPLEXITY ANALYSIS")
    print(separator)
    print_complexity_table()
    
    # ---- TASK 4: Experimental Evaluation ----
    print(separator)
    print("TASK 4: EXPERIMENTAL EVALUATION")
    print(separator)
    sizes, results = experimental_evaluation()
    print()
    print_timing_table(sizes, results)
    plot_results(sizes, results, save_path=r"c:\Users\DELL\Desktop\reacJS\DAA\sorting_comparison.png")
    
    # ---- TASK 5: Real-World Decision ----
    print(separator)
    print_real_world_analysis()
    
    print("\n[DONE] All tasks completed successfully!")


if __name__ == "__main__":
    main()
