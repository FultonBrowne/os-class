import multiprocessing
import numpy as np
import time
import os
import psutil

def set_low_priority():
    """Set the process priority to low."""
    p = psutil.Process(os.getpid())
    try:
        if os.name == 'nt':
            # On Windows
            p.nice(psutil.IDLE_PRIORITY_CLASS)
        else:
            # On Unix/Linux
            p.nice(10)  # Increase niceness to lower priority
    except psutil.AccessDenied:
        print("Access Denied when trying to set low priority.")

def set_high_priority():
    """Set the process priority to high."""
    p = psutil.Process(os.getpid())
    try:
        if os.name == 'nt':
            # On Windows
            p.nice(psutil.HIGH_PRIORITY_CLASS)
        else:
            # On Unix/Linux
            p.nice(-10)  # Decrease niceness to increase priority
    except psutil.AccessDenied:
        print("Access Denied when trying to set high priority.")

def matrix_multiplication(name, priority):
    """Perform a heavy matrix multiplication task."""
    if priority == 'low':
        set_low_priority()
    else:
        set_high_priority()
    p = psutil.Process(os.getpid())
    print(f"{name} started with priority {p.nice()}")

    size = 5000  # Adjust size to make the computation take ~30 seconds
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    start_time = time.time()
    C = np.dot(A, B)
    end_time = time.time()
    print(f"{name} finished in {end_time - start_time:.2f} seconds.")

def eigenvalue_computation(name, priority):
    """Compute the eigenvalues of a large random matrix."""
    if priority == 'low':
        set_low_priority()
    else:
        set_high_priority()
    p = psutil.Process(os.getpid())
    print(f"{name} started with priority {p.nice()}")

    size = 3000  # Adjust size to make the computation take ~30 seconds
    A = np.random.rand(size, size)
    start_time = time.time()
    eigenvalues = np.linalg.eigvals(A)
    end_time = time.time()
    print(f"{name} finished in {end_time - start_time:.2f} seconds.")

def singular_value_decomposition(name, priority):
    """Perform SVD on a large random matrix."""
    if priority == 'low':
        set_low_priority()
    else:
        set_high_priority()
    p = psutil.Process(os.getpid())
    print(f"{name} started with priority {p.nice()}")

    size = 2000  # Adjust size to make the computation take ~30 seconds
    A = np.random.rand(size, size)
    start_time = time.time()
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    end_time = time.time()
    print(f"{name} finished in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    # Define the tasks
    tasks = [
        (matrix_multiplication, "Matrix Multiplication Task 1", 'low'),
        (eigenvalue_computation, "Eigenvalue Computation Task 1", 'low'),
        (singular_value_decomposition, "SVD Task 1", 'low'),
        (matrix_multiplication, "Matrix Multiplication Task 2", 'high'),
        (eigenvalue_computation, "Eigenvalue Computation Task 2", 'high'),
        (singular_value_decomposition, "SVD Task 2", 'high'),
    ]

    # Create processes
    processes = []
    for func, name, priority in tasks:
        p = multiprocessing.Process(target=func, args=(name, priority))
        processes.append(p)

    # Start processes
    for p in processes:
        p.start()

    # Monitor processes
    total = len(processes)
    # Wait for all processes to finish
    for p in processes:
        p.join()

    print("All processes completed.")
