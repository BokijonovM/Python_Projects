"""
Bokijonov Mukhsinjon
52336
task 3

"""

# getting input from the user and assigning it to user

height = float(input("Enter height in metres: "))
weight = float(input("Enter weight in kg: "))

# the formula for calculating bmi
# bmi = Weight / (Height^2)
bmi = weight/(height**2)


# ** is the power of operator i.e height*height in this case

print("Your BMI is: {0} and you are: ".format(bmi), end='')

#conditions
"""
Category								BMI (kg/m2)			BMI Prime
                                		from	to	      from		to
Very severely underweight						15					0.60
Severely underweight	        		15	    16	      0.60		0.64
Underweight	                    		16	    18.5	  0.64		0.74
Normal (healthy weight)	        		18.5	25	      0.74		1.0
Overweight	                    		25	    30	      1.0		1.2
Obese Class I (Moderately obese)		30	    35	      1.2		1.4
Obese Class II (Severely obese)			35	    40	      1.4		1.6
Obese Class III (Very severely obese)	40				  1.6
"""
if ( bmi >= 16 and bmi < 18.5):
   print("Underweight")
elif ( bmi >= 18.5 and bmi < 25):
   print("Normal")
elif ( bmi >= 25 and bmi < 30):
   print("Overweight")
elif ( bmi >=30):
   print("Obese")
