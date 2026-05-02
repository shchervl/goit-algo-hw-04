import gc
import random
import timeit

SAMPLES = 3
REPEATS = 7


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


ALGORITHMS = [
    ("Insertion Sort", insertion_sort),
    ("Merge Sort", merge_sort),
    ("Timsort", sorted),
]


def fmt(t: float) -> str:
    return f"{t * 1000:.4f}ms"


def measure(fn, data: list, label: str) -> float:
    print(f"    {label:<14}: ", end="", flush=True)
    times = []
    gc.disable()
    for i in range(REPEATS):
        snapshot = data.copy()
        t = timeit.timeit(lambda: fn(snapshot), number=1)
        times.append(t)
        print("." if i < REPEATS - 1 else "", end="", flush=True)
    gc.enable()
    result = min(times)
    print(f" min={fmt(result)}", flush=True)
    return result


def bench_size(size: int) -> dict:
    times_by_algo: dict[str, list[float]] = {label: [] for label, _ in ALGORITHMS}

    for s in range(1, SAMPLES + 1):
        print(f"  [sample {s}/{SAMPLES}]", flush=True)
        data = [random.randint(0, size * 10) for _ in range(size)]
        for label, fn in ALGORITHMS:
            slug = label.lower().replace(" ", "_")
            times_by_algo[label].append(measure(fn, data, slug))

    return {
        "Size": size,
        **{label: sum(times) / SAMPLES for label, times in times_by_algo.items()},
    }


def crossover(results: list[dict]) -> int | None:
    for r in results:
        if r["Insertion Sort"] > r["Merge Sort"]:
            return r["Size"]
    return None


def compute_stats(results: list[dict]) -> dict:
    first, last = results[0], results[-1]
    cross = crossover(results)
    return {
        "first": first,
        "last": last,
        "cross": cross,
        "ins_vs_merge_large": last["Insertion Sort"] / last["Merge Sort"],
        "merge_vs_tim_large": last["Merge Sort"] / last["Timsort"],
        "ins_vs_tim_large": last["Insertion Sort"] / last["Timsort"],
        "ins_faster_small": first["Merge Sort"] / first["Insertion Sort"],
    }


def print_results(results: list[dict]) -> None:
    print(f"\n{'Size':<10} | {'Insertion':>14} | {'Merge':>14} | {'Timsort':>14}")
    print("-" * 61)
    for r in results:
        print(
            f"{r['Size']:<10} | {fmt(r['Insertion Sort']):>14} | "
            f"{fmt(r['Merge Sort']):>14} | {fmt(r['Timsort']):>14}"
        )


def print_conclusions(results: list[dict]) -> None:
    s = compute_stats(results)
    first, last = s["first"], s["last"]
    cross_str = str(s["cross"]) if s["cross"] is not None else "N/A"

    print("\n--- Висновки ---")
    print(
        f"1. На масиві з {first['Size']} елементів сортування вставками ({fmt(first['Insertion Sort'])}) "
        f"випереджає сортування злиттям ({fmt(first['Merge Sort'])}) у {s['ins_faster_small']:.1f}x. "
        f"\n\tТочка перетину — близько {cross_str} елементів (результати в цій зоні близькі "
        "і можуть варіюватись між запусками): саме тут накладні витрати "
        "рекурсії та виділення пам'яті merge sort починають окупатися."
    )
    print(
        f"2. Починаючи з {cross_str} елементів merge sort стабільно швидший за insertion sort. "
        f"На {last['Size']} елементах різниця — {s['ins_vs_merge_large']:.0f}x "
        f"({fmt(last['Insertion Sort'])} проти {fmt(last['Merge Sort'])}), "
        "що підтверджує теоретичну різницю O(n²) vs O(n log n)."
    )
    print(
        f"3. Timsort перевершує обидва алгоритми на всіх розмірах: "
        f"на {last['Size']} елементах він у {s['merge_vs_tim_large']:.1f}x швидший за merge sort "
        f"і у {s['ins_vs_tim_large']:.0f}x швидший за insertion sort. "
        "\n\tНа малих масивах перевага — не алгоритмічна: Timsort теж використовує insertion sort "
        "для підмасивів (run ≤ 64 елементи), але реалізований у C, тоді як тестова версія — "
        "це інтерпретований Python з overhead на кожну операцію. "
        "\n\tНа великих масивах додається алгоритмічна перевага: адаптивне злиття runs "
        "(пропуск вже відсортованих підпослідовностей) та уникання зайвих алокацій "
        "пам'яті порівняно з рекурсивним merge sort."
    )
    print(
        "4. Отже виходить що варто використовувати вбудовані sorted() / list.sort(): "
        "Timsort реалізований у C, адаптивний до структури вхідних даних і не потребує "
        "ручного підбору алгоритму під розмір масиву."
    )


def collect_results(sizes: list[int]) -> list[dict]:
    results = []
    for size in sizes:
        print(f"\n[size={size}]", flush=True)
        results.append(bench_size(size))
    return results


def run_benchmarks() -> None:
    sizes = [25, 50, 75, 100, 500, 1000, 5000, 10000]
    results = collect_results(sizes)
    print_results(results)
    print_conclusions(results)


if __name__ == "__main__":
    run_benchmarks()
