#include <stdio.h>
#include <stdlib.h>

int global_var = 42;  // Static/global variable

void allocateMemory() {
    int *heap_var = (int *)malloc(sizeof(int));  // Allocating memory on the heap
    *heap_var = 100;

    printf("Heap variable address: %p, value: %d\n", (void *)heap_var, *heap_var);

    free(heap_var);  // Free the allocated memory
}

void functionStackExample() {
    int stack_var = 50;  // Local variable on the stack
    printf("Stack variable address: %p, value: %d\n", (void *)&stack_var, stack_var);
}

int main() {
    int local_var = 10;  // Local variable on the stack

    printf("Global variable address: %p, value: %d\n", (void *)&global_var, global_var);
    printf("Local variable address: %p, value: %d\n", (void *)&local_var, local_var);

    allocateMemory();
    functionStackExample();

    return 0;
}
