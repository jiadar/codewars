def josephus_survivor(n,k):
    prev = 1
    for i in range(1, n+1):
        cur = (prev + k - 1) % i + 1
        print(f"i = {i}: (( {prev} + {k} - 1) % {i} ) + 1  = {cur}")
        prev = cur
    return cur

josephus_survivor(7, 3)
