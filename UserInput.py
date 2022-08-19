# user input instead of fixed data


Name_Of_Unit = "hours"
Name_Of_Unit_to_be_converted = "Days"
Calculation_To_Units = 24


def days_to_units(number_of_days):
    return f"{number_of_days} {Name_Of_Unit_to_be_converted} = {Calculation_To_Units * number_of_days} {Name_Of_Unit} "
#    print(f"{number_of_days} {Name_Of_Unit_to_be_converted} = {Calculation_To_Units * number_of_days} {Name_Of_Unit} ")
#    print(str(number_of_days) + " " + str(Name_Of_Unit_to_be_converted) + " = " + str(Calculation_To_Units * number_of_days) + " " + str(Name_Of_Unit))


#days_to_units(35)
# input function is used to get input from the user it already exits you don't need to create it
User_Input = input(" Hey , Please enter Number of days \n")
User_Input_Var = int(User_Input)

Calculation_Result = days_to_units(User_Input_Var)
print(Calculation_Result)