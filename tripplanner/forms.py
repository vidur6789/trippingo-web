#from bootstrap_datepicker_plus import DatePickerInput
from django import forms


Traveller_Type_C	= 	[	
						("Family"	, 	"Family"),
						("Couple" 	, 	"Couple"),
						("Business"	, 	"Business"),
						("Friends"	, 	"Friends"),
						("Solo"		, 	"Solo")
						]


Category_C 			=	[		
						("Landmark"		,	"Landmarks"),
						("Shopping"		, 	"Shopping"),
						("Museum"		, 	"Museums"),
						("NaturePark"	,	"Nature Park"),
						("AmusementPark",	"Amusement Parks"),
						]


Travel_Dates_C=	[
						(True			,	'Fixed'),
						(False			,	'Flexible')
						]

MaxHours_C =	[
						(1			,	'1'),
						(2			,	'2'),
						(3			,	'3'),
						(4			,	'4'),
						(5			,	'5'),
						(6			,	'6'),
						(7			,	'7'),
						(8			,	'8'),
						(9			,	'9'),
						(10			,	'10'),
						(11			,	'11'),
						(12			,	'12'),
						(13			,	'13'),
						(14			,	'14')

						]




# Meal_Preference_C	= 	[
# 						('LongMeal'		,	'Long Meal'),
# 						('ShortMeal'	,	'Short Meal')
# 						]






class SetTravellerInfoBasic (forms.Form):

	Your_Name = forms.CharField	(	
											widget 	= forms.TextInput(
											attrs 	= {
											'class'			: 'form-control',
											'placeholder' 	: 'John Doe'
											}						)
										)
	Your_Email = forms.EmailField	(	
											widget 	= forms.TextInput(
											attrs 	= {
											'class'			: 'form-control',
											'placeholder' 	: 'JohnDoe@u.nus.edu.sg'
											}						)
										)
	
	How_Are_You_Travelling = forms.ChoiceField	(	
											choices = Traveller_Type_C,
											widget 	= forms.Select(
											attrs 	= {
											'select class'	: 'custom-select my-1 mr-sm-2',
											})
										)
	Interest = forms.MultipleChoiceField(
											choices = Category_C,
											widget = forms.CheckboxSelectMultiple(
											)
										)
	Travel_Dates = forms.ChoiceField(
											choices = Travel_Dates_C,
											required= True,
											widget 	= forms.Select(
											attrs 	= {
											'select class'			: 'custom-select my-1 mr-sm-2',
											}			
											)
										)





class FlexTravel (forms.Form):

	No_of_Travel_Days = forms.IntegerField(	
											widget 	= forms.TextInput(
											attrs 	= {
											'class'			: 'form-control',
											'placeholder' 	: '1'
											}						)
										)

	Min_Hours_Per_Day = forms.ChoiceField		(		
											choices = MaxHours_C,
											widget 	= forms.Select(
											attrs 	= {
											'select class'	: 'custom-select my-1 mr-sm-2',
											})
										)
	Max_Hours_Per_Day = forms.ChoiceField	(	
											choices = MaxHours_C,
											widget 	= forms.Select(
											attrs 	= {
											'select class'	: 'custom-select my-1 mr-sm-2',
											})
										)#MaxHours = 14
	# Meal_Preferences = forms.ChoiceField	(
	# 										choices = Meal_Preference_C,
	# 										required= True,
	# 										widget 	= forms.Select(
	# 										attrs 	= {
	# 										'select class'		: 'custom-select my-1 mr-sm-2',
	# 										#'type' 			: 'checkbox',
	# 										}			
	# 										)
	# 									)

										
	Hotel_Name = forms.CharField	(		required=False,
											widget 	= forms.TextInput(
											attrs 	= {
											'class'			: 'form-control',
											'placeholder' 	: 'Marina Bay Sands'
											}						)
										)





class NonFlexTravel (forms.Form):
	Arrival_Date 	=	forms.DateField(
											widget=forms.SelectDateWidget(
											attrs = {
											'data-date-format' : 'dd/mm/yyyy',
											'class': 'form-control snps-inline-select'
													}

    										)
										)
											
	Departure_Date	= 	forms.DateField(
											widget=forms.SelectDateWidget(
											attrs = {
											'data-date-format' : 'dd/mm/yyyy',
											'class': 'form-control snps-inline-select'
											}
											)
    									)					
	Min_Hours_Per_Day = forms.ChoiceField		(		
											choices = MaxHours_C,
											widget 	= forms.Select(
											attrs 	= {
											'select class'	: 'custom-select my-1 mr-sm-2',
											})
										)
	Max_Hours_Per_Day = forms.ChoiceField	(	
											choices = MaxHours_C,
											widget 	= forms.Select(
											attrs 	= {
											'select class'	: 'custom-select my-1 mr-sm-2',
											})
										)
	# Meal_Preferences = forms.ChoiceField	(
	# 										choices = Meal_Preference_C,
	# 										required= True,
	# 										widget 	= forms.Select(
	# 										attrs 	= {
	# 										'select class'			: 'custom-select my-1 mr-sm-2',
	# 										#'type' 			: 'checkbox',
	# 										}			
	# 										)
										# )
	Hotel_Name = forms.CharField	(		required=False,
											widget 	= forms.TextInput(
											attrs 	= {
											'class'			: 'form-control',
											'placeholder' 	: 'Marina Bay Sands'
											}						)
										)




