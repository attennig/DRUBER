from time import process_time

# assigning n = 50
n = 500000

# Start the stopwatch / counter
t1_start = process_time()

for i in range(n):
    print(i, end=' ')

print()

# Stop the stopwatch / counter
t1_stop = process_time()

print("Elapsed time:", t1_stop, t1_start)

print("Elapsed time during the whole program in seconds:",
      t1_stop - t1_start)