"""
originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation
"""
# pylint: disable=C0301,C0103
from .config import po
from .base import DSheet, DBook
try:
    import numpy as np
except ImportError:
    pass

class MSheet(DSheet):
    """
    This class represents an Origin Matrix Sheet, it holds an instance of a PyOrigin MatrixSheet.
    """
    try:
        _npdtype_to_orgdtype = {
            np.float64: po.DF_DOUBLE,
            np.float32: po.DF_FLOAT,
            np.int16: po.DF_SHORT,
            np.int32: po.DF_LONG,
            np.int8: po.DF_CHAR,
            np.uint8: po.DF_BYTE,
            np.uint16: po.DF_USHORT,
            np.uint32: po.DF_ULONG,
            np.complex128: po.DF_COMPLEX,
        }
        _orgdtype_to_npdtype = {v: k for k, v in _npdtype_to_orgdtype.items()}
    except NameError:
        pass

    def get_book(self):
        """
        Returns parent book of sheet.

        Parameters:

        Returns:
            (MBook)

        Examples:
            mb = ma.get_book().add_sheet()
        """
        return MBook(self._get_book())

    @property
    def depth(self):
        """
        return the number of matrix objects in the matrix sheet

        Examples:

        >>>ms = op.find_sheet('m')
        >>>ms.depth
        """
        return self.obj.GetNumMats()

    @depth.setter
    def depth(self, z):
        """
        set the number of matrix objects in the matrix sheet

        Examples:

        ms=op.new_sheet('m', hidden=True)
        ms.depth = 100
        print(ms.depth)
        """
        self.obj.SetNumMats(z)
        return self.obj.GetNumMats()

    def from_np(self, arr, dstack=False):
        """
        Set a matrix sheet data from a multi-dimensional numpy array. Existing data and MatrixObjects will be deleted.

        Parameters:
            arr (numpy array): 2D for a single MatrixObject, and 3D for multiple MatrixObjects (rows, cols, N)
            dstack (bool):   True if arr as row,col,depth, False if depth,row,col
        Returns:
            None

        Examples:
            ms = op.new_sheet('m')
            arr = np.array([[[1, 2, 3], [4, 5, 6]], [[11, 12, 13], [14, 15, 16]]])
            ms.from_np(arr)
        """
        dfmt = self._npdtype_to_orgdtype.get(arr.dtype.type)
        if dfmt is None:
            raise ValueError('Array Data Type not supported')
        if arr.ndim < 2:
            raise ValueError('1D array not supported')
        if arr.ndim == 2:
            row,col = arr.shape
            mat = self.obj.MatrixObjects(0)
            mat.DataFormat = dfmt
            self.shape = row,col
            ret = mat.SetData(arr)
            if ret == 0:
                print('matrix set data error')
            return
        if arr.ndim != 3:
            raise ValueError('array greater then 3D not supported')
        if dstack:
            rows, cols, depth = arr.shape
        else:
            depth, rows, cols = arr.shape
        self.depth = depth
        self.shape = rows, cols
        for i in range(depth):
            mo = self.obj[i]
            mo.DataFormat = dfmt
            if dstack:
                mo.SetData(arr[:,:,i])
            else:
                mo.SetData(arr[i])

    def to_np2d(self, index=0, order='C'):
        """
        Transfers data from a single MatrixObject to a numpy 2D array.

        Parameters:
            index (int): MatrixObject index in the MatrixLayer
            order (str): Order of numpy array. 'C' for C-style row major order, 'F' for Fortran-style column major order

        Returns:
            (numpy array) 2D

        Examples:
            arr = ms.to_np2d(0)
            print(arr)
            arr = ms.to_np2d(0, 'R')
            print(arr)
        """
        mo = self.obj.MatrixObjects(index)
        return np.asarray(mo.GetData(), self._orgdtype_to_npdtype[mo.DataFormat], order)

    def to_np3d(self, dstack=False, order='C'):
        """
        Transfers data from a MatrixSheet to a numpy 3D array.

        Parameters:
            dstack (bool): True output arrays as row,col,depth, False if depth,row,col
            order (str): Order of numpy array. 'C' for C-style row major order, 'F' for Fortran-style column major order

        Returns:
            (numpy array) 3D

        Examples:
            arr=[]
            for i in range(10):
                tmp = np.arange(1,13).reshape(3,4)
                arr.append(tmp*(i+1))
            aa = np.dstack(arr)
            print(aa.shape)
            ma = op.new_sheet('m')
            ma.from_np(aa, True)

            bb = ma.to_np3d()
            print(bb.shape)
            mb = op.new_sheet('m')
            mb.from_np(bb)

            cc = ma.to_np3d(True)
            print(cc.shape)
            mc = op.new_sheet('m')
            mc.from_np(cc)
            mc.show_thumbnails()
        """
        m2d = []
        for mo in self.obj.MatrixObjects:
            m2d.append(np.asarray(mo.GetData(), self._orgdtype_to_npdtype[mo.DataFormat], order))
        if dstack:
            return np.dstack(m2d)
        return np.array(m2d)

    def show_image(self, show = True):
        """
        Show MatrixObjects as images or as numeric values.

        Parameters:
            show (bool): If True, show as images

        Returns:
            None

        Examples:
            ms.show_image()
            ms.show_image(False)
        """
        self.set_int("Image", show)

    def __show_contrll(self, show, slider):
        mbook = self.obj.GetParent()
        if not show:
            mbook.SetNumProp("Selector", 0)
        else:
            mbook.SetNumProp("Selector", 1)
            mbook.SetNumProp("Slider", slider)

    def show_thumbnails(self, show = True):
        """
        Show thumbnail images for a MatrixObjects.

        Parameters:
            show (bool): If True, show thumbnails

        Returns:
            None

        Examples:
            ms.show_thumbnails()
            ms.show_thumbnails(False)
        """
        self.__show_contrll(show, 0)


    def show_slider(self, show = True):
        """
        Show image slider for MatrixObjects.

        Parameters:
            show (bool): If True, show slider

        Returns:
            None

        Examples:
            mat.show_slider()
            mat.show_slider(False)
        """
        self.__show_contrll(show, 1)

class MBook(DBook):
    """
    This class represents an Origin Matrix Book, it holds an instance of a PyOrigin MatrixPage.
    """
    def _sheet(self, obj):
        return MSheet(obj)

    def add_sheet(self, name='', active=True):
        """
        add a new matrix sheet to the matrix book

        Parameters:
            name (str): the name of the new sheet. If not specified, default names will be used
            active (bool): Activate the newly added sheet or not

        Return:
            (MSheet)

        Examples:
            mb = ma.get_book().add_sheet('Dot Product')
            print(mb.shape)
        """
        return MSheet(self._add_sheet(name, active))

    def show_image(self, show = True):
        """
        similar to MSheet, but set all sheets in matrix book

        Parameters:
            show (bool): If True, show as images

        Returns:
            None

        Examples:
            mb = op.find_book('m', 'MBook1')
            mb.show_image()
        """
        self.set_int("Image", show)
