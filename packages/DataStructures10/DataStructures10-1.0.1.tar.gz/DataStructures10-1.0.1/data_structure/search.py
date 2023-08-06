def linearSearch(values, search_for):
    search_at = 0
    search_res = False

    # Match the value with each data element
    while search_at < len(values) and search_res is False:
        if values[search_at] == search_for:
            search_res = True

        else:
            search_at = search_at + 1
    if search_res == True:
        return "Found " + str(search_for) + " at index " + str(search_at)

    else:
        return "Element not found"


def binarySearch(values, x):
    idx0 = 0
    idxn = (len(values) - 1)

    while idx0 <= idxn and values[idx0] <= x <= values[idxn]:

        # Find the mid point
        mid = idx0 + \
              int(((float(idxn - idx0) / (values[idxn] - values[idx0]))
                   * (x - values[idx0])))

        # Compare the value at mid point with search value
        if values[mid] == x:
            return "Found " + str(x) + " at index " + str(mid)

        if values[mid] < x:
            idx0 = mid + 1
    return "Searched element not in the list"
