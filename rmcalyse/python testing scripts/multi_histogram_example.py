import random
import numpy as np
import matplotlib.pyplot as plt

x = [random.gauss(3, 1) for _ in range(400)]
y = [random.gauss(4, 2) for _ in range(400)]

bins = np.linspace(-10, 10, 100)

plt.hist(x, bins, alpha=0.5, label='x')
plt.hist(y, bins, alpha=0.5, label='y')
plt.legend(loc='upper left')
plt.title('Title 1')
plt.title('Title 2')
plt.show()
