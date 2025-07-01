#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Optimized big integer matrix multiplication using Python's PyLong operations
static PyObject* matrix_multiply_bigint(PyObject* m_list, PyObject* n_list) {
    // Extract matrix elements as PyLong objects
    PyObject *m00, *m01, *m10, *m11;
    PyObject *n00, *n01, *n10, *n11;
    
    // Get matrix m elements
    PyObject *m_row0 = PyList_GetItem(m_list, 0);
    PyObject *m_row1 = PyList_GetItem(m_list, 1);
    m00 = PyList_GetItem(m_row0, 0);
    m01 = PyList_GetItem(m_row0, 1);
    m10 = PyList_GetItem(m_row1, 0);
    m11 = PyList_GetItem(m_row1, 1);
    
    // Get matrix n elements
    PyObject *n_row0 = PyList_GetItem(n_list, 0);
    PyObject *n_row1 = PyList_GetItem(n_list, 1);
    n00 = PyList_GetItem(n_row0, 0);
    n01 = PyList_GetItem(n_row0, 1);
    n10 = PyList_GetItem(n_row1, 0);
    n11 = PyList_GetItem(n_row1, 1);
    
    // Calculate: a = m[1][0]*n[0][1] + m[1][1]*n[1][1]
    PyObject *temp1 = PyNumber_Multiply(m10, n01);  // m[1][0] * n[0][1]
    if (!temp1) return NULL;
    
    PyObject *temp2 = PyNumber_Multiply(m11, n11);  // m[1][1] * n[1][1]
    if (!temp2) {
        Py_DECREF(temp1);
        return NULL;
    }
    
    PyObject *a = PyNumber_Add(temp1, temp2);       // a = sum
    Py_DECREF(temp1);
    Py_DECREF(temp2);
    if (!a) return NULL;
    
    // Calculate: b = m[0][0]*n[0][1] + m[0][1]*n[1][1]
    temp1 = PyNumber_Multiply(m00, n01);            // m[0][0] * n[0][1]
    if (!temp1) {
        Py_DECREF(a);
        return NULL;
    }
    
    temp2 = PyNumber_Multiply(m01, n11);            // m[0][1] * n[1][1]
    if (!temp2) {
        Py_DECREF(temp1);
        Py_DECREF(a);
        return NULL;
    }
    
    PyObject *b = PyNumber_Add(temp1, temp2);       // b = sum
    Py_DECREF(temp1);
    Py_DECREF(temp2);
    if (!b) {
        Py_DECREF(a);
        return NULL;
    }
    
    // Calculate result matrix: [[a+b, b], [b, a]]
    PyObject *a_plus_b = PyNumber_Add(a, b);        // a + b
    if (!a_plus_b) {
        Py_DECREF(a);
        Py_DECREF(b);
        return NULL;
    }
    
    // Build result matrix
    PyObject *result = PyList_New(2);
    PyObject *row0 = PyList_New(2);
    PyObject *row1 = PyList_New(2);
    
    // Row 0: [a+b, b]
    Py_INCREF(a_plus_b);
    Py_INCREF(b);
    PyList_SetItem(row0, 0, a_plus_b);
    PyList_SetItem(row0, 1, b);
    
    // Row 1: [b, a]
    Py_INCREF(b);
    Py_INCREF(a);
    PyList_SetItem(row1, 0, b);
    PyList_SetItem(row1, 1, a);
    
    PyList_SetItem(result, 0, row0);
    PyList_SetItem(result, 1, row1);
    
    // Clean up
    Py_DECREF(a);
    Py_DECREF(b);
    Py_DECREF(a_plus_b);
    
    return result;
}

// Fast matrix exponentiation for Fibonacci
static PyObject* fibonacci_matrix_power(PyObject* self, PyObject* args) {
    unsigned long long n;
    
    if (!PyArg_ParseTuple(args, "K", &n)) {
        return NULL;
    }
    
    if (n == 0) {
        return PyLong_FromLong(0);
    }
    if (n == 1) {
        return PyLong_FromLong(1);
    }
    
    // Create base matrix [[1, 1], [1, 0]]
    PyObject *one = PyLong_FromLong(1);
    PyObject *zero = PyLong_FromLong(0);
    
    PyObject *base_row0 = PyList_New(2);
    PyObject *base_row1 = PyList_New(2);
    PyObject *base = PyList_New(2);
    
    Py_INCREF(one); Py_INCREF(one);
    PyList_SetItem(base_row0, 0, one);
    PyList_SetItem(base_row0, 1, one);
    
    Py_INCREF(one); Py_INCREF(zero);
    PyList_SetItem(base_row1, 0, one);
    PyList_SetItem(base_row1, 1, zero);
    
    PyList_SetItem(base, 0, base_row0);
    PyList_SetItem(base, 1, base_row1);
    
    // Create identity matrix [[1, 0], [0, 1]]
    PyObject *id_row0 = PyList_New(2);
    PyObject *id_row1 = PyList_New(2);
    PyObject *result = PyList_New(2);
    
    Py_INCREF(one); Py_INCREF(zero);
    PyList_SetItem(id_row0, 0, one);
    PyList_SetItem(id_row0, 1, zero);
    
    Py_INCREF(zero); Py_INCREF(one);
    PyList_SetItem(id_row1, 0, zero);
    PyList_SetItem(id_row1, 1, one);
    
    PyList_SetItem(result, 0, id_row0);
    PyList_SetItem(result, 1, id_row1);
    
    // Fast exponentiation
    unsigned long long power = n - 1;
    
    while (power > 0) {
        if (power & 1) {
            PyObject *new_result = matrix_multiply_bigint(result, base);
            if (!new_result) {
                Py_DECREF(result);
                Py_DECREF(base);
                return NULL;
            }
            Py_DECREF(result);
            result = new_result;
        }
        
        PyObject *new_base = matrix_multiply_bigint(base, base);
        if (!new_base) {
            Py_DECREF(result);
            Py_DECREF(base);
            return NULL;
        }
        Py_DECREF(base);
        base = new_base;
        
        power >>= 1;
    }
    
    // Extract F(n) from result[0][0]
    PyObject *result_row0 = PyList_GetItem(result, 0);
    PyObject *fib_result = PyList_GetItem(result_row0, 0);
    Py_INCREF(fib_result);
    
    Py_DECREF(result);
    Py_DECREF(base);
    
    return fib_result;
}

// Direct matrix multiplication function
static PyObject* mmfv4_bigint(PyObject* self, PyObject* args) {
    PyObject *m_list, *n_list;
    
    if (!PyArg_ParseTuple(args, "OO", &m_list, &n_list)) {
        return NULL;
    }
    
    // Validate input matrices
    if (!PyList_Check(m_list) || !PyList_Check(n_list)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be lists");
        return NULL;
    }
    
    if (PyList_Size(m_list) != 2 || PyList_Size(n_list) != 2) {
        PyErr_SetString(PyExc_ValueError, "Matrices must be 2x2");
        return NULL;
    }
    
    // Validate rows
    for (int i = 0; i < 2; i++) {
        PyObject *m_row = PyList_GetItem(m_list, i);
        PyObject *n_row = PyList_GetItem(n_list, i);
        
        if (!PyList_Check(m_row) || !PyList_Check(n_row)) {
            PyErr_SetString(PyExc_TypeError, "Matrix rows must be lists");
            return NULL;
        }
        
        if (PyList_Size(m_row) != 2 || PyList_Size(n_row) != 2) {
            PyErr_SetString(PyExc_ValueError, "Matrix rows must have 2 elements");
            return NULL;
        }
    }
    
    return matrix_multiply_bigint(m_list, n_list);
}

// Method definitions
static PyMethodDef mmfv4_methods[] = {
    {"mmfv4_bigint", mmfv4_bigint, METH_VARARGS, "Big integer 2x2 matrix multiplication"},
    {"fibonacci", fibonacci_matrix_power, METH_VARARGS, "Fast Fibonacci calculation using matrix exponentiation"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef mmfv4_module = {
    PyModuleDef_HEAD_INIT,
    "mmfv4",
    "Big integer matrix multiplication module for large Fibonacci calculations",
    -1,
    mmfv4_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_mmfv4(void) {
    return PyModule_Create(&mmfv4_module);
}