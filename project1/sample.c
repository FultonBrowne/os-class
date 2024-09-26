#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

// Number of threads to create
#define NUM_THREADS 5

// Function to be executed by each thread
void* threadFunction(void* arg) {
    int thread_id = *((int*)arg);
    printf("Hello from thread %d!\n", thread_id);
    sleep(1); // Simulate some work being done
    printf("Goodbye from thread %d!\n", thread_id);
    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];
    int result;

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i + 1;
        result = pthread_create(&threads[i], NULL, threadFunction, &thread_ids[i]);
        if (result != 0) {
            printf("Error creating thread %d\n", i + 1);
            exit(1);
        }
    }

    // Wait for all threads to finish
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("All threads have finished.\n");
    return 0;
}
