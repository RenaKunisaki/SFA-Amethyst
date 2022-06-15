#include "main.h"

/*
static int partitionStrings(const char **items, int iStart, int iEnd) {
    const char *pivot = items[iEnd];
    const char *swap;
    int iPivot = iStart;
    for(int i=iStart; i<iEnd; i++) {
        if(strcmpi(items[i], pivot) < 0) {
            //swap items[i], items[iPivot]
            swap = items[i];
            items[i] = items[iPivot];
            items[iPivot] = swap;
            iPivot++;
        }
    }
    //swap items[iEnd], items[iPivot]
    swap = items[iEnd];
    items[iEnd] = items[iPivot];
    items[iPivot] = swap;
    return iPivot;
}

void quicksortStrings(const char **items, int iStart, int iEnd) {
    if(iStart < iEnd) {
        int iPivot = partitionStrings(items, iStart, iEnd);
        quicksortStrings(items, iStart, iPivot - 1);
        quicksortStrings(items, iPivot + 1, iEnd);
    }
}
*/

//generic quicksort

static int hackCount;
static int partition(const void **items, int iStart, int iEnd,
CompareFunc compare) {
    const char *pivot = items[iEnd];
    const char *swap;
    int iPivot = iStart;
    for(int i=iStart; i<iEnd; i++) {
        if(compare(items[i], pivot) < 0) {
            //swap items[i], items[iPivot]
            swap = items[i];
            items[i] = items[iPivot];
            items[iPivot] = swap;
            iPivot++;
        }
    }
    if(iPivot == iEnd) {
        hackCount++;
        return iPivot;
    }
    //swap items[iEnd], items[iPivot]
    swap = items[iEnd];
    items[iEnd] = items[iPivot];
    items[iPivot] = swap;
    return iPivot;
}

void quicksort_(const void **items, int iStart, int iEnd, CompareFunc compare,
int depth) {
    //hacks to prevent infinite loops with empty lists
    if(depth > 256) return;
    if(hackCount >= 16384) return;
    if(iStart < iEnd) {
        int iPivot = partition(items, iStart, iEnd, compare);
        quicksort_(items, iStart,     iPivot - 1, compare, depth+1);
        quicksort_(items, iPivot + 1, iEnd,       compare, depth+1);
    }
}

void quicksort(const void **items, int iStart, int iEnd, CompareFunc compare) {
    hackCount = 0;
    quicksort_(items, iStart, iEnd, compare, 0);
}
