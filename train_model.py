
import csv
import matplotlib.pyplot as plt
import math


def csv_to_array():
	file = open('data.csv')
	csvreader = csv.reader(file)
	arr = []
	for row in csvreader:
		arr.append(row)
	arr.pop(0)
	return arr

def rescale(arr):
	if len(arr) < 1:
		return
	min = arr[0];
	max = arr[0];
	for elem in arr:
		if (elem > max):
			max = elem
		elif (elem < min):
			min = elem
	for i in range (0, len(arr)):
		arr[i] = (arr[i] - min) / (max - min)
	return ([min, max])

def descale(arr, min, max):
	if len(arr) < 1:
		return
	diff = max - min
	for i in range (0, len(arr)):
		arr[i] = arr[i] * diff + min

def theta_to_file(theta0, theta1):
	file = open('theta_value.csv', 'w')
	csvwriter = csv.writer(file)
	csvwriter.writerow(["theta0", "theta1"])
	csvwriter.writerow([str(theta0), str(theta1)])

def rmse_coeff(theta0, theta1, arr_km, arr_price):
	sqr_error = 0
	for i in range (0, len(arr_km)):
		sqr_error += (arr_price[i] - (theta0 + theta1 * arr_km[i]))**2
	sqr_error /= len(arr_km)
	rmse = math.sqrt(sqr_error)
	return (float(rmse))

def show(arr_km, arr_price, theta0, theta1, rmse):
	plt.plot(arr_km, arr_price, 'o', color='blue')
	km_start = 290000.0
	km_end = 10000.0
	estimat1 = [km_start, km_end]
	estimat2 = [theta0 + theta1 * km_start, theta0 + theta1 * km_end]
	plt.plot(estimat1, estimat2, color='red')
	plt.xlabel("km")
	plt.ylabel("price")
	plt.title('Linear Regression', fontsize=16)
	plt.text(200000,8000,'RMSE : ' + str(rmse))
	plt.show()

def train(arr_km, arr_price):
	theta0 = 0
	theta1 = 0
	[min_km, max_km] = rescale(arr_km)
	[min_price, max_price] = rescale(arr_price)

	#learning algorithm
	learning_rate = 0.1
	inv_m = 1 / float(len(arr_km))
	for i in range (0, 10000):
		estimate_price = map(lambda km: theta0 + theta1 * km, arr_km)
		zip_price_estimation = zip(estimate_price, arr_price)
		diff = list(map(lambda x: x[0] - x[1], zip_price_estimation))
		zip_km_diff = list(zip(arr_km, diff))
		diff_mult_km = list(map(lambda tup: tup[0] * tup[1], zip_km_diff))
		tmp_theta0 = learning_rate * inv_m * sum(diff)
		tmp_theta1 = learning_rate * inv_m * sum(diff_mult_km)
		theta0 -= tmp_theta0
		theta1 -= tmp_theta1

	#descale array
	descale(arr_km, min_km, max_km)
	descale(arr_price, min_price, max_price)
	diff_price = max_price - min_price
	diff_km = max_km - min_km
	#descale theta
	theta0 = theta0 * diff_price + min_price - theta1 / diff_km * min_km * diff_price
	theta1 = theta1 / diff_km * diff_price

	#modify theta_value.csv
	theta_to_file(theta0, theta1)
	#compute RMSE
	rmse = rmse_coeff(theta0, theta1, arr_km, arr_price)
	show(arr_km, arr_price, theta0, theta1, rmse)

def main():
	arr = csv_to_array()
	arr_km, arr_price = [], []
	for elem in arr:
		arr_km.append(float(elem[0]))
		arr_price.append(float(elem[1]))
	train(arr_km, arr_price)

if __name__ == '__main__':
	main()