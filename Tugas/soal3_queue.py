from llistqueue import Queue

values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
    elif i % 4 == 0:
        values.dequeue()

# Tampilkan hasil
result = []
while not values.isEmpty():
    result.append(values.dequeue())

print("Isi Queue (front → rear):", result)
