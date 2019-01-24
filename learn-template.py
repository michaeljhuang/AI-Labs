from matplotlib import pyplot as plt
def f(x,y):
   return 6*x**2-7*x*y+4*y**2+32*x-16*y
def grad(x,y):
   return(-1*(12*x-7*y+32),-1*(-7*x+8*y-16))
def grad_descent(rate = .1):
   x = 0
   y = 0
   for i in range(1000):
       if(grad(x,y) == (0,0)):
           #print("break")
           return (x, y, f(x, y), i)
       (dx,dy)=grad (x,y)
       if(dx> 10000 or dy>10000):
           break
       x = x+dx*rate
       y = y+dy*rate
   return (x,y,f(x,y),500)# 1000 means it does not converge.
def main():
   x_series = []
   y_series = []
   for i in range(1,50):
       (x,y,z,count) = grad_descent(rate=i/100)
       if(count!= 1000):
           print(x,y,z)
       x_series.append(i/100)
       y_series.append(count)
   plt.plot(x_series, y_series)
   plt.show()
if __name__ == '__main__':
   main()
