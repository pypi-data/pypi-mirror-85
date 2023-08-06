class Temperature():
    """Create persistent convertible temperature objects w/ shared global scale

    Default scale is celsius
    Conversions are set and accessed as properties with:
    self.c -- Celsius
    self.f -- Fahrenheit
    self.k -- Kelvin

    Arguments:
    temperature -- Temperature to assign
    isinterval -- Set to True if temperature as interval is desired
    decimal_place -- Set the number of decimal points to round temperature
        2 by default
    local_scale -- Override any global scale used

    self.getTemperature() accesses value w/ current global scale preference
    self.setGlobalScale() sets temperature scale that all instances use when
        self.getTemperature() is called.
        Equivelant non-instance function is Temperature.setCurrentScale()
    self.setLocalScale() overrides Global conversion preference for an instance
    self.useGlobalScale() stops conversion preference override
    """
    _Current_Scale = 'C'

    def setCurrentScale(scale_letter):
        """accepts string representing current scale.

        'c' for celsius, 'f' for fahrenheit, 'k' for kelvin"""
        Temperature._Current_Scale = Temperature._scaleStrCheck(scale_letter)

    def getCurrentGlobalScale():
        return Temperature._Current_Scale

    def convertToCelsius(temperature, isinterval=False):
        """Converts given temperature from current global scale to Celsius

        Useful when quick conversion is needed on an impermanent variable"""
        temp = Temperature(isinterval=isinterval)
        temp.setTemperature(temperature)
        return temp.c

    def _scaleStrCheck(scale_letter):
        """Checks that scale string is appropriate format

        'c' for celsius, 'f' for fahrenheit, 'k' for kelvin"""
        if ((scale_letter == 'c') or (scale_letter == 'C') or (
                scale_letter == 'celsius') or (scale_letter == 'Celsius') or (
                scale_letter == 'centigrade') or (
                scale_letter == 'Centigrade')):
            current_scale = 'C'
        elif ((scale_letter == 'f') or (scale_letter == 'F') or (
                scale_letter == 'fahrenheit') or (
                scale_letter == 'Fahrenheit')):
            current_scale = 'F'
        elif ((scale_letter == 'k') or (scale_letter == 'K') or (
                scale_letter == 'kelvin') or (scale_letter == 'Kelvin')):
            current_scale = 'K'
        else:
            raise ValueError("Argument must be 'C' or 'celsius', 'F' or"
                             " 'fahrenheit', or 'K' or 'kelvin'")
        return current_scale

    def __init__(self, temp=0, isinterval=False, decimal_place=2,
                 local_scale=False):
        self.__is_interval = True if (isinterval is True) else False
        self.__scale_override = False
        self.setDecimalPlace(decimal_place)
        if local_scale:
            self.setLocalScale(local_scale)
            self.setTemperature(temp)
        else:
            self._celsius = temp

    def _globalScaleOverrideCheck(self):
        if self.__scale_override is False:
            return self._Current_Scale
        else:
            return self.__scale_override

    def setDecimalPlace(self, decimal_place):
        """Sets the number of decimal places to round temperatures
        Argument decimal_place must be an integer or None for no decimal place.
        Saved value is not rounded - Temperature is rounded when returned"""
        if isinstance(decimal_place, int) or (decimal_place is None):
            self._decimal_place = decimal_place
        else:
            raise TypeError("Number of Decimal places must be passed as "
                            "an integer, or None for no decimal place.")

    def getCurrentScale(self, word=False, capitalized=True):
        """Returns the current default scale type of this temperature as string
        This is the current global scale unless a local scale has been set.
        Non method equivelant is Temperature.getCurrentScaleString(), which
        returns current global scale.

        Keyword Arguments:
        word -- Set False to return first letter of scale, True for full word
        capitalized -- Set to False to return scale string in all lower case"""
        scale_string = None
        if self.__scale_override:
            scale_string = self.__scale_override
        else:
            scale_string = Temperature._Current_Scale

        if word is True:
            if scale_string == "F":
                scale_string = "Fahrenheit"
            if scale_string == "C":
                scale_string = "Celsius"
            if scale_string == "K":
                scale_string = "Kelvin"
        if capitalized is False:
            scale_string = scale_string.lower()
        return scale_string

    def getTemperature(self):
        """Returns temperature in scale determined by Global scale
        or by internal scale if self.__scale_override"""
        current_scale = self._globalScaleOverrideCheck()

        if current_scale == 'C':
            return self.c
        elif current_scale == 'F':
            return self.f
        elif current_scale == 'K':
            return self.k

    def setTemperature(self, temperature):
        """Sets temperature assuming it is in Global scale
        (or internal scale if self.__scale_override)"""
        current_scale = self._globalScaleOverrideCheck()

        if current_scale == 'C':
            self.c = temperature
        elif current_scale == 'F':
            self.f = temperature
        elif current_scale == 'K':
            self.k = temperature

    def setGlobalScale(self, scale_letter):
        Temperature.setCurrentScale(scale_letter)

    def useGlobalScale(self):
        """If local scale conversion is set, resets to using Global scale"""
        self.__scale_override = False

    def setLocalScale(self, scale_letter):
        """Overrides global scale conversion with provided scale.
        reversed by function self.useGlovalScale()"""
        if scale_letter is not False:
            self.__scale_override = Temperature._scaleStrCheck(scale_letter)
        else:
            self.useGlobalScale()

    # Property used to check temperature input before applying to __celsius
    @property
    def _celsius(self):
        return self.__celsius
    @_celsius.setter
    def _celsius(self, t):
        try:
            t + 1
        except TypeError:
            raise TypeError("Given value is of type " + str(
                            type(t)) + ". Value must be a number.")
        if (t < -273.15) and (self.__is_interval is False):
            raise ValueError("Given temperature is below absolute zero")
        self.__celsius = t

    @property
    def c(self):
        """returns celsius temperature"""
        t = round(self._celsius, self._decimal_place)
        return t
    @c.setter
    def c(self, t):
        self._celsius = t

    @property
    def f(self):
        """returns fahrenheit temperature"""
        interval = 9 * (self._celsius) / 5
        i = (interval + 32) if self.__is_interval is False else interval
        return round(i, self._decimal_place)
    @f.setter
    def f(self, t):
        if self.__is_interval is False:
            t = 5 * (t - 32) / 9
        else:
            t = 5 * t / 9
        self._celsius = t

    @property
    def k(self):
        """returns kelvin temperature"""
        interval = self._celsius
        i = (interval + 273.15) if self.__is_interval is False else interval
        return round(i, self._decimal_place)
    @k.setter
    def k(self, t):
        if self.__is_interval is False:
            self._celsius = t - 273.15
        else:
            self._celsius = t

    # Scale method aliases
    C = c
    Celsius = c
    celsius = c

    F = f
    fahrenheit = f
    Fahrenheit = f

    K = k
    kelvin = k
    Kelvin = k


def C(temp=0, isinterval=False, decimal_place=2, local=False):
    """Returns Temperature object assuming given temperature is Celsius"""
    temperature = Temperature(temp, isinterval, decimal_place, local_scale='C')
    if local is False:
        temperature.useGlobalScale()
    return temperature


# C Function Aliases
c = C
Celsius = C
celsius = C


def F(temp=0, isinterval=False, decimal_place=2, local=False):
    """Returns Temperature object assuming given temperature is Fahrenheit"""
    temperature = Temperature(temp, isinterval, decimal_place, local_scale='F')
    if local is False:
        temperature.useGlobalScale()
    return temperature


# F Function Aliases
f = F
Fahrenheit = F
fahrenheit = F


def K(temp=0, isinterval=False, decimal_place=2, local=False):
    """Returns Temperature object assuming given temperature is Kelvin"""
    temperature = Temperature(temp, isinterval, decimal_place, local_scale='K')
    if local is False:
        temperature.useGlobalScale()
    return temperature


# K Function Aliases
k = K
Kelvin = K
kelvin = k
