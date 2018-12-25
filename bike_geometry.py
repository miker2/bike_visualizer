# Some thoughts:
# The basic idea here is that we'll have a way of storing various types of bike geometry.
# We'll also be able to store a cockpit configuration with a specific bike geometry, but they should
# be stored separately.
# We need some sort of UI that allows us to enter new bike geometry parameters
# We need a "math" engine that calculates points in space based on the bike geometry
# Perhaps we also want a storage container for seatpost & saddle information
# We need a UI that will draw the various bike geometries, and allow the user to compare them (with 
# options on how to align two different geometries, e.g. centered at BB, or wheels on ground + 
# centered fore/aft or centered at rear axle or whatever else I can think of)
# Really nice would be a utility that would allow the user to calculate certain properties (like
# change in stack/reach based on stem choice, or what's the best space/stem angle/stem length combo
# in order to achieve a desired stack/reach)
# We will need some tools like in my spreadsheet that allow for the calculation of fork properties
# if other geometric properties are known (wheelbase, stack, trail, etc)

import math

DEG2RAD = math.pi/180

class BikeInfo (object):
	def __init__(self):
		pass
		
	def as_dict(self):
		return { key:value for key, value in self.__dict__.items() if not key.startswith('__') and \
			not callable(key)}

class BikeGeometry (BikeInfo):
	""" This is a basic storage container for bicycle geometry information. It 
	    will be used calcuate various points on a bicycle in order to draw the 
	    geometry of the bicycle. It can also be used in conjunction with the 
	    CockpitConfig class in order to determine the stack/reach of various 
	    points on the cockpit of the bicycle relative to the bottom bracket."""
	def __init__(self):
		# I forget how to code in python, but I'll figure it out again pretty soon
		# My bike geometry class needs the following properties:
		self.bike_name = ""
		self.frame_size = 58;
		self.wheel_size = '700c';
		self.bb_drop = 0
		self.fork_length = 0
		self.fork_offset = 0
		self.top_tube_length = 0
		self.head_tube_length = 0
		self.head_tube_angle = 0
		self.seat_tube_angle = 0
		self.chainstay_length = 0
		self.seat_tube_length = 0
		self.wheelbase_spec = 0
	
class CockpitConfig (BikeInfo):
	"""  """
	def __init__(self, sl, sa, tch, sph, sh=40):
		self.stem_length = sl;
		self.stem_angle = sa;
		self.top_cap_stack = tch;
		self.spacer_stack = sph;
		self.stem_stack = sh;
		
	@property
	def stack(self):
		return 0.5 * self.stem_stack + self.top_cap_stack + self.spacer_stack
		
	def handlebar_offset(self, hta):
		stem_offset = Point(self.stem_length, 0).rotate(self.stem_angle * DEG2RAD)
		ho_zero = Point(0, self.stack) + stem_offset
		return ho_zero.rotate((90-hta)*DEG2RAD)
	
	def __repr__(self):
		return "<%s: stem_length=%d, stem_angle=%d, stem_stack=%d, top_cap_stack=%d, spacer_stack=%d>" % (
			self.__class__.__name__, self.stem_length, self.stem_angle, self.stem_stack, self.top_cap_stack, 
			self.spacer_stack)
			
	def __str__(self):
		return "Cockpit setup:\n  stem length: %d mm\n  stem angle: %d deg\n  stack: %d mm" % (
			self.stem_length, self.stem_angle, self.stack)

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

class GeometryMath (object):
	
	def __init__(self, bike_geometry):
		self.geometry = bike_geometry;
		
	def update(self):
		gm = self.geometry
		self.rear_axle = Point(-math.sqrt(gm.chainstay_length**2 + gm.bb_drop**2),
													 gm.bb_drop);
		self.stack = math.sin(gm.head_tube_angle*DEG2RAD) * (gm.head_tube_length + gm.fork_length - \
			gm.fork_offset * math.cos(gm.head_tube_angle * DEG2RAD)) + gm.bb_drop
		self.reach = gm.top_tube_length - self.stack * math.tan((90 - gm.seat_tube_angle) * DEG2RAD)
		self.front_axle = Point(gm.fork_offset / math.cos((90 - gm.head_tube_angle) * DEG2RAD) + \
			(gm.head_tube_length + gm.fork_length - gm.fork_offset * math.tan((90 - self.head_tube_angle) * \
			DEG2RAD)) * math.cos(self.head_tube_angle * DEG2RAD) + self.reach,
		   gm.bb_drop)
		   

		