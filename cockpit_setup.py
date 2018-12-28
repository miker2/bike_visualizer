import console
import ui
from bike_geometry import CockpitConfig
from point import Point

class CockpitSetupView (ui.View):
	def __init__(self, **kwargs):
		super(CockpitSetupView, self).__init__(kwargs)
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

		self.cockpit_data = CockpitConfig()
		for key in self.cockpit_data.as_dict().keys():
			setattr(self.cockpit_data, key, int(self.v[key].text))
		# Now we need to put this data somewhere. Ideally, the cockpit data is associated with a
		# BikeGeometry object!
		print(self.cockpit_data)
		print(repr(self.cockpit_data))
		print(self.cockpit_data.__dict__)
		# Just as a test, this works: cockpit_data.__dict__['stem_angle'] = 7
		print(self.cockpit_data.as_dict())
		print(self.cockpit_data.handlebar_offset(90))
		
		print(self.cockpit_data.toJson())
								
		self.close_ui(sender)

if __name__ == '__main__':
	csv = CockpitSetupView()
	print("closed the view")
	print(csv.cockpit_data)
