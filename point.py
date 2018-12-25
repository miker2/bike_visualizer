import cmath
from typing import Tuple

class Point:
	def __init__(self, x:float, y:float):
		self._x = x
		self._y = y
	
	@classmethod
	def fromTuple(cls, _pt: Tuple[float, float]):
		return cls(_pt[0],_pt[1])
	
	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
	
	@property
	def pt(self):
		return self.asTuple()	
				
	def asTuple(self) -> Tuple[float, float]:
		return (self.x, self.y)
		
	def rotate(self, angle):
		ct = cmath.cos(angle)
		st = cmath.sin(angle)
		return Point(ct * self.x - st * self.y, st * self.x + ct * self.y)

	def __add__(self, point):
		return Point(self.x + point.x, self.y + point.y) 
		
	def __sub__(self, point):
		# Implement the minus operator as an addition plus unary minus.
		return self.__add__(point.__neg__())
		
	def __neg__(self):
		return Point(-self.x, -self.y)

	def __str__(self):
		return "(%-0.4f, %-0.4f)" % (self.x, self.y)

