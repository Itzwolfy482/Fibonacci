#include <iostream>
#include <unordered_map>
#include <chrono>
#include <iomanip>
#include <fstream>
#include <string>
#include <gmp.h>
#include <gmpxx.h>
#include <vector>

using namespace std;
using namespace std::chrono;

// Matrix class for 2x2 matrices using GMP arbitrary precision integers
class Matrix2x2 {
public:
    mpz_class a, b, c, d;
    
    Matrix2x2() : a(0), b(0), c(0), d(0) {}
    Matrix2x2(mpz_class a, mpz_class b, mpz_class c, mpz_class d) 
        : a(a), b(b), c(c), d(d) {}
    
    // Matrix multiplication
    Matrix2x2 operator*(const Matrix2x2& other) const {
        return Matrix2x2(
            a * other.a + b * other.c,
            a * other.b + b * other.d,
            c * other.a + d * other.c,
            c * other.b + d * other.d
        );
    }
    
    bool operator==(const Matrix2x2& other) const {
        return a == other.a && b == other.b && c == other.c && d == other.d;
    }
    
    void print() const {
        cout << "[[" << a << ", " << b << "], [" << c << ", " << d << "]]" << endl;
    }
};

// Utility function to format time duration
string format_duration(nanoseconds duration) {
    auto ns = duration.count();
    if (ns < 1000) {
        return to_string(ns) + " ns";
    } else if (ns < 1000000) {
        return to_string(ns / 1000.0) + " μs";
    } else if (ns < 1000000000) {
        return to_string(ns / 1000000.0) + " ms";
    } else {
        return to_string(ns / 1000000000.0) + " s";
    }
}

class FibonacciCalculator {
private:
    // Cache for memoization - maps exponent to resulting matrix
    unordered_map<long long, Matrix2x2> cache;
    Matrix2x2 base_matrix;
    
    // Statistics
    int cache_hits = 0;
    int cache_misses = 0;
    
public:
    FibonacciCalculator() : base_matrix(1, 1, 1, 0) {
        // Initialize with identity matrix for exponent 0
        cache[0] = Matrix2x2(1, 0, 0, 1);  // Identity matrix
        cache[1] = base_matrix;             // Base matrix
    }
    
    // Fast matrix exponentiation with memoization
    Matrix2x2 matrix_power(long long n) {
        if (n == 0) return Matrix2x2(1, 0, 0, 1);  // Identity matrix
        if (n == 1) return base_matrix;
        
        // Check cache first
        auto it = cache.find(n);
        if (it != cache.end()) {
            cache_hits++;
            return it->second;
        }
        
        cache_misses++;
        
        Matrix2x2 result;
        if (n % 2 == 0) {
            // Even power: A^n = (A^(n/2))^2
            Matrix2x2 half_power = matrix_power(n / 2);
            result = half_power * half_power;
        } else {
            // Odd power: A^n = A * A^(n-1)
            result = base_matrix * matrix_power(n - 1);
        }
        
        // Cache the result
        cache[n] = result;
        return result;
    }
    
    // Calculate nth Fibonacci number
    mpz_class fibonacci(long long n) {
        if (n == 0) return 0;
        if (n == 1) return 1;
        
        Matrix2x2 result = matrix_power(n - 1);
        return result.a;  // F(n) is in the top-left position
    }
    
    // Calculate and save to file (for very large numbers)
    bool fibonacci_to_file(long long n, const string& filename) {
        cout << "Calculating F(" << n << ") and saving to " << filename << "..." << endl;
        
        auto start = high_resolution_clock::now();
        mpz_class result = fibonacci(n);
        auto calc_end = high_resolution_clock::now();
        
        cout << "Calculation completed. Writing to file..." << endl;
        
        auto write_start = high_resolution_clock::now();
        ofstream file(filename);
        if (!file.is_open()) {
            cout << "Error: Could not create file " << filename << endl;
            return false;
        }
        
        // Write header information
        file << "Fibonacci Number F(" << n << ")" << endl;
        file << "Calculated using Matrix Exponentiation with Memoization" << endl;
        file << "Number of digits: " << result.get_str().length() << endl;
        file << "Calculation time: " << format_duration(duration_cast<nanoseconds>(calc_end - start)) << endl;
        file << "Generated on: " << __DATE__ << " " << __TIME__ << endl;
        file << "========================================" << endl << endl;
        
        // Write the actual number
        file << result.get_str();
        
        file.close();
        auto write_end = high_resolution_clock::now();
        
        cout << "Successfully saved F(" << n << ") to " << filename << endl;
        cout << "Number of digits: " << result.get_str().length() << endl;
        cout << "Calculation time: " << format_duration(duration_cast<nanoseconds>(calc_end - start)) << endl;
        cout << "File write time: " << format_duration(duration_cast<nanoseconds>(write_end - write_start)) << endl;
        
        return true;
    }
    
    // Get cache statistics
    void print_stats() const {
        cout << "\n=== Cache Statistics ===" << endl;
        cout << "Cache hits: " << cache_hits << endl;
        cout << "Cache misses: " << cache_misses << endl;
        cout << "Cache size: " << cache.size() << endl;
        cout << "Hit ratio: " << fixed << setprecision(2) 
             << (cache_hits * 100.0 / (cache_hits + cache_misses)) << "%" << endl;
    }
    
    void clear_stats() {
        cache_hits = 0;
        cache_misses = 0;
    }
};

int main() {
    FibonacciCalculator calc;
    
    cout << "Fibonacci Calculator using Matrix Exponentiation with Memorization" << endl;
    cout << "=================================================================" << endl;
    
    // Test cases
    vector<long long> test_cases = {10, 50, 100, 500, 1000, 5000, 10000, 50000};
    
    for (long long n : test_cases) {
        cout << "\nCalculating F(" << n << ")..." << endl;
        
        // Clear stats for this calculation
        calc.clear_stats();
        
        // Time the calculation
        auto start = high_resolution_clock::now();
        mpz_class result = calc.fibonacci(n);
        auto end = high_resolution_clock::now();
        
        auto duration = duration_cast<nanoseconds>(end - start);
        
        // Display results
        cout << "F(" << n << ") = ";
        string result_str = result.get_str();
        if (result_str.length() > 100) {
            cout << result_str.substr(0, 50) << "..." << result_str.substr(result_str.length() - 50) 
                 << " (" << result_str.length() << " digits)" << endl;
        } else {
            cout << result_str << endl;
        }
        
        cout << "Time taken: " << format_duration(duration) << endl;
        calc.print_stats();
    }
    
    // Interactive mode
    cout << "\n\nInteractive Mode:" << endl;
    cout << "=================" << endl;
    cout << "1. Enter positive number for console output" << endl;
    cout << "2. Enter negative number to save to file (e.g., -1000000000 for F(1 billion))" << endl;
    cout << "3. Enter 0 to exit" << endl;
    
    long long n;
    while (true) {
        cout << "\nEnter n (positive for console, negative for file, 0 to exit): ";
        cin >> n;
        
        if (n == 0) break;
        
        if (n < 0) {
            // File output mode
            long long actual_n = -n;
            string filename = "fibonacci_" + to_string(actual_n) + ".txt";
            
            cout << "This will calculate F(" << actual_n << ") and save to " << filename << endl;
            cout << "Warning: F(" << actual_n << ") will have approximately " 
                 << (long long)(actual_n * 0.2089877) << " digits." << endl;
            
            if (actual_n >= 100000000) {
                cout << "This is a very large number that may take significant time and memory!" << endl;
                cout << "Continue? (y/n): ";
                char confirm;
                cin >> confirm;
                if (confirm != 'y' && confirm != 'Y') {
                    cout << "Cancelled." << endl;
                    continue;
                }
            }
            
            calc.clear_stats();
            if (calc.fibonacci_to_file(actual_n, filename)) {
                calc.print_stats();
            }
        } else {
            // Console output mode (existing code)
            calc.clear_stats();
            
            auto start = high_resolution_clock::now();
            mpz_class result = calc.fibonacci(n);
            auto end = high_resolution_clock::now();
            
            auto duration = duration_cast<nanoseconds>(end - start);
            
            cout << "F(" << n << ") = ";
            string result_str = result.get_str();
            if (result_str.length() > 200) {
                cout << result_str.substr(0, 100) << "..." << result_str.substr(result_str.length() - 100) 
                     << "\n(" << result_str.length() << " digits)" << endl;
            } else {
                cout << result_str << endl;
            }
            
            cout << "Time taken: " << format_duration(duration) << endl;
            calc.print_stats();
        }
    }
    
    cout << "Goodbye!" << endl;
    return 0;
}