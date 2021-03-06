:Description: This model is used in the reference(s) here below.
    The network was generated manually from the paper. 
:Model: The model is available in SIF format (**PKN-ToyPCB.sif**) and SBML-qual format 
    (**PKN-ToyPCB.xml**) available from **cnodata**. See code below.
:Data: The data in MIDAS format is **MD-ToyPCB.csv**. 
    The data was generated manually.

.. image:: https://github.com/cellnopt/cellnopt/blob/master/cno/datasets/ToyPCB/ToyPCB.png
   :alt: ToyPCB figure

.. code-block:: python

    from cno import cnodata, CNOGraph
    c = cnograph.CNOGraph(cnodata("PKN-ToyPCB.sif"), cnodata("MD-ToyPCB.csv"))
    c.plot()


References
-------------

.. [1] **Morris, Melody K and Saez-Rodriguez, Julio and Clarke, David C and Sorger, Peter K and Lauffenburger, Douglas a**,
   *Training signaling pathway maps to biochemical data with constrained fuzzy logic: quantitative analysis of liver cell responses to inflammatory stimuli.*
   PLoS computational biology, 7, 3, 2011
   `Citation <http://www.pubmedcentral.nih.gov/articlerender.fcgi?artid=3048376>`_
