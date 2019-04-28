import itertools
import math
from multiprocessing import Pool
import timeit

def sieve_primes(n):
    a = [True for x in range(n + 1)]
    i = 2
    while i <= math.sqrt(n):
        if a[i]:
            for j in range(i*i, n + 1, i):
                a[j] = False
        i += 1
    return [i for i in range(2, len(a)) if a[i]]
    
def segment_primes(start, end):
    root_limit = int(math.sqrt(end)) + 1
    root_primes = sieve_primes(root_limit)
    a = [True for x in range(end - start + 1)]
    for root_prime in root_primes:
        prime_multiple = start - start % root_prime
        while prime_multiple < start or prime_multiple == root_prime:
            prime_multiple += root_prime
        for j in range(prime_multiple, end + 1, root_prime):
            a[j - start] = False
    if start == 1: a[0] = False
    return [i + start for i in range(0, len(a)) if a[i]]
    
def runner(i, n, segment_size):
    start = i
    end = min(i + segment_size - 1, n)
    result = segment_primes(start, end)
    print('done')
    return result

def runner_star(i_n_segment_size):
    return runner(*i_n_segment_size)

def multithreaded_segmented_primes(n, segment_size=None):
    if segment_size is None: segment_size = n // 10
    rng = range(1, n + 1, segment_size)
    p = Pool(len(rng))
    primess = p.map(runner_star, zip(rng, itertools.repeat(n), itertools.repeat(segment_size)))
    primes = []
    for ps in primess:
        primes.extend(ps)
    return primes

def main():
    print(timeit.timeit(lambda: multithreaded_segmented_primes(100000000), number=1))

if __name__ == '__main__':
    main()
