import math
        

class Vector(tuple):
    '''A vector representation.'''
    
    def __init__(self, iterable):
        super(Vector, self).__init__(iterable)

    @property
    def length(self):
        return self.dot(self) ** 0.5
    
    @property
    def unit(self):
        try:
            return self / self.length
        except:
            return self * 0

    def __add__(self, other):
        return Vector([i + j for i, j in zip(self, other)])

    def __sub__(self, other):
        return Vector([i - j for i, j in zip(self, other)])

    def __mul__(self, scalar):
        return Vector([scalar * i for i in self])

    def __rmul__(self, scalar):
         return Vector([scalar * i for i in self])

    def __div__(self, scalar):
        return Vector([i / scalar for i in self])

    def __neg__(self):
        return Vector([-i for i in self])

    def __mod__(self, scalar):
        return Vector([i % scalar for i in self])

    def __pow__(self, exponent):
        return Vector([i ** exponent for i in self])

    def angle(self, other):
        '''Get the angle between this vector and another.'''
        return math.acos(self.dot(other) / (self.length * other.length))

    def dot(self, other):
        '''Get the dot product with another vector.'''
        return sum([i * j for i, j in zip(self, other)])

    def distance_to(self, other):
        '''Get the distance to another vector.'''
        return (self - other).length

class Euclidian(tuple):
    def __init__(self, origin, magnitude, direction):
        self.origin = origin
        self.magnitude = magnitude
        self.direction = direction

    def angle(self, other):
        return self.direction - other.direction
