# ACS utilizes the following units system-wide:
#   time        : seconds
#   distance    : feet
#   force       : newtons
#   temperature : fahrenheit
#   pressure    : hectopascals

def meters_to_feet(n):
    return n * 3.28084

def celsius_to_fahrenheit(n):
    return n * 1.8 + 32

def newtons_to_pounds(n):
    return n * 0.224809
