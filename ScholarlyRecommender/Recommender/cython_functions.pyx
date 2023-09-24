# cython_functions.pyx
import gzip
import numpy as np
cimport numpy as np
from cpython cimport array
import array

def calculate_ncd(np.ndarray[object, ndim=1] test_texts, np.ndarray[object, ndim=1] train_texts):
    cdef int i, j
    cdef int num_test = len(test_texts)
    cdef int num_train = len(train_texts)
    cdef np.ndarray[np.float64_t, ndim=2] ncd_results = np.zeros((num_test, num_train), dtype=np.float64)

    for i in range(num_test):
        x1 = test_texts[i]
        Cx1 = len(gzip.compress(x1.encode()))
        
        for j in range(num_train):
            x2 = train_texts[j]
            Cx2 = len(gzip.compress(x2.encode()))
            
            x1x2 = " ".join([x1, x2])
            Cx1x2 = len(gzip.compress(x1x2.encode()))
            
            ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)
            ncd_results[i, j] = ncd  # Store the individual NCD value
    
    return ncd_results

