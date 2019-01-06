import console
import ui
import objc_util
from bike_geometry import FrameGeometry, GeometryMath
from cockpit_setup import CockpitSetupView

class FrameGeometryForm (ui.View):
	def __init__(self, **kwargs):
		super(FrameGeometryForm, self).__init__(**kwargs)
		self.v = ui.load_view()
		objc_util.ObjCInstance(self.v['cockpit']).button().titleLabel().setLineBreakMode(0)
		self.v.present('sheet')
		
		self.bike_geometry = None
		
	def close_ui(self, sender):
		self.v.close()

	def validate_data(self, sender):
		if len(sender.text) == 0:
			return False
		try:
			float(sender.text)
			sender.text_color = 'black'
			return True
		except ValueError:
			# Here is where we need to show a warning to the user!
			sender.text_color = 'red'
			return False
			
	def not_empty(self, sender):
		if len(sender.text) > 0:
			return True
		else:
			return False
			
	def all_valid(self, view):
		# Walk through the view entrys and check that they are valid (if they are a TextField)
		print(view.subviews)
		form_valid = True
		for sv in view.subviews:
			if isinstance(sv, ui.TextField):
				print("Found text field!")
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
			console.alert('Please finish filling out the form!','Check for blank fields and errors', 'OK',
				hide_cancel_button=True)
			return
		bike_data = FrameGeometry()
		# NOTE: I need to figure out how to deal with converting the numbers to actual ints while leaving
		# attributes that could be converted to ints (i.e. frame_size) as strings.
		for key in bike_data.as_dict().keys():
			try:
				val = float(self.v[key].text)
			except ValueError:
				val = self.v[key].text
			setattr(bike_data, key, val)

		print(bike_data.__dict__)
		#print(self.csv.cockpit_data)
		print(bike_data.toJson())
		self.close_ui(sender)
		GeometryMath(bike_data)
		
	def load_cockpit_setup(self, sender):
		print("This would load the cockpit setup details (If empty, load blank form, otherwise load " \
			"current details to edit).")
		selv.csv = CockpitSetupView()
		print("cockpit setup loaded!")

FrameGeometryForm()
