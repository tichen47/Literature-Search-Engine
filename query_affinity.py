from scipy import spatial
import numpy as np
import sys
# a, b
def get_distance(a, b):
    return 1 - spatial.distance.cosine(a, b)

# infile: trained embedding file, invec: the query vector
# return the top 3 cloest vector of the input vector
def get_top_3(infile, invec):
    ans= []
    # min1<=min2<=min3= 3 cloest vector to invec
    min1=2147483647
    min2=2147483647
    min3=2147483647
    # name of min1, 2, 3: authors or venues
    min1s= ""
    min2s=""
    min3s=""
    f= open(infile, "r")
    a=f.readline()
    lnum=1
    for line in f:
        lnum=lnum+1
        print(lnum)
        v= line.split()
        name= v.pop(0)
        v= np.array(v).astype(np.float)
        dist= get_distance(v, invec)
        if(dist<min1):
            min2= min1
            min3= min2
            min2s= min1s
            min3s= min2s
            min1= dist
            min1s=name

        if(dist>min1 and dist<min2):
            min3=min2
            min3s=min2s
            min2=dist
            min2s=name

        if(dist>min2 and dist<min3):
            min3= dist
            min3s= name

    return [min1s, min2s, min3s]



ins= "0.003127 0.003453 -0.002992 -0.002561 0.001068 0.002360 0.000735 0.000165 -0.002815 0.001733 -0.003403 0.000976 -0.000587 -0.000748 -0.002590 -0.001470 0.002015 0.002364 0.002320 0.001248 0.001207 -0.002971 -0.003200 0.003883 0.002970 0.002414 -0.000472 0.003137 -0.000387 0.000574 -0.000117 -0.002331 0.001025 -0.001045 -0.002989 0.003714 0.003421 -0.000856 -0.000177 0.000398 -0.002842 -0.003131 0.003558 0.000049 -0.002017 -0.002377 -0.002403 0.001326 0.000157 0.001040 -0.003292 -0.002975 -0.000102 0.000893 0.001992 -0.002477 0.003187 0.000724 0.000875 -0.000475 0.002333 -0.001787 -0.001639 0.001686 -0.000588 0.000805 0.001410 -0.003194 -0.001549 0.002276 0.003306 0.003072 -0.002380 -0.001647 -0.000710 0.001564 -0.002960 0.002342 0.002178 -0.001249 -0.001212 -0.001749 0.003304 0.003056 -0.000922 0.003293 0.003766 0.001418 0.003893 -0.002431 -0.001197 -0.001646 -0.002271 0.002199 0.001234 0.000332 -0.001714 0.001191 0.002390 0.000151 0.001781 -0.003869 0.003371 0.000375 -0.001431 -0.001628 -0.000584 -0.002293 -0.003414 -0.002216 0.003341 -0.001383 -0.002093 0.001810 -0.001331 0.003716 -0.001254 -0.003585 0.002122 -0.000058 -0.002726 0.000762 0.001127 -0.000376 0.001425 -0.003092 0.000688 0.001419"
inv= np.array(ins.split()).astype(np.float)
print(get_top_3("metapath2vec/out_aminer/m2vpp.aminer2017.w1000.l100.txt.size128.window7.negative5.txt", inv))

