cdef extern from "zlib.h":
    int compress(unsigned char *dest, unsigned long *destLen, const unsigned char *source, unsigned long sourceLen)
    unsigned long compressBound(unsigned long sourceLen)