from cno.boolean import Steady
from cno import cnodata
from numpy import array
import numpy

def test_steady():


    s = Steady(cnodata("PKN-ToyMMB.sif"), cnodata("MD-ToyMMB.csv"))



    s.simulate(1) 
    s.score()
    # pd.DataFrame(s.diff/2.)[[0,2,4,1,6,3,5]] # this order is the one to 
    # identical to R. Need to check that

    # we can check the scorei

        
        
    solutions = {'Akt': array([1, 1, 1, 1, 1, 1, 0, 0, 0]),
         'EGF': array([1, 0, 1, 1, 0, 1, 1, 0, 1]),
          'Erk': array([1, 0, 1, 0, 0, 0, 1, 1, 1]),
           'Hsp27': array([1, 1, 1, 0, 1, 1, 1, 1, 1]),
            'Jnk': array([0, 1, 1, 0, 1, 1, 0, 1, 1]),
             'Mek': array([1, 0, 1, 0, 0, 0, 1, 1, 1]),
              'NFkB': array([0, 1, 1, 0, 1, 1, 0, 1, 1]),
               'PI3K': array([1, 1, 1, 1, 1, 1, 0, 0, 0]),
                'Raf': array([1, 0, 1, 0, 0, 0, 1, 0, 1]),
                 'Ras': array([1, 0, 1, 1, 0, 1, 1, 0, 1]),
                  'TNFa': array([0, 1, 1, 0, 1, 1, 0, 1, 1]),
                   'TRAF6': array([0, 1, 1, 0, 1, 1, 0, 1, 1]),
                    'cJun': array([0, 1, 1, 0, 1, 1, 0, 1, 1]),
                     'p38': array([0, 1, 1, 0, 1, 1, 0, 1, 1]),
                      'p90RSK': array([1, 0, 1, 0, 0, 0, 1, 1, 1])}

    for k in s.values.keys():
        assert numpy.all(solutions[k] == s.values[k])

    assert s.score()/2. == 0.094674603174603175

    """
[,1]  [,2]   [,3] [,4]   [,5]    [,6] [,7]
[1,] 0.00405 0.500 0.3698 0.02 0.0072 0.00000 0.00
[2,] 0.01620 0.045 0.0050 0.00 0.0000 0.28125 0.18
[3,] 0.00405 0.045 0.0050 0.02 0.0072 0.28125 0.18
[4,] 0.00405 0.000 0.3698 0.00 0.0000 0.00000 0.00
[5,] 0.01620 0.045 0.0050 0.00 0.0000 0.28125 0.18
[6,] 0.00405 0.045 0.0050 0.00 0.0000 0.28125 0.18
[7,] 0.00000 0.500 0.0000 0.02 0.0072 0.00000 0.00
[8,] 0.00000 0.045 0.0050 0.50 0.5000 0.28125 0.18
[9,] 0.00000 0.045 0.0050 0.02 0.0072 0.28125 0.18

$simResults[[1]]$t0
[,1] [,2] [,3] [,4] [,5] [,6] [,7]
[1,]    0    0    0    0    0    0    0
[2,]    0    0    0    0    0    0    0
[3,]    0    0    0    0    0    0    0
[4,]    0    0    0    0    0    0    0
[5,]    0    0    0    0    0    0    0
[6,]    0    0    0    0    0    0    0
[7,]    0    0    0    0    0    0    0
[8,]    0    0    0    0    0    0    0
[9,]    0    0    0    0    0    0    0

s.score()
pd.DataFrame(s.diff/2.)[[0,2,4,1,6,3,5]]

     Akt Hsp27 NFkB Erk p90RSK Jnk cJun
     [,1] [,2] [,3] [,4] [,5] [,6] [,7]
     [1,]    1    1    0    1    1    0    0
     [2,]    1    1    1    0    0    1    1
     [3,]    1    1    1    1    1    1    1
     [4,]    1    0    0    0    0    0    0
     [5,]    1    1    1    0    0    1    1
     [6,]    1    1    1    0    0    1    1
     [7,]    0    1    0    1    1    0    0
     [8,]    0    1    1    1    1    1    1
     [9,]    0    1    1    1    1    1    1

     """

    """assert numpy.all(s.diff/2. ==  \
    array([[ 0.00405,  0.02   ,  0.5    ,  0.     ,  0.3698 ,  0.     ,  0.0072 ],
        [ 0.0162 ,  0.     ,  0.045  ,  0.28125,  0.005  ,  0.18   ,  0.     ],
        [ 0.00405,  0.02   ,  0.045  ,  0.28125,  0.005  ,  0.18   ,  0.0072 ],
        [ 0.00405,  0.     ,  0.     ,  0.     ,  0.3698 ,  0.     ,  0.     ],
        [ 0.0162 ,  0.     ,  0.045  ,  0.28125,  0.005  ,  0.18   ,  0.     ],
        [ 0.00405,  0.     ,  0.045  ,  0.28125,  0.005  ,  0.18   ,  0.     ],
        [ 0.     ,  0.02   ,  0.5    ,  0.     ,  0.     ,  0.     ,  0.0072 ],
        [ 0.     ,  0.5    ,  0.045  ,  0.28125,  0.005  ,  0.18   ,  0.5    ],
        [ 0.     ,  0.02   ,  0.045  ,  0.28125,  0.005  ,  0.18   ,  0.0072 ]]))"""
