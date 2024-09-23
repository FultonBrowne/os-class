import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
import time

# Function to multiply a slice of matrix A with matrix B
def matrix_multiply(start_row, end_row, A, B, result, sync_event=None):
    if sync_event:
        sync_event.wait()  # Synchronize threads
    print(f"Thread handling rows {start_row} to {end_row} started.")

    result[start_row:end_row, :] = np.dot(A[start_row:end_row, :], B)
    print(f"Thread handling rows {start_row} to {end_row} completed.")

# Set matrix dimensions (try larger matrices for more noticeable effects)
N = 1000  # Number of rows/columns

# Generate random matrices A and B
A = np.random.rand(N, N)
B = np.random.rand(N, N)

# Result matrix initialized to zeros
result = np.zeros((N, N))

# Number of threads
num_threads = 5
chunk_size = N // num_threads

# Synchronization events for controlling the execution order of threads
events = [threading.Event() for _ in range(num_threads)]

# Create a thread pool
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = []
    for i in range(num_threads):
        start_row = i * chunk_size
        end_row = (i + 1) * chunk_size if i != num_threads - 1 else N
        futures.append(executor.submit(matrix_multiply, start_row, end_row, A, B, result, events[i]))

    # Simulate synchronized start
    print("Starting matrix multiplication with synchronized threads...")
    for event in events:
        time.sleep(0.5)  # Delay to simulate order of execution
        event.set()  # Allow each thread to start

    # Wait for all threads to finish
    for future in futures:
        future.result()

print("Matrix multiplication completed. Verifying result...")

# Verification using single-threaded matrix multiplication for correctness
expected_result = np.dot(A, B)
if np.allclose(result, expected_result):
    print("The result is correct.")
else:
    print("There is an error in the computation.")
