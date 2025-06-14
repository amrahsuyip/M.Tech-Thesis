import itertools
import random
from itertools import permutations
import numpy as np

G = list ( itertools . permutations ([1 , 2 , 3 , 4]) )

def mul (a , b ) :
    A = np . array ( a ) - 1
    B = np . array ( b ) - 1
    C = tuple ( B [ A ] + 1)
    return C

def add (a , b ) :
    res = [0 for i in range (len ( a ) ) ]
    for i in range (len ( a ) ) :
        res [ i ] = ( a [ i ] + b [ i ]) % 5
    return tuple ( res )

def mul_in_F_5_S_4 (a , b , uniq = False ) :
    res = [0 for i in range (len ( a ) ) ]
    st = set ()
    for i in range (len ( a ) ) :
        for j in range (len( b ) ) :
            if a [ i ] * b [ j ] == 0:
                  continue
            elem = mul ( G [ i ] , G [ j ])
            idx = G . index ( elem )
            if idx in st and uniq :
                  raise ValueError
            st . add ( idx )
            res [ idx ] += a [ i ] * b [ j ]
            res [ idx ] %= 5
    return tuple ( res )

def isZero ( Z ) :
    for i in Z :
        if max( i ) != min( i ) != 0:
            return False
    return True

# idempotents of F5 -S4.
# computed through another algorithm .
e = [
    (4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4) ,
    (4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4) ,
    (1 , 0 , 0 , 2 , 2 , 0 , 0 , 1 , 2 , 0 , 0 , 2 , 2 , 0 , 0 , 2 , 1 , 0 , 0 , 2 , 2 , 0 , 0 , 1) ,
    (1 , 3 , 3 , 0 , 0 , 3 , 3 , 3 , 0 , 2 , 2 , 0 , 0 , 2 , 3 , 0 , 3 , 2 , 2 , 0 , 0 , 3 , 2 , 3) ,
    (1 , 2 , 2 , 0 , 0 , 2 , 2 , 3 , 0 , 3 , 3 , 0 , 0 , 3 , 2 , 0 , 3 , 3 , 3 , 0 , 0 , 2 , 3 , 3) ,
]

received_word = (2 , 1 , 4 , 1 , 1 , 4 , 0 , 0 , 1 , 1 , 3 , 4 , 1 , 3 , 4 , 4 , 1 , 1 , 1 , 4 , 4 , 0 , 4 , 2)
S = [ mul_in_F_5_S_4 ( received_word , e [ i ]) for i in range (4) ]

if isZero ( S ) :
    print ("The received word is correct .")

def C (i , h ) :
    x = [0 for k in range (24) ]
    x [ i ] = 1
    return mul_in_F_5_S_4 (x , e [ h ] , uniq = True )

while True :
      P , Q , R , SS = [] , [] , [] , []
      id0 = random . randint (0 , len ( G ) - 1)
      id1 = random . randint (0 , len ( G ) - 1)
      id2 = random . randint (0 , len ( G ) - 1)
      SS = []
      if id0 == id1 or id1 == id2 or id0 == id2 :
          continue
      for h in range (4) :
          temp = C ( id0 , h )
          P += temp
          temp = C ( id1 , h )
          Q += temp
          temp = C ( id2 , h )
          R += temp
      SS += S [ h ]
      for i in range (5) :
          for j in range (5) :
              for k in range (5) :
                  check = True
                  for x in range (len ( P ) ) :
                      if ( i * P [ x ] + j * Q [ x ] + k * R [ x ]) % 5 != SS [ x ]:
                          check = False
                          break
                      if check and abs ( i) + abs( j ) + abs( k ) != 0:
                          print (" Error found ")
                          print (
                      f"""
                      {i} units at index {id0 +1}
                      {j} units at index {id1 +1}
                      {k} units at index {id2 +1}
                      """
                      )
                      corrected_word = list ( received_word )
                      corrected_word [ id0 ] += 5 - i
                      corrected_word [ id1 ] += 5 - j
                      corrected_word [ id2 ] += 5 - k
                      corrected_word = tuple (
                          [ corrected_word [ i ] % 5 for i in range (len(
                              corrected_word ) ) ]
                      )
                      print (" corrected_word : ", corrected_word )
                      exit (0)
