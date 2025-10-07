
import time
import matplotlib.pyplot as plt


def buublesort(list):
    n=len(list)
    for i in range (n):
        print(f'{i}: Iteration')
        print(list)
        swapped=False
        for j in range (n-i-1):
            if list[j]>list[j+1]:
                list[j],list[j+1]=list[j+1],list[j]
                swapped=True
                print(f'swapped,j ={swapped,j}: {list}')
                #time.sleep(2)
        if not swapped:
            print('list already ordered')
            break

list=[5,10,12,20,18,15,1,8,23]
#list=[10,20,30,40,50,60]
buublesort(list)
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Mi gráfico")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()