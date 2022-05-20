import testlib
import random, os
from ddt import file_data, ddt, data, unpack

# change this variable to True to disable timeout and enable print
DEBUG=True
DEBUG=False

WARP = 2   # test VM
WARP = 1   # your PC

import images   # preload

@ddt
class Test(testlib.TestCase):
    def do_test(self, id_file, spacing, expected, timeout):
        """Test implementation
        - file_txt:		text file containing the input matrix
        - file_png:	    png image you must write the picture inside
        - spacing:      spacing between rectangles and for the border
        - expected_png:	expected result - file png
        - expected:     expected result - image dimensions
        - timeout:      variable timeout depending on test
        """
        file_txt     = 'matrices/' + id_file + '.txt'
        file_png     = 'test_'     + id_file + '.png'
        expected_png = 'matrices/' + id_file + '.png'
        TIMEOUT = timeout * WARP   # warp factor 
        if DEBUG:
                import program01 as program
                result = program.ex(file_txt, file_png, spacing)
        else:
            with    self.ignored_function('pprint.pprint'), \
                    self.ignore_print(), \
                    self.forbidden_function('builtins.input'), \
                    self.forbidden_function('builtins.eval'), \
                    self.check_open( { file_txt: 'trt', file_png: 'bwb' } ), \
                    self.check_imports(allowed=['program01', '_io', 'images','encodings.utf_8']), \
                    self.timeout(TIMEOUT), \
                    self.timer(TIMEOUT):
                import program01 as program
                result = program.ex(file_txt, file_png, spacing)
        self.assertEqual(type(result), tuple,
                         ('The output type should be: tuple\n'
                          '[Il tipo di dato in output deve essere: tuple]'))
        self.assertEqual(len(result), 2,
                         ('The tuple should contain 2 elements\n'
                          '[La tupla deve contenere due elementi]'))
        self.assertEqual(result, expected,
                         ('The return value is incorrect\n'
                          '[Il valore di ritorno è errato]'))
        self.check_img_file(file_png, expected_png)
        os.remove(file_png)
        return 1

    @data(  # test-id    spacing   exp_dimensions   timeout
            ( 'example',   42,      ( 288, 348),     0.5),
            ( 'minimal',   30,      (  82, 140),     0.5),
            ( 'mat-3-1',    1,      ( 466, 120),     0.5),
            ( 'mat-4-5',    5,      ( 120,  61),     0.5),
            ( 'mat-5-5',    5,      ( 150,  78),     0.5),
            ( 'mat-2-97',  97,      ( 690, 341),     0.5),
            ( 'mat-23-2',   2,      ( 882, 802),     0.5),
            ( 'mat-53-1',   1,      ( 600,1748),     0.5),
            ( 'mat-12-25', 25,      (2362, 813),     1.0),
            ( 'mat-16-25', 25,      (2822,1071),     1.0),
            ( 'extra-1-6', 6,        (370, 182),     0.1),
            ( 'extra-1-32', 32,      (798, 108),     0.1),
            ( 'extra-1-49', 49,      (534, 268),     0.1),
            ( 'extra-3-0', 0,        (652, 546),     0.5),
            ( 'extra-3-40', 40,     (2498, 658),     1.0),
            ( 'extra-6-8', 8,      (3784, 1350),     3.0),
            ( 'extra-9-20', 20,    (6350, 2106),     7.5),
            ( 'extra-12-44', 44,   (8842, 3208),     15.0),
            ( 'extra-15-46', 46,  (10880, 4040),     24.0),
            ( 'extra-18-46', 46,  (13022, 4892),     35.0),
            ( 'extra-21-46', 46,  (14626, 5666),     45.0),
            ( 'extra-24-25', 25,  (15351, 5997),     50.0),
            )
    @unpack
    def test_matrici(self, id_file, spacing, expected, timeout):
        return self.do_test(id_file, spacing, expected, timeout)

    ######################### SECRET TESTS START HERE! #########################


if __name__ == '__main__':
    Test.main()

