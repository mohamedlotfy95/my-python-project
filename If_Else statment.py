# user input instead of fixed data
# days_to_units(35)
# input function is used to get input from the user it already exits you don't need to create it

Name_Of_Unit = "hours"
Name_Of_Unit_to_be_converted = "Days"
Calculation_To_Units = 24
User_Input = input(" Hey , Please enter Number of days \n")


def days_to_units(number_of_days):
    try:
        if number_of_days < 0:
            return "no negative value is allowed"
        elif number_of_days == 0:
            return " you entered 0 Please Enter only valid numbers"

    except ValueError:
        return f"{number_of_days} {Name_Of_Unit_to_be_converted} = {Calculation_To_Units * number_of_days} {Name_Of_Unit}"


def validate_and_excute():
    if User_Input.isdigit():
        user_input_var = int(User_Input)
        calculation_result = days_to_units(user_input_var)
        print(calculation_result)
    else:
        print(" Please Enter only valid numbers")


validate_and_excute()
