cdef class CounterHashMap(dict):

    def __init__(self, **kwargs):
        """
        A constructor which calls its super.
        """
        super().__init__(kwargs)

    def __str__(self)-> str:
        """
        The __str__ method loops through the mappings contained in this map and returns the string of each entry's key
        and value.

        RETURNS
        -------
        str
            String of the each entry's key and value.
        """
        result = ""
        for key in self.keys():
            result += key + " " + self[key].__str__() + "\n"
        return result

    cpdef put(self, object key):
        """
        The put method takes a object type input. If this map contains a mapping for the key, it puts this key after
        incrementing its value by one. If his map does not contain a mapping, then it directly puts key with the value
        of 1.

        PARAMETERS
        ----------
        key : object
            key to put.
        """
        if key in self:
            self[key] = self[key] + 1
        else:
            self[key] = 1

    cpdef putNTimes(self, object key, int N):
        """
        The putNTimes method takes an object and an integer N as inputs. If this map contains a mapping for the key, it
        puts this key after incrementing its value by N. If his map does not contain a mapping, then it directly puts
        key with the value of N.

        PARAMETERS
        ----------
        key : object
            key to put.
        N : int
            to increment value.
        """
        if key in self:
            self[key] += N
        else:
            self[key] = N

    cpdef int count(self, object key):
        """
        The count method takes an object as input, if this map contains a mapping for the key, it returns the value
        corresponding this key, 0 otherwise.

        PARAMETERS
        ----------
        key : object
            key to get value.

        RETURNS
        -------
        int
            the value corresponding given key, 0 if it is not mapped.
        """
        if key in self:
            return self[key]
        else:
            return 0

    cpdef int sumOfCounts(self):
        """
        The sumOfCounts method loops through the values contained in this map and accumulates the counts of this values.

        RETURNS
        -------
        int
            accumulated counts.
        """
        cdef int total
        total = 0
        for key in self:
            total += self[key]
        return total

    cpdef object max(self, double threshold = 0.0):
        """
        The max method takes a threshold as input and loops through the mappings contained in this map.
        It accumulates the count values and if the current entry's count value is greater than maxCount, which is
        initialized as 0, it updates the maxCount as current count and maxKey as the current count's key.
        At the end of the loop, if the ratio of maxCount/total is greater than the given threshold it returns maxKey,
        else None.

        PARAMETERS
        ----------
        threshold : float
            threshold float value.

        RETURNS
        -------
        object
            object type maxKey if greater than the given threshold, None otherwise.
        """
        cdef int maxCount, total
        maxCount = 0
        total = 0
        maxKey = None
        for key in self:
            total += self[key]
            if self[key] > maxCount:
                maxCount = self[key]
                maxKey = key
        if maxCount / total > threshold:
            return maxKey
        else:
            return None

    cpdef add(self, CounterHashMap toBeAdded):
        """
        The add method adds value of each key of toBeAdded to the current counterHashMap.

        PARAMETERS
        ----------
        toBeAdded : CounterHashMap
            CounterHashMap to be added to this counterHashMap.
        """
        for value in toBeAdded:
            self.putNTimes(value, toBeAdded[value])

    cpdef list topN(self, int N):
        """
        The topN method takes an integer N as inout. It creates an list result and loops through the the
        mappings contained in this map and adds each entry to the result list. Then sort this list
        according to their values and returns a list which is a sublist of result with N elements.

        PARAMETERS
        ----------
        N : int
            integer value for defining size of the sublist.

        RETURNS
        -------
        list
            a sublist of N element.
        """
        cdef list result
        result = []
        for key in self:
            result.append([self[key], key])
        result.sort(reverse=True)
        return result[0:N]
