import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free
from libc.string cimport strcat, strcpy
from cython.parallel cimport prange

cdef extern from "zlib.h":
    int compress(unsigned char *dest, unsigned long *destLen, const unsigned char *source, unsigned long sourceLen)
    unsigned long compressBound(unsigned long sourceLen)

def calculate_ncd(np.ndarray[object, ndim=1] test_texts, np.ndarray[object, ndim=1] train_texts):
    cdef int i, j
    cdef int num_test = test_texts.shape[0]
    cdef int num_train = train_texts.shape[0]
    cdef np.ndarray[np.float64_t, ndim=2] ncd_results = np.zeros((num_test, num_train), dtype=np.float64)
    cdef unsigned long Cx1, Cx2, Cx1x2
    cdef bytes x1, x2, x1x2
    
    for i in range(num_test):
        x1 = test_texts[i].encode('utf-8')
        Cx1 = compress_c(x1)
        
        for j in range(num_train):
            x2 = train_texts[j].encode('utf-8')
            Cx2 = compress_c(x2)
            
            x1x2 = x1 + b" " + x2  # Use bytes concatenation
            Cx1x2 = compress_c(x1x2)
            
            ncd_results[i, j] = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)
    
    return ncd_results

cdef unsigned long compress_c(bytes input_str):
    cdef unsigned long source_len = len(input_str)
    cdef unsigned long max_compressed_len = compressBound(source_len)
    cdef unsigned char *compressed_data = <unsigned char *>malloc(max_compressed_len)
    cdef unsigned long compressed_len = max_compressed_len
    
    if compress(compressed_data, &compressed_len, <unsigned char *>input_str, source_len) != 0:
        # Handle compression error
        return 0
    
    free(compressed_data)
    return compressed_len



