import numpy as np
import matplotlib.pyplot as plt

# Параметры
region_size = (20, 20)
temp_min, temp_max = -20, 30

np.random.seed(0) 
temperature_data = np.random.uniform(temp_min, temp_max, region_size)

# Тепловая карта
plt.figure(figsize=(8, 6))
plt.imshow(temperature_data, cmap='coolwarm', origin='lower')

cbar = plt.colorbar()
cbar.set_label('Температура (°C)')

plt.title('Тепловая карта температур')
plt.xlabel('Координата X')
plt.ylabel('Координата Y')
plt.xticks(range(region_size[1]))
plt.yticks(range(region_size[0]))

plt.show()
