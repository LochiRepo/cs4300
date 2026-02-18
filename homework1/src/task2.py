#Declare and test each of these types
def demonstrate_types():
#Integer
    age = 22
#Float
    temperature = 97.2
#String
    name = "Sven"
#Boolean
    is_student = True
    return age, temperature, name, is_student

#Runs the print and program tests
if __name__ == "__main__":
    age, temperature, name, is_student = demonstrate_types()
    print(f"Integer: {age}")
    print(f"Float:   {temperature}")
    print(f"String:  {name}")
    print(f"Boolean: {is_student}")
