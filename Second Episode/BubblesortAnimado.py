import matplotlib.pyplot as plt
import matplotlib.animation as animation

def bubble_sort_visual(arr):
    n = len(arr)
    states = [arr.copy()]  # Save initial state
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                states.append(arr.copy())
        if not swapped:
            break
    return states

# Example data
data = [5,10,12,20,18,15,1,8,23]
states = bubble_sort_visual(data.copy())

fig, ax = plt.subplots()
bars = ax.bar(range(len(data)), states[0])

def update(frame):
    for bar, h in zip(bars, states[frame]):
        bar.set_height(h)
    ax.set_title(f"Step {frame+1}")
    return bars
ani = animation.FuncAnimation(fig, update, frames=len(states), blit=False, repeat=False,interval=1000 )
plt.show()