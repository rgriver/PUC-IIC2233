import unittest
import commands
import errors
import interpretation

class AssertsTest(unittest.TestCase):

    def test_assign(self):
        self.assertRaises(TypeError, commands.assign)

    def test_filter(self):
        self.assertEqual([423, 2444], commands.filter_column(
            [12, 423, 2444, 1],
            ">=",
            100
        ))

    def test_mean(self):
        self.assertEquals(75.75, commands.mean([12, 234, 23, 34]))
        self.assertEqual(2, commands.mean([1, 2, 3]))
        self.assertEqual(137.5, commands.mean([234, 234, 68, 14]))

    def test_median(self):
        self.assertEqual(3.5, commands.median([1, 2, 3, 4, 5, 6]))
        self.assertEqual(215, commands.median([34, 66, 215, 215, 235, 542]))
        self.assertEqual(1684.5, commands.median([34, 36, 3333, 99989]))

    def test_var(self):
        self.assertEqual(round(15287734/3, 4),
                         round(commands.var([42, 74, 4563, 29]), 4))

    def test_std(self):
        self.assertEqual(2257.41, round(commands.std([42, 74, 4563, 29]), 2))

    def test_compare_column(self):
        self.assertEqual(False, interpretation.simplify(
            ["comparar_columna", [1, 2, 3, 4], ">=",
             "PROM", [123, 14, 245, 252]]))

    # Exceptions

    def test_math_error(self):
        self.assertRaises(errors.MathError, commands.var, [24])

    def test_impossible_process(self):
        self.assertRaises(errors.ImpossibleProcessing,
                          commands.extract_column, "registros", "whatever")

    def test_argument_error(self):
        self.assertRaises(errors.ArgumentError, interpretation.simplify,
                          ["asignar", "x"])

    def test_no_arguments(self):
        self.assertRaises(errors.NoArguments, interpretation.simplify,
                          ["asignar"])

    def test_undefined_function(self):
        self.assertRaises(errors.UndefinedFunction,
                          interpretation.validate_command,
                          ["x", [23, 34, 244]])

    def test_reserved_name(self):
        self.assertRaises(errors.ReservedName,
                          interpretation.simplify,
                          ["asignar", "asignar", 234])


suite = unittest.TestLoader().loadTestsFromTestCase(AssertsTest)
unittest.TextTestRunner().run(suite)

