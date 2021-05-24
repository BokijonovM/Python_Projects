import math

"""
Bokijonov Mukhsinjon 52336
Task 4

Please first read README.txt file
Please first read README.txt file
Please first read README.txt file
Please first read README.txt file
Please first read README.txt file
Please first read README.txt file
"""


class BList(object):
	expr = None
	brackets_list = []

	def __init__(self, expression):
		self.expr = expression
		self.get_brakcets_list()
		self.match_brackets()

	#indexs all brackets in expression
	def get_brakcets_list(self):
		self.brackets_list = []
		for c in range(0, len(self.expr)):
			if self.expr[c] == "(" or self.expr[c] == ")":
				self.brackets_list.append((self.expr[c], c, None))
		return self.brackets_list

	#organize brackets list to so corosponding brackets are matched 
	def match_brackets(self):
		focus = None
		c = 0
		while c < len(self.brackets_list):
			if self.brackets_list[c][0] == "(" and self.brackets_list[c][2] == None:
				focus = c
			if self.brackets_list[c][2] == None and self.brackets_list[c][0] == ")" and focus != None:
				self.brackets_list[focus] = ("(", self.brackets_list[focus][1], self.brackets_list[c][1])
				self.brackets_list[c] = (")", self.brackets_list[c][1], self.brackets_list[focus][1])
				focus = None
				c = 0
				continue
			c+=1
		return self.brackets_list

	#get a matching closing bracket for any given opening bracket 
	def get_match(self, c):
		for x in self.brackets_list:
			if x[2] == c:
				return x[1]
		return None


class Solve(object):
	variables = []
	def __init__(self, expr):
		print("A:", self.analyize_expression(expr))

	def analyize_expression(self, expr):
		for t in expr.split(" "):
			if len(t) == 1:
				try:
					float(t)
				except ValueError:
					if t not in ["(", ")", "^", "*", "/", "+", "-"] and t not in variables:
						self.declare_variable(t)
		if "(" in expr:
			while "(" in expr:
				try:
					for c in range(0, len(expr)):
							if expr[c] == "(":
								br = BList(expr)
								expr = expr.replace(
									expr[c:br.get_match(c) + 1],
									self.analyize_expression(expr[c +1:br.get_match(c)]),
									1)
				except IndexError:
					continue
		expr = self.solve_expression(expr)
		return expr

	def declare_variable(self, var):
		print(var, "=", end = "")
		self.variables.append((var, float(input(""))))

	def solve_expression(self, expr):
		terms = expr.split()
		while len(terms) > 1:
			for t in range(0, len(terms)):
				for v in self.variables:
					if terms[t] == v[0]:
						terms[t] = v[1]
			if "pi" in terms:
				for t in range(0, len(terms)):
					if terms[t] == "pi":
						terms[t] = str(math.pi)
			for t in range(0, len(terms)):
				try:
					if "tan" in terms[t] or "cos" in terms[t] or "sin" in terms[t] or "atan" in terms[t] or "acos" in terms[t] or "asin" in terms[t]:
						self.trig(terms, t)
				except IndexError:
					break
			if "^" in terms:
				for t in range(0, len(terms)):
					try:
						if terms[t] == "^":
							self.power(terms, t)
					except IndexError:
						break
			for t in range(0, len(terms)):
				try:
					#root, 2root, 3root
					if terms[t].find("root") != -1:
						self.root(terms, t)
				except IndexError:
					break
			if "*" in terms or "/" in terms:
				for t in range(0, len(terms)):
					try:
						if terms[t] == "*":
							self.times(terms, t)
						elif terms[t] == "/":
							self.obelus(terms, t)
					except IndexError:
						break
			last_term_number = None
			for t in range(0, len(terms)):
				try:
					float(terms[t])
					if last_term_number:
						self.times(terms, t)
					else:
						last_term_number = True
				except ValueError:
					last_term_number = False
			if "+" in terms or "-" in terms:
				for t in range(0, len(terms)):
					try:
						if terms[t] == "+":
							self.plus(terms, t)
						elif terms[t] == "-":
							self.minus(terms, t)
					except IndexError:
						break
		return " ".join(terms)

	def plus(self, terms, t):
		terms[t - 1] = str(float(terms[t - 1]) + float(terms[t + 1]))
		terms.pop(t)
		terms.pop(t)

	def minus(self, terms, t):
		terms[t - 1] = str(float(terms[t - 1]) - float(terms[t + 1]))
		terms.pop(t)
		terms.pop(t)

	def power(self, terms, t):
		terms[t - 1] = str(float(terms[t - 1]) ** float(terms[t + 1]))
		terms.pop(t)
		terms.pop(t)

	def times(self, terms, t):
		try:
			#multiply adjacent factors
			float(terms[t])
			terms[t - 1] = str(float(terms[t - 1]) * float(terms[t]))
			terms.pop(t)
		except ValueError:
			#multiply factors separated by '*'
			terms[t - 1] = str(float(terms[t - 1]) * float(terms[t + 1]))
			terms.pop(t)
			terms.pop(t)

	def obelus(self, terms, t):
		terms[t - 1] = str(float(terms[t - 1]) / float(terms[t + 1]))
		terms.pop(t)
		terms.pop(t)

	def root(self, terms, t):
		if terms[t] == "root":
			terms[t] = str(float(terms[t + 1]) ** (1 / 2))
		else:
			terms[t] = str(float(terms[t + 1]) ** (1 / float(terms[t].replace("root", ""))))
		terms.pop(t + 1)

	def trig(self, terms, t):
		if terms[t] == "tan":
			terms[t] = str(math.tan(float(terms[t + 1])))
		elif terms[t] == "atan":
			terms[t] = str(math.atan(float(terms[t + 1])))
		elif terms[t] == "cos":
			terms[t] = str(math.cos(float(terms[t + 1])))
		elif terms[t] == "acos":
			terms[t] = str(math.acos(float(terms[t + 1])))
		elif terms[t] == "sin":
			terms[t] = str(math.sin(float(terms[t + 1])))
		elif terms[t] == "asin":
			terms[t] = str(math.asin(float(terms[t + 1])))
		terms.pop(t + 1)

while True:
	Solve(input("Input: "))