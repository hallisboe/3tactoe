from queue import Queue
from random import shuffle

DATA = {}

def kill(b):
	l = [[int(''.join(b[:9]), 2), int(b[27], 2)], [int(''.join(b[9:18]), 2), int(b[28], 2)], [int(''.join(b[18:27]), 2), int(b[29], 2)]]
	for n in range(3):
		if l[n][1] == 1:
			l[n][0] = 0
	a = ''.join([str(i[1]) for i in l]) + b[30]
	return list('{0:09b}'.format(l[0][0]) + '{0:09b}'.format(l[1][0]) + '{0:09b}'.format(l[2][0]) + '{0:04b}'.format(int(a, 2)))

def move(b, m):
	n, x, y = m
	s = list(reversed('{0:031b}'.format(b | (2 ** ((n * 3 * 3) + (y * 3) + x)))))
	if(s[30] == '0'):
		s[30] = '1'
	else:
		s[30] = '0'
	for n in [i - 27 for i in [27, 28, 29] if s[i] == '0']:
		l, r = True, True
		for y_x in range(3): 
			x, y = True, True
			for x_y in range(3):
				if(s[(n * 3 * 3) + (y_x * 3) + x_y] == '0'): 
					x = False
				if(s[(n * 3 * 3) + (x_y * 3) + y_x] == '0'): 
					y = False

			if(y or x):
				s[n + 27] = '1'
				s = kill(s)
			if(s[(n * 3 * 3) + (y_x * 3) + y_x] == '0'): 
				l = False
			if(s[(n * 3 * 3) + (y_x * 3) + 2 - y_x] == '0'): 
				r = False
		if(l or r):
			s[n + 27] = '1'
			s = kill(s)


	return int(''.join(reversed(s)), 2)


def display(b):
	s = list(reversed('{0:031b}'.format(b)))
	print('Turn: {}'.format(s[30]))
	for n in range(3):
		print('Board {}:'.format(n + 1))
		for y in range(3):
			output = ''
			for x in range(3):
				output += s[(n * 3 * 3) + (y * 3) + x] + ' '
			print(output + '\n')
	print('Dead: {} {} {}'.format(s[27], s[28], s[29]))


def possible(b):
	s = list(reversed('{0:031b}'.format(b)))
	p = []
	for n in [i - 27 for i in [27, 28, 29] if s[i] == '0']:
		for y in range(3):
			for x in range(3):
				if(s[(n * 3 * 3) + (y * 3) + x] == '0'): 
					p.append([n, x, y]) 
	return p

def value(node, alpha, beta, player, depth):
        if len(node.children) == 0:
            return node.value()
       	if depth == 12:
       		return 0
        if player:
            v = -2;
            for n in node.children:
                v = max(v, value(DATA[n], alpha, beta, False, depth + 1))
                if v > alpha:
                    alpha = v
                if beta <= alpha:
                    break
            return alpha;
        else:
            v = 2;
            for n in node.children:
                v = min(v, value(DATA[n], alpha, beta, True, depth + 1))
                if(v < beta):
                    beta = v
                if (beta <= alpha):
                    break
            return beta;

    

class Node:
	def __init__(self, board):
		self.board = board
		self.children = []

	def expand(self):
		s = '{0:031b}'.format(self.board)
		if len([i for i in [1, 2, 3] if s[i] == '0']) > 0:
			for m in possible(self.board):
				b = list(reversed('{0:031b}'.format(move(self.board, m))))
				

				# Rotate boards
				c = [[0, 1, 3], [1, 2, 5], [5, 7, 8], [3, 6, 7]]
				r = [2, 5, 8, 1, 4, 7, 0, 3, 6]

				for n in range(3):
					if int(''.join(b[n * 9 : 9 + 9 * n]), 2) == 0:
						continue
					v = []
					for N, u in enumerate(c):
						v.append([0, 0, 0, 0])
						for i, corner in enumerate(u):
							v[N][i] += 1 if b[n * 9 + corner] == '1' else 0
					v = [sum(i) for i in v]
					to = v.index(max(v))
					for _ in range(to):
						old = list(b[(n * 9):(9 + n * 9)])
						for element in range(9):
							b[element + n * 9] = old[r[element]]

				l = [[int(''.join(b[:9]), 2), int(b[27], 2)], [int(''.join(b[9:18]), 2), int(b[28], 2)], [int(''.join(b[18:27]), 2), int(b[29], 2)]]
				# Sort boards
				for n in range(2):
					if l[n][1] == 1:
						continue
					for k in range(n + 1, 3):
						if l[k][1] == 1:
							continue
						if l[n] < l[k]:
							temp = list(l[n])
							l[n] = list(l[k])
							l[k] = temp

				a = ''.join([str(i[1]) for i in l]) + b[30]
				d = ''.join(list(reversed('{0:09b}'.format(l[0][0]) + '{0:09b}'.format(l[1][0]) + '{0:09b}'.format(l[2][0]) + '{0:04b}'.format(int(a, 2)))))
				b = int(d, 2)
				if not b in DATA:
					n = Node(b)
					DATA[n.board] = n
					queue.put(n)
				self.children.append(b)

	def value(self):
		if '{0:031b}'.format(self.board)[0] == '0':
			return 1
		else:
			return -1

BASE = int('0000000000000000000000000000000', 2) 
display(BASE)
root = Node(BASE)
queue = Queue()
queue.put(root)

#root.expand()


n = 0
prev = 1
while not queue.empty():
	queue.get().expand()
	if n % 10000 == 0:
		print('{} of {} done. In queue: {}. Average BF: {}'.format(n, len(DATA), queue.qsize(), 1 +(queue.qsize() - prev) / 10000))
		prev = queue.qsize() 
	n += 1
print('{} of {} done. In queue: {}. Average BF: {}'.format(n - 1, len(DATA), queue.qsize(), 1 +(queue.qsize() - prev) / 10000))

RESULT = {}
for i, c in enumerate(root.children):
	if not c in RESULT:
		RESULT[c] = value(DATA[c], -1000, 1000, '{0:031b}'.format(DATA[c].board), 0)
		print('{} of {}'.format(i + 1, len(root.children)))
	else:
		print('{} of {}'.format(i + 1, len(root.children)))

print(RESULT)


