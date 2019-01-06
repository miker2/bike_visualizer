# New idea! We'll have one object (BikeGeometry) that will store things like name, size, etc, then the
# BikeGeometry object will contain two other objects (frame geometry & cockpit geometry) which will
# encapsulate the other bits. This way when the user goes to add a new bike type, all of the data
# can be collected at once, making things a bit easier. This also simplifies some of the form
# parsing by separating out string data from geometry (numeric) data.



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

import dialogs
import json
import math
import sys
from point import Point

DEG2RAD = math.pi/180

def bikeGeometryFromJson(jstr):
	jdict = json.loads(jstr)
	print(jdict)
	newClass = getattr(sys.modules[__name__],jdict['type'])
	print(newClass)
	return newClass.fromDict(jdict['data'])
	

class BikeInfo (object):
	""" This is a class for holding bike related information (name, size, etc) as well as a
	    FrameGeometry object and a CockpitGeometry object. """

	def __init__(self):
		# Default some member variables
		self.bike_name = "unknown"
		self.frame_size = 'L' # numeric sizes are also acceptable (i.e. 58cm)
		self.wheel_size = '700c'

		self.frame = FrameGeometry()
		self.cockpit = CockpitGeometry();

class BikeGeometry (object):
	""" Base class for bike info objects (FrameGeometry & CockpitGeometry). This adds a function that
	    makes it easy to get the class member variables as a dictionary. """
	def __init__(self):
		pass
		
	@property
	def TYPE(self):
		return self.__class__.__name__
		
	def as_dict(self):
		return { key:value for key, value in self.__dict__.items() if not key.startswith('__') and \
			not callable(key)}
			
	def toJson(self):
		return json.dumps({'type': self.TYPE, 'data': self.as_dict()})
		
	@classmethod
	def fromDict(cls, data):
		#print('data is {}'.format(data))
		obj = cls()
		for key, vals in data.items():
			setattr(obj, key, vals)
		#print('obj.__dict__ = {}'.format(obj.__dict__))
		return obj
		
	@classmethod
	def fromForm(cls):
		obj = cls()
		form_dict = [{'type': 'number', 'key': key, 'title': key.replace('_',' ').capitalize()} for key \
			in obj.__dict__.keys() if not key.startswith('__') and not callable(key)]
		print(obj)
		print(obj.TYPE)
		print(form_dict)
		vals = dict() #dialogs.form_dialog(obj.TYPE, form_dict)
		print(vals)
		for key, val in vals.items():
			setattr(obj, key, float(val))
		print(obj)
		return obj

class FrameGeometry (BikeGeometry):
	""" This is a basic storage container for bicycle geometry information. It 
	    will be used calcuate various points on a bicycle in order to draw the 
	    geometry of the bicycle. It can also be used in conjunction with the 
	    CockpitGeometry class in order to determine the stack/reach of various
	    points on the cockpit of the bicycle relative to the bottom bracket."""
	def __init__(self):
		# My bike geometry class needs the following properties:
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
		print('class name = {}'.format(self.TYPE))
	
class CockpitGeometry (BikeGeometry):
	"""  """
	def __init__(self, sl=110, sa=-6, tch=15, sph=20, sh=40):
		self.stem_length = sl;
		self.stem_angle = sa;
		self.top_cap_stack = tch;
		self.spacer_stack = sph;
		self.stem_stack = sh;
		print('class name = {}'.format(self.TYPE))
		
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

class GeometryMath (object):
	
	def __init__(self, bike_geometry):
		self.geometry = bike_geometry;
		self.update()
		print(self)
		
	def update(self):
		gm = self.geometry
		self.rear_axle = Point(-math.sqrt(gm.chainstay_length**2 + gm.bb_drop**2),
													 gm.bb_drop);
		self.stack = math.sin(gm.head_tube_angle*DEG2RAD) * (gm.head_tube_length + gm.fork_length - \
			gm.fork_offset * math.cos(gm.head_tube_angle * DEG2RAD)) + gm.bb_drop
		self.reach = gm.top_tube_length - self.stack * math.tan((90 - gm.seat_tube_angle) * DEG2RAD)
		self.bottom_bracket = Point(0, 0)
		self.front_axle = Point(gm.fork_offset / math.cos((90 - gm.head_tube_angle) * DEG2RAD) + \
			(gm.head_tube_length + gm.fork_length - gm.fork_offset * math.tan((90 - gm.head_tube_angle) * \
			DEG2RAD)) * math.cos(gm.head_tube_angle * DEG2RAD) + self.reach,
		   gm.bb_drop)
		self.rear_axle = Point(-math.sqrt(gm.chainstay_length**2 - gm.bb_drop**2),
				       gm.bb_drop)
		self.fork_crown = Point(self.reach+gm.head_tube_length*math.cos(gm.head_tube_angle * DEG2RAD),
					self.stack-gm.head_tube_length*math.sin(gm.head_tube_angle * DEG2RAD))
		self.head_tube_crown = Point(self.reach, self.stack)
		self.top_tube_end = self.head_tube_crown - Point(gm.top_tube_length, 0)
		self.seat_tube_junction = Point(-gm.seat_tube_length*math.cos(gm.seat_tube_angle * DEG2RAD),
						 gm.seat_tube_length*math.sin(gm.seat_tube_angle * DEG2RAD))

	def __str__(self):
		_str = "{}:\n".format(self.__class__.__name__)
		for key, val in self.__dict__.items():
			if not key.startswith('__') and not callable(key):
				_str += "\t{}: {}\n".format(key, val)
		return _str
