from cellnopt.core import cnodata
from cellnopt.feeder import Feeder



def test_feeder():

    f = Feeder()
    pknmodel = cnodata("PKN-ToyMMB.sif")
    midas = cnodata("MD-ToyMMB.csv")

    f.run(model=pknmodel, data=midas)
    f.newlinks
    f.summary()

