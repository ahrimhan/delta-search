import numpy as np
import scipy.sparse as sp
import numpy.matlib as ml


member = sp.csr_matrix([[1, 0], [0, 1], [0, 1]], dtype=int)
link = sp.csr_matrix([[0, 1, 1], [0, 0, 1], [1, 0, 0]], dtype=int)

methodsum = member.sum(0)
membersum = methodsum.repeat(3, 0)

linksum = link.sum(1).repeat(2, 1)

intersect = link * member

union = sp.csr_matrix(membersum + linksum - intersect - member, dtype=float)

print "intersect"
print intersect

print "union"
print union

distance = 1 - (intersect / union).todense()

print "distance"
print distance

distancesum = sp.csr_matrix(distance.sum(0), dtype=float)
print "distance sum"
print distancesum.todense()

print "method sum"
print methodsum

distancesum_other = ml.repmat([distance.sum()], 1, 2) - distancesum
print "distance sum other"
print distancesum_other

entityCount_other = ml.repmat([3], 1, 2) - methodsum
print "entity count other"
print entityCount_other

epcMatrix = distancesum.multiply(entityCount_other) / methodsum /distancesum_other

print np.squeeze(np.asarray(epcMatrix)).tolist()

total = 0
n = 34
for idx1 in xrange(0, n - 1):
    for idx2 in xrange(idx1 + 1, n):
        total = total + 1

print "total: %d, %d" % (total, total*2)
print (n * (n-1)) / 2.0


