# Tempera

## Description

Create temperature objects which return their value in a set 'global' unit scale - either Celsius, Fahrenheit, or Kelvin - using the method <b>getTemperature()</b>. When the Global temperature scale is changed, all temperature objects are returned in that scale.

I created this module to easily convert multiple temperatures displayed on a GUI when a user selects a different scale. I imagine it could be useful any time one has multiple persistant temperatures that need to undergo unit conversion at will.

## Using this Module

The Global temperature scale can be set with the method <b>self.setGlobalScale()</b>. All Temperature objects will return in this scale with <b>self.getTemperature()</b>. 

Set or return from a specific scale using <b>self.c</b> for Celsius, <b>self.f</b> for Fahrenheit, and <b>self.k</b> for Kelvin.

### Local Scales

If you want a specific Temperature object to return <b>self.getTemperature()</b> in a different scale regardless of the current global scale, use <b>self.setLocalScale()</b>. Can return to using global scale with <b>self.setLocalScale(False)</b> or <b>self.useGlobalScale()</b>.

### Rounding

Set the number of decimal places with the <b>decimal_place</b> keyword argument:
```python
temp1 = temperature.Temperature(12, decimal_place=2)
```
Or with <b>self.setDecimalPlace(int)</b>. The default decimal place is 2. <i>None</i> will always return a rounded integer.

### Intervals

Temperature objects can also represent intervals instead of actual temperatures with the keyword argument <b>isinterval=True</b>. For example, if you wanted to represent an interval of 3 celsius units:
```python
temp_interval = temperature.Temperature(3, isinterval=True)

print(temp1.C + temp_interval.C)  # Adds 3 celsius to temp1 and prints
```

## How it functions

The temperature is stored internally in Celsius. All setting and getting of the temperature in different scales is a conversion from this 'private' celsius attribute. This attribute is not rounded. Any rounding is done when <b>getTemperature()</b> (or a similar method) is called, so setting a decimal place does not affect the internally stored temperature.
