class Point:
	def __init__(self, x, y):
		self._x = x
		self._y = y
	
	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
		
	@property
	def pt(self):
		return (self.x, self.y)
		
	def rotate(self, angle):
		ct = math.cos(angle)
		st = math.sin(angle)
		return Point(ct * self.x - st * self.y, st * self.x + ct * self.y)

	def __add__(self, point):
		return Point(self.x + point.x, self.y + point.y) 

	def __str__(self):
		return "(%-0.4f, %-0.4f)" % (self.x, self.y)
