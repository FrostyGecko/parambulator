from pint import UnitRegistry
from uncertainties import ufloat
from uncertainties import unumpy as unp
import copy as copy
ureg = UnitRegistry()
import random
import numpy as np
import scipy.stats as stats

class constant():
    def __init__(self, 
                 value: float or int, 
                 uncertainty: float or int = 0, 
                 unit: str = '', 
                 abbreviation: str = '', 
                 name: str = '', 
                 system: str = '', 
                 value_ref: str = '', 
                 value_ref_link: str = '', 
                 u_ref: str = '', 
                 u_ref_link: str = '',
                 description: str = '',
                 lower_bound: float = None,
                 upper_bound: float = None,
                 **kwargs):
        '''
        Initializes a constant with specified attributes, including its value, unit, and references.
        
        For example,
        
        AU   = constant(
                            abbrev          = 'AU',
                            name            = 'astronomical unit',
                            value           = 1.49597870700*(10**11),
                            uncertainty     = 3,
                            unit            = 'm',
                            value_ref       = 'IAU',
                            value_ref_link  = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                            u_ref           = 'IAU',
                            u_ref_link      = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf'
                           )
        

        Parameters
        ----------
        value : float
            The nominal value of the constant (e.g., 9.81 for gravity in m/s^2).
        uncertainty : float, optional
            Uncertainty in the value of the constant, allowing for error propagation in calculations. Default is 0.
        unit : str, optional
            Unit of the constant (e.g., 'm/s^2', 'kg'). Default is an empty string.
        abbreviation : str, optional
            Abbreviation for the constant (e.g., 'g' for gravity). Default is an empty string.
        name : str, optional
            Full name of the constant (e.g., 'Gravitational acceleration'). Default is an empty string.
        system : str, optional
            Specifies the measurement system of the constant, such as 'SI' or 'Imperial'. Default is an empty string.
        value_ref : str, optional
            Citation or reference for the value of the constant. Default is an empty string.
        value_ref_link : str, optional
            URL or link to the source of the value. Default is an empty string.
        u_ref : str, optional
            Reference for the uncertainty. Default is an empty string.
        u_ref_link : str, optional
            URL or link to the source of the uncertainty. Default is an empty string.
        description : str, optional
            Description of the constant
        lower_bound : float, optional
            Lower limit of uniform distribution
        upper_bound : float, optional
            Upper limit of uniform distribution
        **kwargs : dict, optional
            Additional keyword arguments for any extra parameters.

        Returns
        -------
        None.
        '''
        
        try:
            assert isinstance(value, (float,int))
            assert isinstance(uncertainty, (float,int))
            assert uncertainty >= 0, "Uncertainty must be greater than or equal to 0"
            assert isinstance(unit,str)
            
            self.abbreviation   = abbreviation                          # Short name (e.g., 'c' for speed of light)
            self.name           = name                                  # Full name of the constant (e.g., 'Speed of Light')
            try:
                self.value      = ufloat(value, uncertainty)*ureg(unit) # Store value with unit and uncertainty
            except:
                self.value      = ufloat(value, uncertainty) * unit     # Fallback if unit is invalid
            self.system         = system                                # System for classification (e.g., 'SI')
            self.value_ref      = value_ref                             # Source for the constant's value
            self.value_ref_link = value_ref_link                        # Link to source
            self.u_ref          = u_ref                                 # Source for uncertainty
            self.u_ref_link     = u_ref_link                            # Link to uncertainty source
            self.lower_bound    = lower_bound                         
            self.upper_bound    = upper_bound
            
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def __repr__(self) -> str:
        '''
        Provides a string representation of the constant's nominal value and unit, 
        useful for debugging and quick reference.

        Returns
        -------
        str
            A string representation showing the constant's value and unit.
        '''
        return str(self.value)

    #%% Trigonometric Methods
    def sin(self) -> float or object:
        '''
        Computes the sine of the constant's value, propagating any associated uncertainty.
        
        Returns
        -------
        constant
            A new constant instance with the sine of the original value and its propagated uncertainty.
        '''
        try:
            value = unp.sin(self.value).tolist()                  # Calculate sine
            return constant(value.n, uncertainty=value.s)         # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def cos(self) -> float or object:
        '''
        Computes the cosine of the constant's value, propagating any associated uncertainty.
        
        Returns
        -------
        constant
            A new constant instance with the cosine of the original value and its propagated uncertainty.
        '''
        try:
            value = unp.cos(self.value).tolist()                  # Calculate cosine
            return constant(value.n, uncertainty=value.s)         # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    def tan(self) -> float or object:
        '''
        Computes the tangent of the constant's value, propagating any associated uncertainty.
        
        Returns
        -------
        constant
            A new constant instance with the tangent of the original value and its propagated uncertainty.
        '''
        try:
            value = unp.tan(self.value).tolist()                  # Calculate tangent
            return constant(value.n, uncertainty=value.s)         # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    def arcsin(self) -> float or object:
        '''
        Computes the arcsine (inverse sine) of the constant's value, propagating any associated uncertainty.
        
        Returns
        -------
        constant
            A new constant instance with the arcsine of the original value and its propagated uncertainty.
        '''
        try:
            value = unp.arcsin(self.value).tolist()               # Calculate arcsine
            return constant(value.n, uncertainty=value.s)         # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            
    def arccos(self) -> float or object:
        '''
        Computes the arccosine (inverse cosine) of the constant's value, propagating any associated uncertainty.
        
        Returns
        -------
        constant
            A new constant instance with the arccosine of the original value and its propagated uncertainty.
        '''
        try:
            value = unp.arccos(self.value).tolist()               # Calculate arccosine
            return constant(value.n, uncertainty=value.s)         # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    def arctan(self) -> float or object:
        '''
        Computes the arctangent (inverse tangent) of the constant's value, propagating any associated uncertainty.
        
        Returns
        -------
        constant
            A new constant instance with the arctangent of the original value and its propagated uncertainty.
        '''
        try:
            value = unp.arctan(self.value).tolist()               # Calculate arctangent
            return constant(value.n, uncertainty=value.s)         # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    #%% Arithmetic Operations
    def __add__(self, val) -> float or object:
        '''
        Adds another constant or a scalar to this constant, handling compatible units, and 
        returns a new constant with the result and propagated uncertainty.

        Parameters
        ----------
        val : constant or float
            Another constant or a numeric value to add to this constant.

        Returns
        -------
        constant
            A new constant instance representing the sum.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = self.value + val.value         # Add constant values
            else:
                new_constant.value = self.value + val * self.unit   # Add scalar (assumes compatible unit)
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None


    def __radd__(self, val) -> float or object:
        '''
        Adds this constant to another constant or scalar from the right, handling units.

        Parameters
        ----------
        val : constant or float
            A numeric value or another constant to add from the right side.

        Returns
        -------
        constant
            A new constant instance with the addition result.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = self.value + val.value         # Add constant values
            else:
                new_constant.value = self.value + val * self.unit   # Add scalar (assumes compatible unit)
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def __sub__(self, val) -> float or object:
        '''
        Subtracts another constant or scalar from this constant and returns the result.

        Parameters
        ----------
        val : constant or float
            The value to subtract, either as another constant or a numeric value.

        Returns
        -------
        constant
            A new constant instance representing the result of the subtraction.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = self.value - val.value         # Subtract constant values
            else:
                new_constant.value = self.value - val * self.unit   # Subtract scalar
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    def __rsub__(self, val) -> float or object:
        '''
        Subtracts this constant from another constant or scalar (right-hand subtraction).

        Parameters
        ----------
        val : constant or float
            The value from which this constant will be subtracted.

        Returns
        -------
        constant
            A new constant instance representing the result.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = val.value - self.value         # Subtract constant values
            else:
                new_constant.value = val * self.unit - self.value   # Subtract scalar
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def __mul__(self, val) -> float or object:
        '''
        Multiplies this constant by another constant or scalar, handling uncertainty propagation.

        Parameters
        ----------
        val : constant or float
            The value to multiply, as another constant or numeric value.

        Returns
        -------
        constant
            A new constant instance representing the product.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = self.value * val.value         # Multiply constant values
            else:
                new_constant.value = self.value * val * self.unit   # Multiply scalar
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def __rmul__(self, val) -> float or object:
        '''
        Multiplies a constant or scalar by this constant from the right (right-hand multiplication).

        Parameters
        ----------
        val : constant or float
            The constant or numeric value to multiply.

        Returns
        -------
        constant
            A new constant instance representing the product.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = val.value * self.value         # Multiply constant values
            else:
                new_constant.value = val * self.unit * self.value   # Multiply scalar
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def __truediv__(self, val) -> float or object:
        '''
        Divides this constant by another constant or scalar, propagating uncertainty.

        Parameters
        ----------
        val : constant or float
            The divisor, as another constant or a scalar.

        Returns
        -------
        constant
            A new constant instance representing the division result.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = self.value / val.value         # Divide constant values
            else:
                new_constant.value = self.value / val               # Divide by scalar
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def __rtruediv__(self, val) -> float or object:
        '''
        Divides another constant or scalar by this constant (right-hand division).

        Parameters
        ----------
        val : constant or float
            The dividend, as another constant or a scalar.

        Returns
        -------
        constant
            A new constant instance representing the division result.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = val.value / self.value         # Divide constant values
            else:
                new_constant.value = val / self.value               # Divide by scalar
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def __pow__(self, val) -> float or object:
        '''
        Raises this constant to the power of another constant or scalar, propagating uncertainty.

        Parameters
        ----------
        val : constant or float
            The exponent, either as another constant or numeric value.

        Returns
        -------
        constant
            A new constant instance representing the result of the exponentiation.
        '''
        try:
            new_constant = copy.copy(self)                          # Create a copy for the result
            new_constant.clear_info()                               # Clear metadata in result
            if hasattr(val, 'value'):                               # Checks if val has attribute "value"
                new_constant.value = self.value ** val.value        # Power with constant
            else:
                new_constant.value = self.value ** val              # Power with scalar
            return new_constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def log(self) -> float or object:
        '''
        Computes the natural logarithm of the constant's value, propagating uncertainty.

        Returns
        -------
        constant
            A new constant instance representing the natural log of the original value.
        '''
        try:
            value = unp.log(self.value).tolist()                    # Calculate log
            return constant(value.n, uncertainty=value.s)           # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    def exp(self) -> float or object:
        '''
        Computes the exponential (e^x) of the constant's value, propagating uncertainty.

        Returns
        -------
        constant
            A new constant instance representing the exponential of the original value.
        '''
        try:
            value = unp.exp(self.value).tolist()                    # Calculate exp
            return constant(value.n, uncertainty=value.s)           # Return as a new constant
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def sqrt(self) -> float or object:
        '''
        Computes the square root of the constant's value, propagating uncertainty.

        Returns
        -------
        constant
            A new constant instance representing the square root of the original value.
        '''
        try:
            return self.__pow__(0.5)                                # Use power method with 0.5 exponent
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    #%% Properties
    @property
    def u(self) -> float:
        '''
        Retrieves the uncertainty of the constant's value.

        Returns
        -------
        float
            The standard deviation (uncertainty) of the constant's value.
        '''
        return self.value.s                                     # Return uncertainty

    @u.setter
    def u(self, new_u):
        '''
        Sets a new uncertainty while preserving the nominal value and unit.
        
        For example, constant.u = 0.5

        Parameters
        ----------
        new_u : float
            The new uncertainty value to set.

        Returns
        -------
        None.
        '''
        try:
            self.value = ufloat(self.value.n, new_u) * self.value.units
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    @property
    def n(self) -> float: 
        '''
        Retrieves the nominal (central) value of the constant.

        Returns
        -------
        float
            The nominal value of the constant.
        '''
        return self.value.n                                     # Return nominal value

    @n.setter 
    def n(self, new_n): 
        '''
        Sets a new nominal value while preserving the uncertainty and unit.
        
        For example, constant.n = 10

        Parameters
        ----------
        new_n : float
            The new nominal value to set.

        Returns
        -------
        None.
        '''
        try:
            self.value = ufloat(new_n, self.value.s) * self.value.units     # Set new nominal value
        except Exception as e:
            print(f'ERROR: {e}')
            return None
        
    @property
    def unit(self) -> object:
        '''
        Retrieves the unit of the constant.

        Returns
        -------
        object
            The unit of the constant's value.
        '''
        return self.value.units                                 # Return units

    @unit.setter
    def unit(self, new_unit):
        '''
        Converts the constant to a new unit. For example, constant.unit = "m"

        Parameters
        ----------
        new_unit : str
            The new unit to convert the constant's value to.

        Returns
        -------
        None.
        '''
        try: 
            self.value = self.value.to(ureg(new_unit))          # Set new unit
        except Exception as e:
            print(f'ERROR: {e}')
            return None
    
    # Random Sampling
    @property
    def gaussian_sample(self) -> float:
        '''
        Returns a Gaussian-distributed sample based on the constant's mean (nominal value) 
        and standard deviation (uncertainty).

        Returns
        -------
        float
            A single sample value drawn from the constant's Gaussian distribution.
        '''
        try:
            return self.gaussian(self.value.n, self.value.s)
        except Exception as e:
            print(f'ERROR: {e}')
            return None
        
    @property
    def uniform_sample(self) -> float:
        '''
        Generates a random sample from a uniform distribution within specified bounds.
        
        The uniform distribution generates values with equal probability across the range defined
        by `self.lower_bound` and `self.upper_bound`.
    
        Returns
        -------
        float
            A random sample from the uniform distribution between `self.lower_bound` and `self.upper_bound`.
            If bounds are not defined, it returns None and prints an error.
    
        '''
        try:
            # Generate a uniform random sample between lower and upper bounds
            return self.uniform(self.lower_bound, self.upper_bound)
        except Exception as e:
            print(f'ERROR: {e}')  # Print error message if uniform sampling fails
            return None
    
    
    @property
    def truncated_normal_sample(self) -> float:
        '''
        Generates a random sample from a truncated normal distribution within specified bounds.
        
        The truncated normal distribution is limited by `self.lower_bound` and `self.upper_bound`
        and is centered around the nominal value `self.n` with a spread defined by `self.u`.
    
        Returns
        -------
        float
            A random sample from the truncated normal distribution with mean `self.n`, standard
            deviation `self.u`, and bounds `self.lower_bound` and `self.upper_bound`.
            If any required parameter is not defined, returns None and prints an error.
    
        '''
        try:
            # Retrieve the nominal value, standard deviation, and bounds for sampling
            nominal     = self.n
            std_dev     = self.u
            lower_bound = self.lower_bound
            upper_bound = self.upper_bound
            
            # Generate a sample from the truncated normal distribution with specified parameters
            return self.truncated_normal_sample(nominal, std_dev, lower_bound, upper_bound)
        except Exception as e:
            print(f'ERROR: {e}')  # Print error message if sampling fails
            return None
    
    
    def probability_between_sample(self, lower_bound: float, upper_bound: float, **kwargs) -> float:
        '''
        Calculates the probability of a sample from the constant's distribution falling between two bounds.
        
        This function uses the constant's nominal value (`self.n`) and standard deviation (`self.u`) to
        model a normal distribution and calculate the probability that a sample falls within the specified
        bounds.
    
        Parameters
        ----------
        lower_bound : float
            The lower limit of the range for which the probability is calculated.
        upper_bound : float
            The upper limit of the range for which the probability is calculated.
        **kwargs : dict
            Additional arguments for customization, if needed.
    
        Returns
        -------
        float
            The probability that a sample falls between `lower_bound` and `upper_bound`.
            If parameters are not set or if an error occurs, returns None and prints an error message.
    
        '''
        try:
            # Calculate the probability of a value falling within the given range
            return self.probability_between(lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            mean=self.n,
                                            standard_deviation=self.u)
        except Exception as e:
            print(f'ERROR: {e}')  # Print error message if probability calculation fails
            return None
    
    
    #%% Statistical Methods
    def gaussian(self, nominal: float, std_dev: float, **kwargs) -> float:
        '''
        Generates a random sample from a Gaussian (normal) distribution.
        
        This method produces a random sample centered around the `nominal` value, with a spread
        defined by `std_dev`, following a Gaussian distribution.
    
        Parameters
        ----------
        nominal : float
            The mean (center) of the Gaussian distribution.
        std_dev : float
            The standard deviation (spread) of the Gaussian distribution.
        **kwargs : dict
            Additional arguments for customization, if needed.
    
        Returns
        -------
        float
            A random sample from the Gaussian distribution with mean `nominal` and standard deviation `std_dev`.
            If an error occurs, returns None and prints an error message.
    
        '''
        try:
            # Generate a random sample from the Gaussian distribution
            return random.gauss(nominal, std_dev)
        except Exception as e:
            print(f'ERROR: {e}')  # Print error message if sampling fails
            return None
    
    def uniform(self,
                       lower_bound: float, 
                       upper_bound: float,
                       **kwargs) -> float:
        """
        Returns a sample from a uniform distribution within the specified bounds.
        
        Parameters
        ----------
        lower_bound : float
            The minimum possible value for the uniform distribution.
        upper_bound : float
            The maximum possible value for the uniform distribution.
            
        Returns
        -------
        float
            A sample drawn from the uniform distribution between lower_bound and upper_bound.
        """
        try:
            return random.uniform(lower_bound, upper_bound)
        except Exception as e:
            print(f'ERROR: {e}')
            return None
            
    def truncated_normal(self,
                         nominal: float, 
                         std_dev: float, 
                         lower_bound: float, 
                         upper_bound: float,
                         **kwargs) -> float:
        """
        Returns a sample from a truncated normal distribution with specified bounds.

        Parameters
        ----------
        nominal : float
            The mean (nominal) value of the underlying normal distribution before truncation.
        std_dev : float
            The standard deviation of the underlying normal distribution before truncation.
        lower_bound : float
            The minimum possible value for the truncated distribution (left truncation).
        upper_bound : float
            The maximum possible value for the truncated distribution (right truncation).

        Returns
        -------
        float
            A sample drawn from the truncated normal distribution.
        """

        try: 
            # Define the standardized bounds
            a = (lower_bound - nominal) / std_dev   # Lower bound in standard deviations
            b = (upper_bound - nominal) / std_dev   # Upper bound in standard deviations
    
            # Define the truncated normal distribution
            truncated_normal = stats.truncnorm(a, b, loc=nominal, scale=std_dev)
    
            # Draw and return a sample
            return truncated_normal.rvs()
        except Exception as e:
            print(f'ERROR: {e}')
            return None
        
    def t_distribution(self, 
                       df: float,
                       mean: float, 
                       standard_deviation: float,
                       **kwargs) -> float:
        """
        Returns a sample from a t-distribution with specified degrees of freedom, mean, and standard deviation.
        
        Parameters
        ----------
        df : float
            The degrees of freedom for the t-distribution. A higher df makes the distribution resemble a normal distribution.
        mean : float, optional
            The mean (location) of the t-distribution. Default is 0.
        standard_deviation : float, optional
            The standard deviation (scale) of the t-distribution. Default is 1.
            
        Returns
        -------
        float
            A sample drawn from the t-distribution with specified parameters.
        """
        try:
            # Draw and return a sample from the t-distribution
            return stats.t.rvs(df, loc=mean, scale=standard_deviation)
        except Exception as e:
            print(f'ERROR: {e}')
            return None
        

    def normal_probability(self, 
                           value: float, 
                           mean: float, 
                           standard_deviation: float,
                           **kwargs) -> float:
        """
        Calculates the probability density of a given value occurring in a normal distribution 
        with specified mean and standard deviation.
        
        Parameters
        ----------
        value : float
            The value for which to calculate the probability density.
        mean : float
            The mean of the normal distribution.
        standard_deviation : float
            The standard deviation of the normal distribution.
            
        Returns
        -------
        float
            The probability density of the value occurring in the specified normal distribution.
        """
        # Calculate the probability density
        try:
            return stats.norm.pdf(value, loc=mean, scale=standard_deviation)
        except Exception as e:
            print(f'ERROR: {e}')
            return None
        
    def cumulative_probability(self, 
                               value: float, 
                               mean: float, 
                               standard_deviation: float, 
                               direction: str = "below",
                               **kwargs) -> float:
        """
        Calculates the cumulative probability of a value being below or above a given threshold
        in a normal distribution with a specified mean and standard deviation.
        
        Parameters
        ----------
        value : float
            The threshold value for which to calculate the cumulative probability.
        mean : float
            The mean of the normal distribution.
        standard_deviation : float
            The standard deviation of the normal distribution.
        direction : str, optional
            Specifies whether to calculate the probability of values "below" or "above" the threshold.
            Accepts "below" (default) or "above".
            
        Returns
        -------
        float
            The cumulative probability of the value being below or above the threshold.
        """
        # Calculate the cumulative probability below the threshold
        try: 
            cdf_value = stats.norm.cdf(value, loc=mean, scale=standard_deviation)
            
            if direction == "below":
                # Probability of value being less than or equal to the input value
                return cdf_value
            elif direction == "above":
                # Probability of value being greater than the input value
                return 1 - cdf_value
            else:
                raise ValueError("Invalid direction. Please choose 'below' or 'above'.")
        except Exception as e:
            print(f'ERROR: {e}')
            return None

    def probability_between(self, 
                            lower_bound: float, 
                            upper_bound: float, 
                            mean: float, 
                            standard_deviation: float,
                            **kwargs) -> float:
        """
        Calculates the cumulative probability of a value falling between a specified lower 
        and upper bound in a normal distribution with given mean and standard deviation.
        
        Parameters
        ----------
        lower_bound : float
            The lower bound of the range.
        upper_bound : float
            The upper bound of the range.
        mean : float
            The mean of the normal distribution.
        standard_deviation : float
            The standard deviation of the normal distribution.
            
        Returns
        -------
        float
            The cumulative probability of a value falling between the lower and upper bounds.
        """
        try:
            
            assert lower_bound < upper_bound, "lower_bound must be less than uppder_bound"
            assert standard_deviation >= 0, "standard deviation must be greater than or equal to 0"
            
            # Calculate the cumulative probability up to the upper bound
            cdf_upper = stats.norm.cdf(upper_bound, loc=mean, scale=standard_deviation)
            
            # Calculate the cumulative probability up to the lower bound
            cdf_lower = stats.norm.cdf(lower_bound, loc=mean, scale=standard_deviation)
            
            # The probability of the value being within the bounds is the difference between the two CDF values
            return cdf_upper - cdf_lower
        except Exception as e:
            print(f'ERROR: {e}')
            return None
        
    #%% Normal Methods    
    def clear_info(self):
        '''
        Clears the metadata of the constant, including name, abbreviation, and reference links.

        Returns
        -------
        None.
        '''
        self.abbreviation = ''                                  # Clear abbreviation
        self.name = ''                                          # Clear name
        self.value_ref = ''                                     # Clear value reference
        self.value_ref_link = ''                                # Clear value reference link
        self.u_ref = ''                                         # Clear uncertainty reference
        self.u_ref_link = ''                                    # Clear uncertainty reference link
        
    def copy(self) -> object:
        '''
        Creates and returns a deep copy of the constant instance, preserving all attributes.

        Returns
        -------
        constant
            A deep copy of the constant instance.
        '''
        return copy.deepcopy(self)
    
    def self_test(self):
        '''
        Runs a set of internal tests on basic arithmetic and trigonometric operations, verifying
        the behavior of constants under various operations.
        
        Returns
        -------
        None.
        '''
        a   = constant(
                            value           = 0.7,
                            uncertainty     = 0.2,
                            unit            = 'm',
                           )
        
        b   = constant(
                            value           = 0.4,
                            uncertainty     = 0.1,
                            unit            = 'm',
                           )
        
        a_pint_ufloat = ufloat(0.7,0.2)*ureg('meter')
        b_pint_ufloat = ufloat(0.4,0.1)*ureg('meter')
        
        print('----')
        print ('constant library  :  uncertainties W/pint libraries')
        print('----')
        print(f'{a+b}  :  {a_pint_ufloat+b_pint_ufloat}')
        print(f'{b+a}  :  {b_pint_ufloat+a_pint_ufloat}')
        print(f'{a-b}  :  {a_pint_ufloat-b_pint_ufloat}')
        print(f'{b-a}  :  {b_pint_ufloat-a_pint_ufloat}')
        print(f'{a*b}  :  {a_pint_ufloat*b_pint_ufloat}')
        print(f'{b*a}  :  {b_pint_ufloat*a_pint_ufloat}')
        print(f'{a/b}  :  {a_pint_ufloat/b_pint_ufloat}')
        print(f'{b/a}  :  {b_pint_ufloat/a_pint_ufloat}')
        
        print('----')
        print(f'{a+5}  :  {a_pint_ufloat+5*ureg("meter")}')
        print(f'{a-5}  :  {a_pint_ufloat-5*ureg("meter")}')
        print(f'{a*5}  :  {a_pint_ufloat*(5*ureg("meter"))}')
        print(f'{5*a}  :  {(5*ureg("meter"))*a_pint_ufloat}')
        print(f'{a/5}  :  {a_pint_ufloat/(5*ureg("meter"))}')
        print(f'{5/a}  :  {(5*ureg("meter"))/a_pint_ufloat}')
        
        print('----')
        print(f'{np.sin(a)}  :  {unp.sin(a_pint_ufloat)}')
        print(f'{np.cos(a)}  :  {unp.cos(a_pint_ufloat)}')
        print(f'{np.tan(a)}  :  {unp.tan(a_pint_ufloat)}')
        print(f'{np.arcsin(a)}  :  {unp.arcsin(a_pint_ufloat)}')
        print(f'{np.arccos(a)}  :  {unp.arccos(a_pint_ufloat)}')
        print(f'{np.arctan(a)}  :  {unp.arctan(a_pint_ufloat)}')
        print(f'{np.log(a)}  :  {unp.log(a_pint_ufloat)}')
        print(f'{np.exp(a)}  :  {unp.exp(a_pint_ufloat)}')
        print(f'{pow(a,2)}  :  {pow(a_pint_ufloat,2)}')
        print(f'{np.sqrt(a)}  :  {unp.sqrt(a_pint_ufloat)}')
        
        

#%% Template
if __name__ == "__main__":
    sigma   = constant(
                        abbrev          = 'sigma',
                        name            = 'Stefan-Boltzmann constant', 
                        value           = 5.670374419*(10**(-8)),
                        uncertainty     = 0,
                        unit            = 'W/(m^2*K^4)',
                        value_ref       = 'NIST',
                        value_ref_link  = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma',
                        u_ref           = 'NIST',
                        u_ref_link      = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma'
                       )

    AU   = constant(
                        abbrev          = 'AU',
                        name            = 'astronomical unit',
                        value           = 1.49597870700*(10**11),
                        uncertainty     = 3,
                        unit            = 'm',
                        value_ref       = 'IAU',
                        value_ref_link  = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                        u_ref           = 'IAU',
                        u_ref_link      = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf'
                       )

    AU.self_test()


    