cdef class CounterHashMap(dict):

    cpdef put(self, object key)
    cpdef putNTimes(self, object key, int N)
    cpdef int count(self, object key)
    cpdef int sumOfCounts(self)
    cpdef object max(self, double threshold = *)
    cpdef add(self, CounterHashMap toBeAdded)
    cpdef list topN(self, int N)