import numpy as np
bar_array = np.array(range(1,20))
print(bar_array)
bar_array[:-1] = bar_array[1:]
bar_array[-1] = 20
print(bar_array)
bar_array[:-1] = bar_array[1:]
bar_array[-1] = 21
print(bar_array)
bar_array[:-1] = bar_array[1:]
bar_array[-1] = 22

print(bar_array)
# bar_array[:-1] = bar_array[1:]
# bar_array=bar_array.__lshift__(1)

# bar_array.
print(bar_array)
