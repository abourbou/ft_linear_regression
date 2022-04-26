import csv

def main():
	file = open('theta_value.csv')
	csvreader = csv.reader(file)
	arr = []
	for row in csvreader:
		arr.append(row)
	if (len(arr) != 2 or arr[0] != ['theta0', 'theta1'] or len(arr[1]) != 2):
		print("theta_value.csv is corrupted")
		return 1
	theta0 = float(arr[1][0])
	theta1 = float(arr[1][1])
	milleage = float(input("What is the milleage?\n"))
	print("the estimate price is : "+ str(theta0 + theta1 * milleage))

if __name__ == '__main__':
	main()