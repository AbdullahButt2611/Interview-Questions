# Process vs Thread

Processes and threads are fundamental concepts in operating systems and concurrent programming. They both refer to the execution of code, but they have distinct characteristics.

### Process

-  **Isolation:** Each process runs in its own isolated memory space. One process cannot directly access the memory of another process. This provides a high level of security and stability because if one process fails, it does not affect others.
- **Resource Overhead:** Processes have more overhead in terms of system resources. Each process has its own copy of the program code, data, and system resources.
- **Communication:** Inter-process communication (IPC) is required for processes to communicate with each other. This can be achieved through mechanisms like pipes, sockets, or message passing.
- **Creation Overhead:** Creating a new process is typically more resource-intensive than creating a thread.
- **Fault Isolation:** If one process crashes, it does not affect the others.

### Thread

- **Shared Memory:** Threads within the same process share the same memory space. They can directly access and modify data in the shared memory.
- **Resource Efficiency:** Threads are more lightweight compared to processes. They share resources such as code, data, and file descriptors.
- **Communication:** Threads within the same process can communicate more easily since they share the same memory space. However, caution must be taken to avoid race conditions and other synchronization issues.
- **Creation Overhead:** Creating a new thread is generally faster and requires less overhead compared to creating a new process.
- **Fault Impact:** If one thread encounters an issue (like a segmentation fault), it can potentially crash the entire process, affecting all threads within it.

### Key Points

- Processes provide a higher level of isolation and security but come with more overhead.
- Threads are more lightweight and share resources but require careful synchronization to avoid conflicts.
- Both processes and threads are used to achieve parallelism and concurrency in programs.
- The choice between processes and threads depends on the specific requirements of the application, and sometimes a combination of both is used to take advantage of their respective strengths.