import console
import ui
import objc_util
import cockpit_setup

def close_ui(sender):
	#print(sender)
	v.close()

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
			print("Found text field!")
			try: 
				form_valid &= sv.action(sv)
			except TypeError:
				pass				
	return form_valid
		
def parse_form(sender):
	print("Clicking this button will parse all of the form entrys and save them to the database!")
	# We only want to be able to do this once all of the forms entries 
	# are valid! Until then, the 'Save' button should be grayed out!
	if not all_valid(sender.superview):
		console.alert('Please finish filling out the form!','Check for blank fields and errors', 'OK',hide_cancel_button=True)
		return
	bike_data = BikeGeometry(int(main_view['stem_length'].text),
		int(main_view['stem_angle'].text), int(main_view['top_cap_stack'].text), 
		int(main_view['spacer_stack'].text), int(main_view['stem_stack'].text))
	# Now we need to put this data somewhere. Ideally, the cockpit data is associated with the bike geometry!
	
	close_ui(sender)
	
def load_cockpit_setup(sender):
	print("This would load the cockpit setup details (If empty, load blank form, otherwise load current details to edit).")
	cockpit_setup.load_view()
	print("cockpit setup loaded!")
			
		
v = ui.load_view()
objc_util.ObjCInstance(v['cockpit']).button().titleLabel().setLineBreakMode(0)
#v['save_btn'].enabled = False


v.present('sheet')




