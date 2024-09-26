import multiprocessing
import numpy as np
import time

def worker_process(name, queue):
    """Function run by worker processes to perform complex NumPy tasks."""
    start_time = time.time()
    matrix_size = 5000  # Large size for increased computational complexity

    # Generate two large random matrices
    A = np.random.rand(matrix_size, matrix_size)
    B = np.random.rand(matrix_size, matrix_size)

    # Perform matrix multiplication
    C = np.dot(A, B)

    # Compute eigenvalues of the result
    eigenvalues = np.linalg.eigvals(C)

    # Compute matrix inversion (may be computationally intensive)
    try:
        C_inv = np.linalg.inv(C)
    except np.linalg.LinAlgError:
        C_inv = None  # Matrix is singular and cannot be inverted

    # Perform Singular Value Decomposition
    U, s, Vt = np.linalg.svd(C, full_matrices=False)

    # Compute determinant (may be zero for singular matrices)
    determinant = np.linalg.det(C)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Send the results back to the main process
    msg = (
        f"{name} Results:\n"
        f"- Sum of eigenvalues: {np.sum(eigenvalues):.2e}\n"
        f"- Determinant: {determinant:.2e}\n"
        f"- Sum of singular values: {np.sum(s):.2e}\n"
        f"- Inversion {'succeeded' if C_inv is not None else 'failed (singular matrix)'}\n"
        f"- Elapsed time: {elapsed_time:.2f} seconds"
    )
    queue.put(msg)
    queue.put(f"{name} done")

if __name__ == "__main__":
    # Create a queue to share messages between processes
    message_queue = multiprocessing.Queue()

    # Number of worker processes
    num_processes = 3

    # Create and start worker processes
    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(
            target=worker_process,
            args=(f"Process-{i+1}", message_queue)
        )
        processes.append(p)
        p.start()

    # Collect messages from workers
    finished_processes = 0
    while finished_processes < num_processes:
        msg = message_queue.get()
        print(f"\nMain process received:\n{msg}")
        if "done" in msg:
            finished_processes += 1

    # Wait for all worker processes to finish
    for p in processes:
        p.join()

    print("\nAll worker processes have finished.")
