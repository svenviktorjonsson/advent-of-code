import numpy as np

class CArray(np.ndarray):
    """Numpy Array wrapper supporting complex and ArrayLike[complex] get- and set-item arguments
    
    The real axis is the first axis of the array and the imag axis is the second axis of the array.
    """

    def __getitem__(self, arg):
        return super().__getitem__(self._convert_if_complex(arg))

    def __setitem__(self, arg, value):
        return super().__setitem__(self._convert_if_complex(arg),value)

    def _convert_if_complex(self, arg):
        if isinstance(arg, slice) and any(isinstance(a,complex) for a in (arg.start,arg.stop,arg.step)):
            start = 0j if arg.start is None else arg.start+0j
            stop = complex(*self.shape) if arg.stop is None else arg.stop+0j
            zs = start + np.arange(0,np.abs(stop-start),arg.step)*np.exp(1j*np.angle(stop-start))
            return np.real(zs).astype(int),np.imag(zs).astype(int)
        if isinstance(arg,complex):
            return int(arg.real),int(arg.imag)
        if isinstance(arg,np.ndarray) and arg.size and isinstance(arg[0],complex):
            return np.real(arg).astype(int),np.imag(arg).astype(int)
        if isinstance(arg,list):
            return self._convert_if_complex(np.array(arg))
        return arg


if __name__=="__main__":
    a = np.full((10,10),".").view(CArray)
    a[[1j,5j,2+7j]] = "#"
    a[3:10+7j] = "2"
    a[0j:] = "D"
    a[-1-2j] = "E"

    for row in a:
        print(" ".join(row))

    #output
    # --> is the imag axis
    # |
    # v is the real axis
    """
    D # . . . # . . . .
    . D . . . . . . . .
    . . D . . . . # . .
    2 . . D . . . . . .
    . 2 . . D . . . . .
    . . 2 . . D . . . .
    . . . 2 . . D . . .
    . . . . 2 . . D . .
    . . . . . 2 . . D .
    . . . . . . 2 . E D
    """