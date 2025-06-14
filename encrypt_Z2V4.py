mul_in_V4 = [
    [0 , 1 , 2 , 3] ,
    [1 , 0 , 3 , 2] ,
    [2 , 3 , 0 , 1] ,
    [3 , 2 , 1 , 0] ,
]

def function_mul_in_V4 (a , b ) :
    return mul_in_V4 [ a ][ b ]

add_table = [[0 for i in range (16) ] for i in range (16) ]
mul_table = [[0 for i in range (16) ] for i in range (16) ]

# Pre - compute tables for \(\ mathbb {Z}_2 V_4 \) algebra
for i in range (16) :
    for j in range (16) :
      a = bin( i ) [2:]. zfill (4)
      b = bin( j ) [2:]. zfill (4)

      # Addition
      x = [( int( a [ k ]) + int( b [ k ]) ) % 2 for k in range (4) ]
      x_str = "". join ([ str( val ) for val in x ])
      add_table [ i ][ j ] = int( x_str , 2)

      # Multiplication
      y = [0] * 4
      for k in range (4) : # iterate through basis of first element
          for l in range (4) : # iterate through basis of second element
              if int ( a [ k ]) * int (b [ l ]) != 0:
                  res = function_mul_in_V4 (k , l )
                  y [ res ] += 1
      y_mod2 = [ val % 2 for val in y ]
      mul_table [ i ][ j ] = int("". join ([ str( val ) for val in y_mod2 ]) , 2)

# Generator matrix structure ( simplified from report )
# In the report , this is a very large 2 x256 matrix of ring elements .
G1 = [ i for i in range (16) ]
G2_part1 = ( G1 * 16) [:256]
G2_part2 = [ i // 16 for i in range (256) ]
G2 = [ G2_part1 , G2_part2 ]

# --- Encryption ---
c = input (" Enter a character to encrypt : ")
if not c : c = 'Y'
else : c = c [0]
expr = bin( ord( c ) ) [2:]. zfill (8)
elems = [int( expr [:4] , 2) , int( expr [4:] , 2) ]

encoded = [0] * len ( G2 [0])
print ( f" Encrypting ’{c} ’ -> { expr } -> { elems }")

for i in range (len ( G2 [0]) ) :
    # message_part_1 * G_col_1 + message_part_2 * G_col_2
    a = mul_table [ elems [0]][ G2 [0][ i ]]
    b = mul_table [ elems [1]][ G2 [1][ i ]]
    encoded [ i ] = add_table [ a ][ b ]

print ("\ nEncoded word (256 - bit vector represented as integers 0 -15):")
print ( encoded )
