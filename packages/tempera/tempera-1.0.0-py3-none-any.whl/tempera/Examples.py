import temperature

# Create temperature objects directly, in celsius:
temp1 = temperature.Temperature(12, decimal_place=None)
temp2 = temperature.Temperature(18, decimal_place=1)
temp3 = temperature.Temperature(30)  # Default decimal place is 2

# Or create them using a value in a specific temperature scale
# Supported scales: Kelvin, Celsius, and Fahrenheit:
temp1 = temperature.K(0, decimal_place=None)
temp2 = temperature.C(18, decimal_place=1)
temp3 = temperature.F(86)

print("Temperatures:")
print(F"temp1 - F: {temp1.f}, C: {temp1.C}, K: {temp1.K}")
print(F"temp2 - F: {temp2.f}, C: {temp2.C}, K: {temp2.K}")
print(F"temp3 - F: {temp3.f}, C: {temp3.C}, K: {temp3.K}")
print("")

temp1.K = 326  # Temperatures can be reassigned using a value in any scale
temp2.f = 23   # Access the scale attribute in upper or lower case
temp3.celsius = -5   # or use the full word

print("Changed Temperatures:")
print(F"temp1 - F: {temp1.f}, C: {temp1.C}, K: {temp1.K}")
print(F"temp2 - F: {temp2.f}, C: {temp2.C}, K: {temp2.K}")
print(F"temp3 - F: {temp3.f}, C: {temp3.C}, K: {temp3.K}")
print("")

# Set a global scale, and getTemperature() will
# return the temperature object in that scale.
temp1.setGlobalScale('f')
print("Global temperature scale set to " + temp1.getCurrentScale(
      word=True) + ":")
print(F"temp1: {temp1.getTemperature()} {temp1.getCurrentScale()}")
print(F"temp1: {temp2.getTemperature()} {temp2.getCurrentScale()}")
print(F"temp1: {temp3.getTemperature()} {temp3.getCurrentScale()}")
print("")

# Method setGlobalScale() allows variation in case and verbage
temp2.setGlobalScale('c')
temp1.setGlobalScale('Kelvin')
temp2.setGlobalScale('celsius')

# Global scale can also be set from the class itself with this function:
temperature.Temperature.setCurrentScale('f')

# Set a local scale for a specific temperature object
# to override the current global scale setting
temp2.setLocalScale('kelvin')
print("Global scale is Fahrenheit, but temp2 has local scale set to Kelvin:")
print(F"Temperature 1 returns as {temp1.getCurrentScale(word=True)}: "
      F"{str(temp1.getTemperature())}")
print(F"Temperature 2 returns as "
      F"{temp2.getCurrentScale(word=True, capitalized=False)}: "
      F"{str(temp2.getTemperature())}")
print(F"Temperature 3 returns as {temp3.getCurrentScale(word=True)}: "
      F"{str(temp3.getTemperature())}")
print("")

# Temperature objects can also represent intervals
temp_interval = temperature.Temperature(3, isinterval=True)
print("Interval of 3 celsius converted to current global scale of Fahrenheit:")
print(temp_interval.getTemperature())

temp1 = temperature.Temperature(12, decimal_place=2)
temp_interval = temperature.Temperature(3, isinterval=True)

print("\n3 celsius added to the current value of temp1:")
print(temp1.C + temp_interval.C)  # Adds 3 celsius to temp1 and prints
