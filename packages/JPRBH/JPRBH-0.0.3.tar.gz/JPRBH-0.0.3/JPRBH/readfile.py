def read():
	with open('data.txt', 'r') as f:
		return f.readlines()

def main():
	read()

if __name__ == "__main__":
	main()

