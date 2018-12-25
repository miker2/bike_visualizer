# I need to turn this into a python object. It will contain all of the UI setup, all of the member
# data, etc.
# The object will then be fully self contained. It can be create from the interactive shell, and
# be responsible for producing all necessary data.

import console
import ui
from bike_geometry import CockpitConfig

class CockpitSetupView (ui.View):
	def __init__(self, **kwargs):
		self.v = ui.load_view('cockpit_setup.pyui')
		self.v.present('sheet')
		
		self.cockpit_data = None
		
	def close_ui(self,sender):
		#print(sender)
		self.v.close()
	
	def validate_data(self,sender):
		if len(sender.text) == 0:
			return False
		try:
			int(sender.text)
			sender.text_color = 'black'
			return True
		except ValueError:
			# Here is where we need to show a warning to the user!
			sender.text_color = 'red'
			return False
			
	def all_valid(self, view):
		# Walk through the view entrys and check that they are valid (if they are a TextField)
		print(view.subviews)
		form_valid = True
		for sv in view.subviews:
			if isinstance(sv, ui.TextField):
				print("Found text field '%s'!" % (sv.name))
				try: 
					form_valid &= sv.action(sv)
				except TypeError:
					pass				
		return form_valid
		
	def parse_form(self, sender):
		print("Clicking this button will parse all of the form entrys and save them to the database!")
		# We only want to be able to do this once all of the forms entries 
		# are valid! Until then, the 'Save' button should be grayed out!
		if not self.all_valid(self.v):
			console.alert('Please finish filling out the form!','OK')
			return
		self.cockpit_data = CockpitConfig(int(self.v['stem_length'].text),
			int(self.v['stem_angle'].text), int(self.v['top_cap_stack'].text), 
			int(self.v['spacer_stack'].text), int(self.v['stem_stack'].text))
		# Now we need to put this data somewhere. Ideally, the cockpit data is associated with a
		# BikeGeometry object!
		print(self.cockpit_data)
		print(repr(self.cockpit_data))
		print(self.cockpit_data.__dict__)
		# Just as a test, this works: cockpit_data.__dict__['stem_angle'] = 7
		print(self.cockpit_data.as_dict())
		print(self.cockpit_data.handlebar_offset(90))
								
		self.close_ui(sender)
		
		
def load_view():
  v = ui.load_view('cockpit_setup.pyui')
  v.present('sheet')
  return v

def close_ui(sender):
	#print(sender)
	sender.superview.close()

def validate_data(sender):
	if len(sender.text) == 0:
		return False
	try:
		int(sender.text)
		sender.text_color = 'black'
		return True
	except ValueError:
		# Here is where we need to show a warning to the user!
		sender.text_color = 'red'
		return False
		
def all_valid(view):
	# Walk through the view entrys and check that they are valid (if they are a TextField)
	print(view.subviews)
	form_valid = True
	for sv in view.subviews:
		if isinstance(sv, ui.TextField):
			print("Found text field '%s'!" % (sv.name))
			try: 
				form_valid &= sv.action(sv)
			except TypeError:
				pass				
	return form_valid
		
def parse_form(sender):
	print("Clicking this button will parse all of the form entrys and save them to the database!")
	# We only want to be able to do this once all of the forms entries 
	# are valid! Until then, the 'Save' button should be grayed out!
	main_view = sender.superview;
	if not all_valid(main_view):
		console.alert('Please finish filling out the form!','OK')
		return
	cockpit_data = CockpitConfig(int(main_view['stem_length'].text),
		int(main_view['stem_angle'].text), int(main_view['top_cap_stack'].text), 
		int(main_view['spacer_stack'].text), int(main_view['stem_stack'].text))
	# Now we need to put this data somewhere. Ideally, the cockpit data is associated with a
	# BikeGeometry object!
	print(cockpit_data)
	print(repr(cockpit_data))
	print(cockpit_data.__dict__)
	# Just as a test, this works: cockpit_data.__dict__['stem_angle'] = 7
	print(cockpit_data.as_dict())
	print(cockpit_data.handlebar_offset(90))
							
	close_ui(sender)
	
csv = CockpitSetupView()
print("closed the view")
print(csv.cockpit_data)