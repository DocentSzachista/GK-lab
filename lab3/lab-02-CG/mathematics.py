import math


def count_verticles_coordinates( v, u) -> list:
   # if ( v <=1 and u <=1 ) and (v>0 and u >0) :
        x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos( math.pi*v)
        y = 160 * u**4 - 320 * u**3 + 160 * u**2
        z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin( math.pi*v)
        return [x, y, z]
  #  else:
   #     print("At least one of the parameters was given wrongly. Please, make sure that both u, v are in range (0,1) ")
def generate_egg(n):
    array = [[[0 for k in range(n)] 
                 for i in range(n)] 
                 for j in range(3)]
    help = 0
    for u, v in zip(range(0, 1, n/3), range(1,0,n/3)):
        array [help] = count_verticles_coordinates(u, v)
        help+=1
    print(array)
generate_egg(4)