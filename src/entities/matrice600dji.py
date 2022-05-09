import numpy as np
from sklearn.linear_model import LinearRegression

# The hovering time is based on flying at 10 m above sea level in a no-wind environment and landing with 10% battery level.

# battery TB47S
#payload = np.array([0.4, 0.9, 1.8, 6]).reshape((-1, 1))
#hovering_time = np.array([30,28,23,16])
# battery TB48S
payload = np.array([0.5, 0.9, 1.9, 5.5]).reshape((-1, 1))
hovering_time = np.array([35,34,29,18])

unit_consumption = 1/(hovering_time*60)
print(unit_consumption)


model = LinearRegression().fit(payload, unit_consumption)

q = model.intercept_
m = model.coef_
print('intercept:', q)
print('slope:', m)

check = hovering_time.reshape((-1, 1))*60 * (q + m*payload)
print(check)