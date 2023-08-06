cdef class LRUCache(object):

    cdef int __cacheSize
    cdef object __map

    cpdef bint contains(self, key: object)
    cpdef object get(self, key: object)
    cpdef add(self, key: object, data: object)