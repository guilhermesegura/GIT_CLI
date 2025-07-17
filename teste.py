# Global variable declaration
global_var = "I am global"

def access_global():
    print(f"Inside function: {global_var}")

def modify_global():
    global global_var  # Declare intent to modify the global variable
    global_var = "I am modified global"
    print(f"Inside function after modification: {global_var}")

access_global()  # Accessing the global variable
print(f"Outside function: {global_var}")

modify_global()  # Modifying the global variable
print(f"Outside function after modification: {global_var}")