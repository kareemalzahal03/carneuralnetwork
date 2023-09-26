from math import cos, sin

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tuple(self):
        return (self.x, self.y)

    # Rotate as a vector around (0,0)
    def rotate(self, theta):
        return Point(self.x * cos(theta) - self.y * sin(theta),
                            self.x * sin(theta) + self.y * cos(theta))
        # self.x = self.x * cos(theta) - self.y * sin(theta)
        # self.y = self.x * sin(theta) + self.y * cos(theta)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
    
def LineCollision(p0, p1, p2, p3):
    s1 = (p1[0] - p0[0], p1[1] - p0[1])
    s2 = (p3[0] - p2[0], p3[1] - p2[1])
    s1xs2 = -s2[0] * s1[1] + s1[0] * s2[1]

    if s1xs2 == 0:
        return None

    s = (-s1[1] * (p0[0] - p2[0]) + s1[0] * (p0[1] - p2[1])) / s1xs2
    t = ( s2[0] * (p0[1] - p2[1]) - s2[1] * (p0[0] - p2[0])) / s1xs2

    if s >= 0 and s <= 1 and t >= 0 and t <= 1:
        return (p0[0] + t * s1[0], p0[1] + t * s1[1])
    else:
        return None

"""
// Returns 1 if the lines intersect, otherwise 0. In addition, if the lines 
// intersect the intersection point may be stored in the floats i_x and i_y.
char get_line_intersection(float p0_x, float p0_y, float p1_x, float p1_y, 
    float p2_x, float p2_y, float p3_x, float p3_y, float *i_x, float *i_y)
{
    float s1_x, s1_y, s2_x, s2_y;
    s1_x = p1_x - p0_x;     s1_y = p1_y - p0_y;
    s2_x = p3_x - p2_x;     s2_y = p3_y - p2_y;

    float s, t;
    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y);
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y);

    if (s >= 0 && s <= 1 && t >= 0 && t <= 1)
    {
        // Collision detected
        if (i_x != NULL)
            *i_x = p0_x + (t * s1_x);
        if (i_y != NULL)
            *i_y = p0_y + (t * s1_y);
        return 1;
    }
    return 0; // No collision
}

"""