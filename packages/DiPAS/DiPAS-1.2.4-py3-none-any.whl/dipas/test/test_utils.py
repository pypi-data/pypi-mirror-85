import unittest

from dipas.utils import get_type_hints_with_boundary


class TestGetTypeHintsWithBoundary(unittest.TestCase):
    def test(self):
        class A:
            a: int

        class B(A):
            b: int

        class C(B):
            c: int

        self.assertSequenceEqual(list(get_type_hints_with_boundary(C)), ['a', 'b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=object)), ['a', 'b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=A)), ['a', 'b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=B)), ['b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=C)), ['c'])


if __name__ == '__main__':
    unittest.main()
