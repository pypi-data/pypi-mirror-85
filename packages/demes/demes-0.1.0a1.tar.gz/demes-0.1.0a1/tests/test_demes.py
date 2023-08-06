import unittest
import copy
import pathlib

from demes import (
    Epoch,
    Migration,
    Pulse,
    Deme,
    DemeGraph,
    Split,
    Branch,
    Merge,
    Admix,
    load,
)

import demes


class TestEpoch(unittest.TestCase):
    def test_bad_time(self):
        for start_time in (-10000, -1, -1e-9):
            with self.assertRaises(ValueError):
                Epoch(start_time=start_time, end_time=0, initial_size=1)
        for end_time in (-10000, -1, -1e-9, float("inf")):
            with self.assertRaises(ValueError):
                Epoch(start_time=100, end_time=end_time, initial_size=1)

    def test_bad_time_span(self):
        with self.assertRaises(ValueError):
            Epoch(start_time=1, end_time=1, initial_size=1)
        with self.assertRaises(ValueError):
            Epoch(start_time=1, end_time=2, initial_size=1)

    def test_bad_size(self):
        for size in (-10000, -1, -1e-9, 0, float("inf")):
            with self.assertRaises(ValueError):
                Epoch(start_time=1, end_time=0, initial_size=size)
            with self.assertRaises(ValueError):
                Epoch(start_time=1, end_time=0, initial_size=1, final_size=size)

    def test_missing_size(self):
        with self.assertRaises(ValueError):
            Epoch(start_time=1, end_time=0)

    def test_valid_epochs(self):
        Epoch(end_time=0, initial_size=1)
        Epoch(end_time=0, final_size=1)
        Epoch(start_time=float("inf"), end_time=0, initial_size=1)
        Epoch(start_time=float("inf"), end_time=10, initial_size=1)
        Epoch(start_time=100, end_time=99, initial_size=1)
        Epoch(end_time=0, initial_size=1, final_size=1)
        Epoch(end_time=0, initial_size=1, final_size=100)
        Epoch(end_time=0, initial_size=100, final_size=1)
        Epoch(start_time=20, end_time=10, initial_size=1, final_size=100)

    def test_inf_start_time_constant_epoch(self):
        with self.assertRaises(ValueError):
            Epoch(start_time=float("inf"), end_time=0, initial_size=10, final_size=20)

    def test_isclose(self):
        eps = 1e-50
        e1 = Epoch(end_time=0, initial_size=1)
        self.assertTrue(e1.isclose(e1))
        self.assertTrue(e1.isclose(Epoch(end_time=0 + eps, initial_size=1)))
        self.assertTrue(e1.isclose(Epoch(end_time=0, initial_size=1 + eps)))

        self.assertFalse(e1.isclose(Epoch(end_time=1e-9, initial_size=1)))
        self.assertFalse(e1.isclose(Epoch(end_time=0, initial_size=1 + 1e-9)))
        self.assertFalse(e1.isclose(Epoch(start_time=10, end_time=0, initial_size=1)))
        self.assertFalse(e1.isclose(Epoch(end_time=0, initial_size=1, final_size=2)))
        self.assertFalse(
            Epoch(end_time=0, initial_size=1, final_size=2).isclose(
                Epoch(
                    end_time=0,
                    initial_size=1,
                    final_size=2,
                    size_function="exponential",
                )
            )
        )
        self.assertFalse(
            e1.isclose(Epoch(end_time=0, initial_size=1, selfing_rate=0.1))
        )
        self.assertFalse(
            e1.isclose(Epoch(end_time=0, initial_size=1, cloning_rate=0.1))
        )
        self.assertFalse(e1.isclose(None))
        self.assertFalse(e1.isclose(123))
        self.assertFalse(e1.isclose("foo"))

    # APR (7/28): Add tests for selfing rate, cloning rate, and size function.


class TestMigration(unittest.TestCase):
    def test_bad_time(self):
        for time in (-10000, -1, -1e-9):
            with self.assertRaises(ValueError):
                Migration("a", "b", start_time=time, end_time=0, rate=0.1)
        for time in (-10000, -1, -1e-9, float("inf")):
            with self.assertRaises(ValueError):
                Migration("a", "b", start_time=100, end_time=time, rate=0.1)

    def test_bad_rate(self):
        for rate in (-10000, -1, -1e-9, float("inf")):
            with self.assertRaises(ValueError):
                Migration("a", "b", start_time=10, end_time=0, rate=rate)

    def test_bad_demes(self):
        with self.assertRaises(ValueError):
            Migration("a", "a", start_time=10, end_time=0, rate=0.1)

    def test_valid_migration(self):
        Migration("a", "b", start_time=float("inf"), end_time=0, rate=1e-9)
        Migration("a", "b", start_time=1000, end_time=999, rate=0.9)

    def test_isclose(self):
        eps = 1e-50
        m1 = Migration("a", "b", start_time=1, end_time=0, rate=1e-9)
        self.assertTrue(m1.isclose(m1))
        self.assertTrue(
            m1.isclose(Migration("a", "b", start_time=1, end_time=0, rate=1e-9 + eps))
        )
        self.assertTrue(
            m1.isclose(Migration("a", "b", start_time=1 + eps, end_time=0, rate=1e-9))
        )
        self.assertTrue(
            m1.isclose(Migration("a", "b", start_time=1, end_time=0 + eps, rate=1e-9))
        )

        self.assertFalse(
            m1.isclose(Migration("b", "a", start_time=1, end_time=0, rate=1e-9))
        )
        self.assertFalse(
            m1.isclose(Migration("a", "b", start_time=1, end_time=0, rate=2e-9))
        )
        self.assertFalse(
            m1.isclose(Migration("a", "c", start_time=1, end_time=0, rate=1e-9))
        )
        self.assertFalse(
            m1.isclose(Migration("a", "c", start_time=2, end_time=0, rate=1e-9))
        )
        self.assertFalse(
            m1.isclose(Migration("a", "c", start_time=1, end_time=0.1, rate=1e-9))
        )
        self.assertFalse(m1.isclose(None))
        self.assertFalse(m1.isclose(123))
        self.assertFalse(m1.isclose("foo"))


class TestPulse(unittest.TestCase):
    def test_bad_time(self):
        for time in (-10000, -1, -1e-9, float("inf")):
            with self.assertRaises(ValueError):
                Pulse("a", "b", time=time, proportion=0.1)

    def test_bad_proportion(self):
        for proportion in (-10000, -1, -1e-9, 1.2, 100, float("inf")):
            with self.assertRaises(ValueError):
                Pulse("a", "b", time=1, proportion=proportion)

    def test_bad_demes(self):
        with self.assertRaises(ValueError):
            Pulse("a", "a", time=1, proportion=0.1)

    def test_valid_pulse(self):
        Pulse("a", "b", time=1, proportion=1e-9)
        Pulse("a", "b", time=100, proportion=0.9)

    def test_isclose(self):
        eps = 1e-50
        p1 = Pulse("a", "b", time=1, proportion=1e-9)
        self.assertTrue(p1.isclose(p1))
        self.assertTrue(p1.isclose(Pulse("a", "b", time=1, proportion=1e-9)))
        self.assertTrue(p1.isclose(Pulse("a", "b", time=1 + eps, proportion=1e-9)))
        self.assertTrue(p1.isclose(Pulse("a", "b", time=1, proportion=1e-9 + eps)))

        self.assertFalse(p1.isclose(Pulse("a", "c", time=1, proportion=1e-9)))
        self.assertFalse(p1.isclose(Pulse("b", "a", time=1, proportion=1e-9)))
        self.assertFalse(p1.isclose(Pulse("a", "b", time=1, proportion=2e-9)))
        self.assertFalse(p1.isclose(Pulse("a", "b", time=1 + 1e-9, proportion=1e-9)))


class TestSplit(unittest.TestCase):
    def test_bad_time(self):
        for time in [-1e-12, -1, float("inf")]:
            with self.assertRaises(ValueError):
                Split("a", ["b", "c"], time)

    def test_children(self):
        with self.assertRaises(ValueError):
            Split("a", "b", 1)
        with self.assertRaises(ValueError):
            Split("a", ["a", "b"], 1)

    def test_valid_split(self):
        Split("a", ["b", "c"], 10)
        Split("a", ["b", "c", "d"], 10)
        Split("a", ["b", "c"], 0)

    def test_isclose(self):
        eps = 1e-50
        s1 = Split("a", ["b", "c"], 1)
        self.assertTrue(s1.isclose(s1))
        self.assertTrue(s1.isclose(Split("a", ["b", "c"], 1)))
        self.assertTrue(s1.isclose(Split("a", ["b", "c"], 1 + eps)))
        # Order of children doesn't matter.
        self.assertTrue(s1.isclose(Split("a", ["c", "b"], 1)))

        self.assertFalse(s1.isclose(Split("a", ["x", "c"], 1)))
        self.assertFalse(s1.isclose(Split("x", ["b", "c"], 1)))
        self.assertFalse(s1.isclose(Split("a", ["b", "c", "x"], 1)))
        self.assertFalse(s1.isclose(Split("a", ["b", "c"], 1 + 1e-9)))


class TestBranch(unittest.TestCase):
    def test_bad_time(self):
        for time in [-1e-12, -1, float("inf")]:
            with self.assertRaises(ValueError):
                Branch("a", "b", time)

    def test_branch_demes(self):
        with self.assertRaises(ValueError):
            Branch("a", "a", 1)

    def test_valid_branch(self):
        Branch("a", "b", 10)
        Branch("a", "b", 0)

    def test_isclose(self):
        eps = 1e-50
        b1 = Branch("a", "b", 1)
        self.assertTrue(b1.isclose(b1))
        self.assertTrue(b1.isclose(Branch("a", "b", 1)))
        self.assertTrue(b1.isclose(Branch("a", "b", 1 + eps)))

        self.assertFalse(b1.isclose(Branch("x", "b", 1)))
        self.assertFalse(b1.isclose(Branch("a", "x", 1)))
        self.assertFalse(b1.isclose(Branch("b", "a", 1)))
        self.assertFalse(b1.isclose(Branch("a", "b", 1 + 1e-9)))


class TestMerge(unittest.TestCase):
    def test_bad_time(self):
        for time in [-1e-12, -1, float("inf")]:
            with self.assertRaises(ValueError):
                Merge(["a", "b"], [0.5, 0.5], "c", time)

    def test_bad_parents_proportions(self):
        with self.assertRaises(ValueError):
            Merge("a", [1], "b", 1)
        with self.assertRaises(ValueError):
            Merge(["a"], 1.0, "b", 10)
        with self.assertRaises(ValueError):
            Merge(["a"], [1], "b", 1)
        with self.assertRaises(ValueError):
            Merge(["a", "b"], [0.5, 0.5], "a", 1)
        with self.assertRaises(ValueError):
            Merge(["a", "a"], [0.5, 0.5], "b", 1)

    def test_invalid_proportions(self):
        with self.assertRaises(ValueError):
            Merge(["a", "b"], [0.1, 1], "c", 1)
        with self.assertRaises(ValueError):
            Merge(["a", "b"], [0.5], "c", 1)
        with self.assertRaises(ValueError):
            Merge(["a", "b"], [1.0], "c", 1)
        with self.assertRaises(ValueError):
            Merge(["a", "b", "c"], [0.5, 0.5, 0.5], "d", 1)

    def test_valid_merge(self):
        Merge(["a", "b"], [0.5, 0.5], "c", 10)
        Merge(["a", "b"], [0.5, 0.5], "c", 0)
        Merge(["a", "b", "c"], [0.5, 0.25, 0.25], "d", 10)
        Merge(["a", "b", "c"], [0.5, 0.5, 0.0], "d", 10)
        Merge(["a", "b"], [1, 0], "c", 10)

    def test_isclose(self):
        eps = 1e-50
        m1 = Merge(["a", "b"], [0.1, 0.9], "c", 1)
        self.assertTrue(m1.isclose(m1))
        self.assertTrue(m1.isclose(Merge(["a", "b"], [0.1, 0.9], "c", 1)))
        self.assertTrue(m1.isclose(Merge(["a", "b"], [0.1, 0.9], "c", 1 + eps)))
        self.assertTrue(m1.isclose(Merge(["a", "b"], [0.1 + eps, 0.9], "c", 1)))
        self.assertTrue(m1.isclose(Merge(["a", "b"], [0.1, 0.9 + eps], "c", 1)))
        # Order of parents/proportions doesn't matter.
        self.assertTrue(m1.isclose(Merge(["b", "a"], [0.9, 0.1], "c", 1)))

        self.assertFalse(m1.isclose(Merge(["a", "x"], [0.1, 0.9], "c", 1)))
        self.assertFalse(m1.isclose(Merge(["x", "b"], [0.1, 0.9], "c", 1)))
        self.assertFalse(
            m1.isclose(Merge(["a", "b"], [0.1 + 1e-9, 0.9 - 1e-9], "c", 1))
        )
        self.assertFalse(m1.isclose(Merge(["a", "b"], [0.1, 0.9], "x", 1)))
        self.assertFalse(m1.isclose(Merge(["a", "b"], [0.1, 0.9], "c", 1 + 1e-9)))
        self.assertFalse(m1.isclose(Merge(["a", "b", "x"], [0.1, 0.9, 0], "c", 1)))


class TestAdmix(unittest.TestCase):
    def test_bad_time(self):
        for time in [-1e-12, -1, float("inf")]:
            with self.assertRaises(ValueError):
                Admix(["a", "b"], [0.5, 0.5], "c", time)

    def test_bad_parents_proportions(self):
        with self.assertRaises(ValueError):
            Admix("a", [1], "b", 1)
        with self.assertRaises(ValueError):
            Admix(["a"], 1.0, "b", 10)
        with self.assertRaises(ValueError):
            Admix(["a"], [1], "b", 1)
        with self.assertRaises(ValueError):
            Admix(["a", "b"], [0.5, 0.5], "a", 1)
        with self.assertRaises(ValueError):
            Admix(["a", "a"], [0.5, 0.5], "b", 1)

    def test_invalid_proportions(self):
        with self.assertRaises(ValueError):
            Admix(["a", "b"], [0.1, 1], "c", 1)
        with self.assertRaises(ValueError):
            Admix(["a", "b"], [0.5], "c", 1)
        with self.assertRaises(ValueError):
            Admix(["a", "b"], [1.0], "c", 1)
        with self.assertRaises(ValueError):
            Admix(["a", "b", "c"], [0.5, 0.5, 0.5], "d", 1)

    def test_valid_admixture(self):
        Admix(["a", "b"], [0.5, 0.5], "c", 10)
        Admix(["a", "b"], [0.5, 0.5], "c", 0)
        Admix(["a", "b", "c"], [0.5, 0.25, 0.25], "d", 10)
        Admix(["a", "b", "c"], [0.5, 0.5, 0.0], "d", 10)
        Admix(["a", "b"], [1, 0], "c", 10)

    def test_isclose(self):
        eps = 1e-50
        a1 = Admix(["a", "b"], [0.1, 0.9], "c", 1)
        self.assertTrue(a1.isclose(a1))
        self.assertTrue(a1.isclose(Admix(["a", "b"], [0.1, 0.9], "c", 1)))
        self.assertTrue(a1.isclose(Admix(["a", "b"], [0.1 + eps, 0.9], "c", 1 + eps)))
        self.assertTrue(a1.isclose(Admix(["a", "b"], [0.1 + eps, 0.9], "c", 1)))
        self.assertTrue(a1.isclose(Admix(["a", "b"], [0.1, 0.9 + eps], "c", 1 + eps)))
        # Order of parents/proportions doesn't matter.
        self.assertTrue(a1.isclose(Admix(["b", "a"], [0.9, 0.1], "c", 1)))

        self.assertFalse(a1.isclose(Admix(["a", "x"], [0.1, 0.9], "c", 1)))
        self.assertFalse(a1.isclose(Admix(["x", "b"], [0.1, 0.9], "c", 1)))
        self.assertFalse(
            a1.isclose(Admix(["a", "b"], [0.1 + 1e-9, 0.9 - 1e-9], "c", 1))
        )
        self.assertFalse(a1.isclose(Admix(["a", "b"], [0.1, 0.9], "x", 1)))
        self.assertFalse(a1.isclose(Admix(["a", "b"], [0.1, 0.9], "c", 1 + 1e-9)))
        self.assertFalse(a1.isclose(Admix(["a", "b", "x"], [0.1, 0.9, 0], "c", 1)))


class TestDeme(unittest.TestCase):
    def test_properties(self):
        deme = Deme(
            "a",
            "b",
            ["c"],
            [1],
            [Epoch(start_time=float("inf"), end_time=0, initial_size=1)],
        )
        self.assertEqual(deme.start_time, float("inf"))
        self.assertEqual(deme.end_time, 0)
        self.assertEqual(deme.ancestors[0], "c")
        self.assertEqual(deme.proportions[0], 1)

        deme = Deme(
            "a", "b", ["c"], [1], [Epoch(start_time=100, end_time=50, initial_size=1)]
        )
        self.assertEqual(deme.start_time, 100)
        self.assertEqual(deme.end_time, 50)
        deme.add_epoch(Epoch(start_time=50, end_time=20, initial_size=100))
        self.assertEqual(deme.start_time, 100)
        self.assertEqual(deme.end_time, 20)
        deme.add_epoch(Epoch(start_time=20, end_time=1, initial_size=200))
        self.assertEqual(deme.start_time, 100)
        self.assertEqual(deme.end_time, 1)

    def test_no_epochs(self):
        with self.assertRaises(ValueError):
            Deme("a", "b", ["c"], [1], [])

    def test_bad_ancestors(self):
        with self.assertRaises(TypeError):
            Deme(
                "a",
                "b",
                "c",
                [1],
                [Epoch(start_time=10, end_time=0, initial_size=1)],
            )
        with self.assertRaises(TypeError):
            Deme(
                "a",
                "b",
                {"c", "d"},
                [0.2, 0.8],
                [Epoch(start_time=10, end_time=0, initial_size=1)],
            )
        with self.assertRaises(ValueError):
            Deme(
                "a",
                "b",
                ["c", "d"],
                None,
                [Epoch(start_time=10, end_time=0, initial_size=1)],
            )
        with self.assertRaises(ValueError):
            Deme(
                "a",
                "b",
                ["c", "d"],
                [0.5, 0.2, 0.3],
                [Epoch(start_time=10, end_time=0, initial_size=1)],
            )
        with self.assertRaises(ValueError):
            Deme(
                "a",
                "b",
                ["a", "c"],
                [0.5, 0.5],
                [Epoch(start_time=10, end_time=0, initial_size=1)],
            )

    def test_two_epochs(self):
        with self.assertRaises(ValueError):
            Deme(
                "a",
                "b",
                ["c"],
                [1],
                [
                    Epoch(start_time=11, end_time=10, initial_size=100),
                    Epoch(start_time=10, end_time=1, initial_size=1),
                ],
            )

    def test_add_epoch(self):
        deme = Deme(
            "a", "b", ["c"], [1], [Epoch(start_time=100, end_time=50, initial_size=1)]
        )
        with self.assertRaises(ValueError):
            deme.add_epoch(Epoch(start_time=60, end_time=0, initial_size=10))
        with self.assertRaises(ValueError):
            deme.add_epoch(Epoch(start_time=40, end_time=0, initial_size=10))
        with self.assertRaises(ValueError):
            deme.add_epoch(Epoch(start_time=50, end_time=50, initial_size=10))
        with self.assertRaises(ValueError):
            deme.add_epoch(
                Epoch(
                    start_time=50,
                    end_time=0,
                    initial_size=10,
                    final_size=20,
                    size_function="constant",
                )
            )

    def test_epochs_out_of_order(self):
        deme = Deme(
            "a", "b", ["c"], [1], [Epoch(start_time=10, end_time=5, initial_size=1)]
        )
        for time in (5, -1, float("inf")):
            with self.assertRaises(ValueError):
                deme.add_epoch(Epoch(start_time=5, end_time=time, initial_size=100))
        deme.add_epoch(Epoch(start_time=5, end_time=0, initial_size=100))

    def test_epochs_are_a_partition(self):
        for start_time, end_time in [(float("inf"), 100), (200, 100)]:
            deme = Deme(
                "a",
                "b",
                ["c"],
                [1],
                [Epoch(start_time=start_time, end_time=end_time, initial_size=1)],
            )
            with self.assertRaises(ValueError):
                deme.add_epoch(Epoch(end_time=100, initial_size=100))
            for t in (50, 20, 10):
                deme.add_epoch(Epoch(end_time=t, initial_size=t))
            prev_end_time = end_time
            for epoch in deme.epochs[1:]:
                self.assertEqual(epoch.start_time, prev_end_time)
                prev_end_time = epoch.end_time

    def test_time_span(self):
        for start_time, end_time in zip((float("inf"), 100, 20), (0, 20, 0)):
            deme = Deme(
                "a",
                "b",
                ["c"],
                [1],
                [Epoch(start_time=start_time, end_time=end_time, initial_size=1)],
            )
            self.assertEqual(deme.time_span, start_time - end_time)

    def test_isclose(self):
        d1 = Deme(
            id="a",
            description="foo deme",
            ancestors=None,
            proportions=None,
            epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
        )
        self.assertTrue(d1.isclose(d1))
        self.assertTrue(
            d1.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
                )
            )
        )
        # Description field doesn't matter.
        self.assertTrue(
            d1.isclose(
                Deme(
                    id="a",
                    description="bar deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
                )
            )
        )

        # selfing_rate is a property of the deme's epoch, so we shouldn't
        # care if this is set for the deme or for the epochs directly.
        d2 = Deme(
            id="a",
            description="foo deme",
            ancestors=None,
            proportions=None,
            epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
            selfing_rate=0.1,
        )
        self.assertTrue(
            d2.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[
                        Epoch(
                            start_time=10, end_time=5, initial_size=1, selfing_rate=0.1
                        )
                    ],
                )
            )
        )

        # cloning_rate is a property of the deme's epoch, so we shouldn't
        # care if this is set for the deme or for the epochs directly.
        d2 = Deme(
            id="a",
            description="foo deme",
            ancestors=None,
            proportions=None,
            epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
            cloning_rate=0.1,
        )
        self.assertTrue(
            d2.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[
                        Epoch(
                            start_time=10, end_time=5, initial_size=1, cloning_rate=0.1
                        )
                    ],
                )
            )
        )

        #
        # Check inequalities.
        #

        self.assertFalse(
            d1.isclose(
                Deme(
                    id="b",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
                )
            )
        )
        self.assertFalse(
            d1.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=["x"],
                    proportions=[1],
                    epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
                )
            )
        )
        self.assertFalse(
            d1.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=9, end_time=5, initial_size=1)],
                )
            )
        )
        self.assertFalse(
            d1.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=10, end_time=9, initial_size=1)],
                )
            )
        )

        self.assertFalse(
            d1.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=10, end_time=5, initial_size=9)],
                )
            )
        )
        self.assertFalse(
            d1.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
                    selfing_rate=0.1,
                )
            )
        )
        self.assertFalse(
            d1.isclose(
                Deme(
                    id="a",
                    description="foo deme",
                    ancestors=None,
                    proportions=None,
                    epochs=[Epoch(start_time=10, end_time=5, initial_size=1)],
                    cloning_rate=0.1,
                )
            )
        )
        d2 = copy.deepcopy(d1)
        d2.add_epoch(Epoch(end_time=0, initial_size=1))
        self.assertFalse(d1 == d2)

    # APR (7/28): Add tests for selfing rate, cloning rate, and size function.
    # Add tests for testing ancestors and proportions.
    # Also add tests for any implied values.


class TestDemeGraph(unittest.TestCase):
    def test_bad_generation_time(self):
        for generation_time in (-100, -1e-9, 0, float("inf")):
            with self.assertRaises(ValueError):
                DemeGraph(
                    description="test",
                    time_units="years",
                    generation_time=generation_time,
                )

    def test_bad_default_Ne(self):
        for N in (-100, -1e-9, 0, float("inf")):
            with self.assertRaises(ValueError):
                DemeGraph(
                    description="test",
                    time_units="years",
                    generation_time=1,
                    default_Ne=N,
                )

    def check_in_generations(self, dg1):
        assert dg1.generation_time is not None
        assert dg1.generation_time > 1
        dg1_copy = copy.deepcopy(dg1)
        dg2 = dg1.in_generations()
        # in_generations() shouldn't modify the original
        self.assertEqual(dg1.asdict(), dg1_copy.asdict())
        # but clearly dg2 should now differ
        self.assertNotEqual(dg1.asdict(), dg2.asdict())

        # Alternate implementation, which recurses the object hierarchy.
        def in_generations2(dg):
            generation_time = dg.generation_time
            dg = copy.deepcopy(dg)
            dg.time_units = "generations"
            if generation_time is None:
                return dg
            dg.generation_time = None

            def divide_time_attrs(obj):
                if not hasattr(obj, "__dict__"):
                    return
                for name, value in obj.__dict__.items():
                    if name in ("time", "start_time", "end_time"):
                        if value is not None:
                            setattr(obj, name, value / generation_time)
                    elif isinstance(value, (list, tuple)):
                        for a in value:
                            divide_time_attrs(a)
                    else:
                        divide_time_attrs(value)

            divide_time_attrs(dg)
            return dg

        self.assertEqual(in_generations2(dg1).asdict(), dg2.asdict())
        # in_generations2() shouldn't modify the original
        self.assertEqual(dg1.asdict(), dg1_copy.asdict())

        # in_generations() should be idempotent
        dg3 = dg2.in_generations()
        self.assertEqual(dg2.asdict(), dg3.asdict())
        dg3 = in_generations2(dg2)
        self.assertEqual(dg2.asdict(), dg3.asdict())

    def test_in_generations(self):
        examples = list(pathlib.Path("examples").glob("*.yml"))
        examples.extend(list(pathlib.Path("../examples").glob("*.yml")))
        if len(examples) == 0:
            raise RuntimeError(
                "Can't find any examples. The tests should be run from the "
                "'test' directory or the toplevel directory."
            )
        i = 0
        for yml in examples:
            dg = load(yml)
            if dg.generation_time not in (None, 1):
                self.check_in_generations(dg)
                i += 1
        self.assertGreater(i, 0)

    def test_bad_migration_time(self):
        dg = demes.DemeGraph(description="test bad migration", time_units="generations")
        dg.deme("deme1", end_time=0, initial_size=1000)
        dg.deme("deme2", end_time=100, initial_size=1000)
        with self.assertRaises(ValueError):
            dg.migration(
                source="deme1", dest="deme2", rate=0.01, start_time=1000, end_time=0
            )

    def test_bad_pulse_time(self):
        dg = demes.DemeGraph(
            description="test bad pulse time", time_units="generations"
        )
        dg.deme("deme1", end_time=0, initial_size=1000)
        dg.deme("deme2", end_time=100, initial_size=1000)
        with self.assertRaises(ValueError):
            dg.pulse(source="deme1", dest="deme2", proportion=0.1, time=10)

    def test_bad_deme(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        with self.assertRaises(ValueError):
            dg.deme("a")
        with self.assertRaises(TypeError):
            dg.deme("a", initial_size=100, ancestors="b")
        with self.assertRaises(ValueError):
            dg.deme("a", initial_size=100, ancestors=["b", "c"], proportions=[0.5, 0.5])
        with self.assertRaises(ValueError):
            dg.deme(
                "a",
                initial_size=100,
                ancestors=["b"],
                end_time=0,
                epochs=[
                    Epoch(initial_size=1, start_time=20, end_time=10),
                    Epoch(start_time=10, end_time=5, initial_size=2),
                ],
            )
        with self.assertRaises(ValueError):
            dg.deme(
                "a",
                initial_size=100,
                ancestors=["b"],
                start_time=15,
                end_time=0,
                epochs=[
                    Epoch(initial_size=1, start_time=20, end_time=10),
                    Epoch(start_time=10, end_time=0, initial_size=2),
                ],
            )

    def test_proportions_default(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        with self.assertRaises(ValueError):
            dg.deme("a", initial_size=100, ancestors=["b", "c"])
        dg.deme("a", initial_size=100, ancestors=["b"])
        self.assertEqual(len(dg["a"].proportions), 1)
        self.assertEqual(dg["a"].proportions[0], 1.0)

    def test_bad_migration(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        with self.assertRaises(ValueError):
            dg.symmetric_migration()
        with self.assertRaises(ValueError):
            dg.symmetric_migration(demes=["a"], rate=0.1)
        with self.assertRaises(ValueError):
            dg.migration("a", "b", rate=0.1)
        dg.deme("a", initial_size=100)
        with self.assertRaises(ValueError):
            dg.migration("a", "b", rate=0.1)
        with self.assertRaises(ValueError):
            dg.migration("b", "a", rate=0.1)

    def test_bad_pulse(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", initial_size=100)
        with self.assertRaises(ValueError):
            dg.pulse("a", "b", 0.1, 10)
        with self.assertRaises(ValueError):
            dg.pulse("b", "a", 0.1, 10)

    def test_bad_split(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        with self.assertRaises(ValueError):
            dg.split("a", ["a", "b", "c"], 10)
        dg.deme("a", initial_size=100, end_time=50)
        dg.deme("b", initial_size=100, start_time=50, end_time=0)
        dg.deme("c", initial_size=100, start_time=20, end_time=0)
        with self.assertRaises(ValueError):
            dg.split("a", ["b", "c"], 50)

    def test_bad_branch(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", start_time=10, end_time=5, initial_size=10)
        dg.deme("b", start_time=20, end_time=0, initial_size=10)
        dg.deme("c", start_time=2, end_time=0, initial_size=10)
        with self.assertRaises(ValueError):
            dg.branch("a", "b", 7)
        with self.assertRaises(ValueError):
            dg.branch("a", "c", 7)

    def test_bad_merge(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", end_time=5, initial_size=10)
        dg.deme("b", end_time=5, initial_size=10)
        dg.deme("c", start_time=5, end_time=0, initial_size=10)
        dg.deme("d", start_time=2, end_time=0, initial_size=1)
        with self.assertRaises(ValueError):
            dg.merge(["a", "b"], [0.5, 0.5], "c", 10)
        with self.assertRaises(ValueError):
            dg.merge(["a", "b"], [0.5, 0.5], "d", 2)

    def test_merge_cuts_epochs(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", initial_size=10, end_time=0)
        dg.deme(
            "b",
            epochs=[
                Epoch(end_time=10, initial_size=5),
                Epoch(end_time=5, initial_size=10),
                Epoch(end_time=0, initial_size=2),
            ],
        )
        dg.deme("c", start_time=5, initial_size=10)
        dg.merge(["a", "b"], [0.5, 0.5], "c", 5)
        self.assertEqual(dg["a"].end_time, 5)
        self.assertEqual(dg["b"].end_time, 5)
        self.assertEqual(len(dg["b"].epochs), 2)

    def test_bad_admixture(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", start_time=2, initial_size=100)
        with self.assertRaises(ValueError):
            dg.admix(["b", "c"], [0.5, 0.5], "a", 5)
        dg.deme("b", end_time=5, initial_size=10)
        dg.deme("c", start_time=5, end_time=0, initial_size=10)
        with self.assertRaises(ValueError):
            dg.admix(["b", "c"], [0.5, 0.5], "a", 2)

    def test_isclose(self):
        g1 = DemeGraph(
            description="test",
            time_units="generations",
        )
        g2 = copy.deepcopy(g1)
        g1.deme("d1", initial_size=1000)
        self.assertTrue(g1.isclose(g1))
        self.assertTrue(g1.isclose(demes.loads(demes.dumps(g1))))

        # Don't care about description for equality.
        g3 = DemeGraph(
            description="some other description",
            time_units="generations",
        )
        g3.deme("d1", initial_size=1000)
        self.assertTrue(g1.isclose(g3))

        # Don't care about doi for equality.
        g3 = DemeGraph(
            description="test",
            time_units="generations",
            doi="https://example.com/foo.bar",
        )
        g3.deme("d1", initial_size=1000)
        self.assertTrue(g1.isclose(g3))

        # The choice of using default_Ne, or alternately setting initial_size
        # for each deme, is a model implementation detail. So the resulting
        # deme graphs should compare equal.
        g3 = DemeGraph(
            description="test",
            time_units="generations",
            default_Ne=1000,
        )
        g3.deme("d1")
        self.assertTrue(g1.isclose(g3))

        # Selfing rate is a property of a deme's epoch, not a deme graph.
        g3 = DemeGraph(
            description="test",
            time_units="generations",
            selfing_rate=0.1,
        )
        g3.deme("d1", initial_size=1000)
        g4 = DemeGraph(
            description="test",
            time_units="generations",
        )
        g4.deme("d1", initial_size=1000, selfing_rate=0.1)
        self.assertTrue(g3.isclose(g4))

        # Cloning rate is a property of a deme's epoch, not a deme graph.
        g3 = DemeGraph(
            description="test",
            time_units="generations",
            cloning_rate=0.1,
        )
        g3.deme("d1", initial_size=1000)
        g4 = DemeGraph(
            description="test",
            time_units="generations",
        )
        g4.deme("d1", initial_size=1000, cloning_rate=0.1)
        self.assertTrue(g3.isclose(g4))

        # The order in which demes are added shouldn't matter.
        g3 = copy.deepcopy(g2)
        g4 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1000)
        g3.deme("d2", initial_size=1000)
        g4.deme("d2", initial_size=1000)
        g4.deme("d1", initial_size=1000)
        self.assertTrue(g3.isclose(g4))

        # The order in which migrations are added shouldn't matter.
        g3.migration("d1", "d2", rate=1e-4, start_time=50, end_time=40)
        g3.migration("d2", "d1", rate=1e-5)
        g4.migration("d2", "d1", rate=1e-5)
        g4.migration("d1", "d2", rate=1e-4, start_time=50, end_time=40)
        self.assertTrue(g3.isclose(g4))

        # The order in which pulses are added shouldn't matter.
        g3.pulse("d1", "d2", proportion=0.01, time=100)
        g3.pulse("d1", "d2", proportion=0.01, time=50)
        g4.pulse("d1", "d2", proportion=0.01, time=50)
        g4.pulse("d1", "d2", proportion=0.01, time=100)
        self.assertTrue(g3.isclose(g4))

        #
        # Check inequalities
        #

        self.assertFalse(g1 == g2)
        g3 = copy.deepcopy(g2)
        g3.deme("dX", initial_size=1000)
        self.assertFalse(g1.isclose(g3))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1001)
        self.assertFalse(g1.isclose(g3))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1000)
        g3.deme("d2", initial_size=1000)
        self.assertFalse(g1.isclose(g3))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", ancestors=["x"], initial_size=1000)
        self.assertFalse(g1.isclose(g3))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1000)
        g3.deme("d2", initial_size=1000)
        g4 = copy.deepcopy(g2)
        g4.deme("d1", initial_size=1000)
        g4.deme("d2", initial_size=1000)
        g4.migration("d2", "d1", rate=1e-5)
        self.assertFalse(g3.isclose(g4))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1000)
        g3.deme("d2", initial_size=1000)
        g3.migration("d1", "d2", rate=1e-5)
        g4 = copy.deepcopy(g2)
        g4.deme("d1", initial_size=1000)
        g4.deme("d2", initial_size=1000)
        g4.migration("d2", "d1", rate=1e-5)
        self.assertFalse(g3.isclose(g4))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1000)
        g3.deme("d2", initial_size=1000)
        g3.migration("d2", "d1", rate=1e-5)
        g4 = copy.deepcopy(g2)
        g4.deme("d1", initial_size=1000)
        g4.deme("d2", initial_size=1000)
        g4.symmetric_migration(["d2", "d1"], rate=1e-5)
        self.assertFalse(g3.isclose(g4))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1000)
        g3.deme("d2", initial_size=1000)
        g4 = copy.deepcopy(g2)
        g4.deme("d1", initial_size=1000)
        g4.deme("d2", initial_size=1000)
        g4.pulse("d1", "d2", proportion=0.01, time=100)
        self.assertFalse(g3.isclose(g4))

        g3 = copy.deepcopy(g2)
        g3.deme("d1", initial_size=1000)
        g3.deme("d2", initial_size=1000)
        g3.pulse("d2", "d1", proportion=0.01, time=100)
        g4 = copy.deepcopy(g2)
        g4.deme("d1", initial_size=1000)
        g4.deme("d2", initial_size=1000)
        g3.pulse("d1", "d2", proportion=0.01, time=100)
        self.assertFalse(g3.isclose(g4))


class TestDemeGraphToDict(unittest.TestCase):
    def test_fill_selfing_rate(self):
        dg = demes.DemeGraph(
            description="a", time_units="generations", selfing_rate=0.5
        )
        dg.deme("a", initial_size=10)
        d = dg.asdict_compact()
        self.assertTrue(d["selfing_rate"] == dg.selfing_rate)

    def test_fill_cloning_rate(self):
        dg = demes.DemeGraph(
            description="a", time_units="generations", cloning_rate=0.5
        )
        dg.deme("a", initial_size=10)
        d = dg.asdict_compact()
        self.assertTrue(d["cloning_rate"] == dg.cloning_rate)

    def test_finite_start_time(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", initial_size=100, start_time=100)
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["start_time"] == dg["a"].start_time)

    def test_deme_selfing_rate(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", initial_size=100, selfing_rate=0.1)
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["selfing_rate"] == dg["a"].selfing_rate)
        dg = demes.DemeGraph(
            description="a", time_units="generations", selfing_rate=0.01
        )
        dg.deme("a", initial_size=100, selfing_rate=0.1)
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["selfing_rate"] == dg["a"].selfing_rate)

    def test_deme_cloning_rate(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", initial_size=100, cloning_rate=0.1)
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["cloning_rate"] == dg["a"].cloning_rate)

    def test_fill_nonstandard_size_function(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme(
            "a",
            epochs=[
                Epoch(initial_size=1, end_time=10),
                Epoch(final_size=10, size_function="linear", end_time=0),
            ],
        )
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["epochs"][-1]["size_function"] == "linear")

    def test_fill_epoch_selfing_rates(self):
        dg = demes.DemeGraph(
            description="a", time_units="generations", selfing_rate=0.2
        )
        dg.deme(
            "a",
            epochs=[
                Epoch(initial_size=10, end_time=10, selfing_rate=0.2),
                Epoch(final_size=20, end_time=0, selfing_rate=0.1),
            ],
        )
        d = dg.asdict_compact()
        self.assertTrue(d["selfing_rate"] == 0.2)
        self.assertTrue("selfing_rate" not in d["demes"]["a"]["epochs"][0])
        self.assertTrue(d["demes"]["a"]["epochs"][1]["selfing_rate"] == 0.1)

        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme(
            "a",
            selfing_rate=0.2,
            epochs=[
                Epoch(initial_size=10, end_time=10, selfing_rate=0.2),
                Epoch(final_size=20, end_time=0, selfing_rate=0.1),
            ],
        )
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["selfing_rate"] == 0.2)
        self.assertTrue("selfing_rate" not in d["demes"]["a"]["epochs"][0])
        self.assertTrue(d["demes"]["a"]["epochs"][1]["selfing_rate"] == 0.1)

        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme(
            "a",
            epochs=[
                Epoch(initial_size=10, end_time=10),
                Epoch(final_size=20, end_time=0, selfing_rate=0.1),
            ],
        )
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["epochs"][1]["selfing_rate"] == 0.1)

    def test_fill_epoch_cloning_rates(self):
        dg = demes.DemeGraph(
            description="a", time_units="generations", cloning_rate=0.2
        )
        dg.deme(
            "a",
            epochs=[
                Epoch(initial_size=10, end_time=10),
                Epoch(final_size=20, end_time=0, cloning_rate=0.1),
            ],
        )
        d = dg.asdict_compact()
        self.assertTrue(d["cloning_rate"] == 0.2)
        self.assertTrue(d["demes"]["a"]["epochs"][1]["cloning_rate"] == 0.1)

        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme(
            "a",
            cloning_rate=0.2,
            epochs=[
                Epoch(initial_size=10, end_time=10),
                Epoch(final_size=20, end_time=0, cloning_rate=0.1),
            ],
        )
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["cloning_rate"] == 0.2)
        self.assertTrue(d["demes"]["a"]["epochs"][1]["cloning_rate"] == 0.1)

        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme(
            "a",
            epochs=[
                Epoch(initial_size=10, end_time=10),
                Epoch(final_size=20, end_time=0, cloning_rate=0.1),
            ],
        )
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["epochs"][1]["cloning_rate"] == 0.1)

    def test_fill_description(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", description="described", initial_size=100)
        d = dg.asdict_compact()
        self.assertTrue(d["demes"]["a"]["description"] == dg["a"].description)

    def test_fill_migration_bounds(self):
        dg = demes.DemeGraph(description="a", time_units="generations")
        dg.deme("a", initial_size=100)
        dg.deme("b", initial_size=100)
        dg.migration("a", "b", 0.01, start_time=20, end_time=10)
        d = dg.asdict_compact()
        self.assertTrue(d["migrations"]["asymmetric"][0]["start_time"] == 20)
        self.assertTrue(d["migrations"]["asymmetric"][0]["end_time"] == 10)
