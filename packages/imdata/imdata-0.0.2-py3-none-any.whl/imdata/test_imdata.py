import os
from imdata import ImData

imd = ImData()

class TestImData:
    def setup(self):
        self.b = b'some string'
        self.lb = b'a long bytes' * 100
        self.s = 'no a bytes'
        self.ls = 'a long long string' * 98

    def test_bp(self):
        pix = imd.bytes_pix(self.b)
        res = imd.pix_bytes(pix)[0]
        assert self.b == res

    def test_lbp_auto(self):
        pix = imd.bytes_pix(self.lb, 'auto')
        assert pix.shape != (400, 600, 3), "size isn't changed"
        res = imd.pix_bytes(pix)[0]
        assert res == self.lb ,"result doesn't match"

    def test_sp(self):
        pix = imd.bytes_pix(self.s)
        res = imd.pix_bytes(pix)
        assert self.s == res[0].decode() ,"result doesn't match"

    def test_tos(self):
        o = imd.to_string(self.lb)
        assert o == self.lb.decode() ,"result doesn't match, to_string error"
        p = imd.to_bytes(self.ls)
        assert p == self.ls.encode() ,"result doesn't match, to_bytes errpr"

    def test_manyb(self):
        o = [self.lb, self.s, self.b]
        res = imd.pix_bytes(imd.bytes_pix(o))
        o = [self.lb, self.s.encode(), self.b]
        assert res == o

    def test_init(self):
        simd = ImData(b'my bytes', 'tif')

        o = simd.bytes_pix(b'my bytes', 'auto')
        assert (o == simd.pix).all()
        assert simd.bytes == b'my bytes'

        op = simd.pix
        simd.bytes = b'my new bytes'
        try:
            if op.shape != simd.pix.shape:
                r = 0
            else:
                r = (op == simd.pix).all()
        except: 
            r = op == simd.pix if op.shape == simd.pix.shape else 0
        assert not r
        np = simd.pix
        
        simd.bytes = b'my old bytes'
        try:
            r = not (np == simd.pix).all()
        except:
            r = not (np == simd.pix)
        assert r
        
        try:
            simd.pix = 'pix'
            assert 0
        except:
            assert 1
        
        simd.save('test.tif')
        try:
            simd.save('error.tiff')
            assert 0
        except:
            assert 1
        
        try:
            simd.save(1)
            assert 0
        except TypeError:
            pass
        
        os.remove('test.tif')
