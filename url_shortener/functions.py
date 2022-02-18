import random

def randb58str(length):
	return ''.join(random.choice('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
             for _ in range(length))
             
if __name__ == "__main__":
	print(randb58str(7))