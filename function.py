# function to avoid the repeating
# def mean define
# parameters :some input values when u use the function
# you have global and internal scope variables
Name_Of_Unit = "hours"
Name_Of_Unit_to_be_converted = "Days"
Calculation_To_Units = 24


def days_to_units(number_of_days, custom_message):
    print(
        f"{number_of_days} {Name_Of_Unit_to_be_converted} = {Calculation_To_Units * number_of_days} {Name_Of_Unit} {custom_message}")
    print(str(number_of_days) + " " + str(Name_Of_Unit_to_be_converted) + " = "
          + str(Calculation_To_Units * number_of_days) + " " + str(Name_Of_Unit) + " " + str(custom_message))


days_to_units(35, "Nice")
days_to_units(50, "")
days_to_units(100, '')
