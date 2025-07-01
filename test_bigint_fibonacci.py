import mmfv4
import time
import sys

sys.set_int_max_str_digits(100000000)
def fibonacci_python_matrix(n):
    """Pure Python matrix exponentiation for comparison"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    def matrix_mult(m, n):
        a = m[1][0] * n[0][1] + m[1][1] * n[1][1]
        b = m[0][0] * n[0][1] + m[0][1] * n[1][1]
        return [[a + b, b], [b, a]]
    
    base = [[1, 1], [1, 0]]
    result = [[1, 0], [0, 1]]  # Identity
    
    power = n - 1
    while power > 0:
        if power & 1:
            result = matrix_mult(result, base)
        base = matrix_mult(base, base)
        power >>= 1
    
    return result[0][0]

def fibonacci_python_iterative(n):
    """Simple iterative approach for comparison"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def test_correctness():
    """Test that C extension produces correct results"""
    print("Testing correctness...")
    
    test_cases = [0, 1, 2, 3, 5, 8, 10, 20, 50, 100]
    
    for n in test_cases:
        c_result = mmfv4.fibonacci(n)
        py_result = fibonacci_python_matrix(n)
        iter_result = fibonacci_python_iterative(n)
        
        if c_result == py_result == iter_result:
            print(f"F({n}) = {c_result} ✓")
        else:
            print(f"F({n}) MISMATCH: C={c_result}, Py={py_result}, Iter={iter_result}")
            return False
    
    return True

def benchmark_large_fibonacci():
    """Benchmark large Fibonacci calculations"""
    print("\nBenchmarking large Fibonacci calculations...")
    
    test_sizes = [1000, 10000, 100000]
    
    for n in test_sizes:
        print(f"\nCalculating F({n}):")
        
        # C extension
        start_time = time.perf_counter()
        c_result = mmfv4.fibonacci(n)
        c_time = time.perf_counter() - start_time
        
        # Python matrix
        start_time = time.perf_counter()
        py_result = fibonacci_python_matrix(n)
        py_time = time.perf_counter() - start_time
        
        # Verify results match
        if c_result == py_result:
            print(f"  C extension: {c_time:.6f} seconds")
            print(f"  Python:      {py_time:.6f} seconds")
            print(f"  Speedup:     {py_time/c_time:.2f}x")
            print(f"  Digits:      {len(str(c_result))}")
        else:
            print(f"  Results don't match!")

def benchmark_million():
    """Benchmark F(1,000,000)"""
    print(f"\n{'='*50}")
    print("ULTIMATE TEST: F(1,000,000)")
    print(f"{'='*50}")
    
    start_time = time.perf_counter()
    result = mmfv4.fibonacci(1000000)
    end_time = time.perf_counter()
    
    calc_time = end_time - start_time
    digits = len(str(result))
    
    print(f"F(1,000,000) calculated in {calc_time:.6f} seconds")
    print(f"Result has {digits:,} digits")
    print(f"First 100 digits: {str(result)[:100]}...")
    print(f"Last 100 digits:  ...{str(result)[-100:]}")

def test_matrix_multiplication():
    """Test direct matrix multiplication"""
    print("\nTesting matrix multiplication...")
    
    # Test with big integers
    m = [[12345678901234567890, 98765432109876543210],
         [11111111111111111111, 22222222222222222222]]
    
    n = [[33333333333333333333, 44444444444444444444],
         [55555555555555555555, 66666666666666666666]]
    
    start_time = time.perf_counter()
    result = mmfv4.mmfv4_bigint(m, n)
    c_time = time.perf_counter() - start_time
    
    print(f"Big integer matrix multiplication: {c_time:.6f} seconds")
    print(f"Result: {result}")

if __name__ == "__main__":
    if test_correctness():
        print("✓ All correctness tests passed!")
        
        test_matrix_multiplication()
        benchmark_large_fibonacci()
        
        # Uncomment for the ultimate test (will take some time!)
        # benchmark_million()
        
        print(f"\n{'='*50}")
        print("Ready for F(1,000,000) calculation!")
        print("Uncomment benchmark_million() to run the ultimate test.")
        print(f"{'='*50}")
    else:
        print("✗ Correctness tests failed!")