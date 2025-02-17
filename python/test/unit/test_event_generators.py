# -*- coding: utf-8 -*-
#
# test_event_generators.py

import unittest
import numpy as np

import arbor as arb

# to be able to run .py file from child directory
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    import options
except ModuleNotFoundError:
    from test import options

"""
all tests for event generators (regular, explicit, poisson)
"""

class RegularSchedule(unittest.TestCase):
    def test_none_contor_regular_schedule(self):
        rs = arb.regular_schedule(tstart=None, tstop=None)

    def test_tstart_dt_tstop_contor_regular_schedule(self):
        rs = arb.regular_schedule(10., 1., 20.)
        self.assertEqual(rs.tstart, 10.)
        self.assertEqual(rs.dt, 1.)
        self.assertEqual(rs.tstop, 20.)

    def test_set_tstart_dt_tstop_regular_schedule(self):
        rs = arb.regular_schedule()
        rs.tstart = 17.
        rs.dt = 0.5
        rs.tstop = 42.
        self.assertEqual(rs.tstart, 17.)
        self.assertAlmostEqual(rs.dt, 0.5)
        self.assertEqual(rs.tstop, 42.)

    def test_event_generator_regular_schedule(self):
        cm = arb.cell_member()
        cm.gid = 42
        cm.index = 3
        rs = arb.regular_schedule(2.0, 1., 100.)
        rg = arb.event_generator(cm, 3.14, rs)
        self.assertEqual(rg.target.gid, 42)
        self.assertEqual(rg.target.index, 3)
        self.assertAlmostEqual(rg.weight, 3.14)

    def test_exceptions_regular_schedule(self):
        with self.assertRaisesRegex(RuntimeError,
            "tstart must a non-negative number, or None"):
            arb.regular_schedule(tstart = -1.)
        with self.assertRaisesRegex(RuntimeError,
            "dt must be a non-negative number"):
            arb.regular_schedule(dt = -0.1)
        with self.assertRaises(TypeError):
            arb.regular_schedule(dt = None)
        with self.assertRaises(TypeError):
            arb.regular_schedule(dt = 'dt')
        with self.assertRaisesRegex(RuntimeError,
            "tstop must a non-negative number, or None"):
            arb.regular_schedule(tstop = 'tstop')

class ExplicitSchedule(unittest.TestCase):
    def test_times_contor_explicit_schedule(self):
        es = arb.explicit_schedule([1, 2, 3, 4.5])
        self.assertEqual(es.times, [1, 2, 3, 4.5])

    def test_set_times_explicit_schedule(self):
        es = arb.explicit_schedule()
        es.times = [42, 43, 44, 55.5, 100]
        self.assertEqual(es.times, [42, 43, 44, 55.5, 100])

    def test_event_generator_explicit_schedule(self):
        cm = arb.cell_member()
        cm.gid = 0
        cm.index = 42
        es = arb.explicit_schedule([0,1,2,3,4.4])
        eg = arb.event_generator(cm, -0.01, es)
        self.assertEqual(eg.target.gid, 0)
        self.assertEqual(eg.target.index, 42)
        self.assertAlmostEqual(eg.weight, -0.01)

    def test_exceptions_explicit_schedule(self):
        with self.assertRaisesRegex(RuntimeError,
            "explicit time schedule can not contain negative values"):
            arb.explicit_schedule([-1])
        with self.assertRaises(TypeError):
            arb.explicit_schedule(['times'])
        with self.assertRaises(TypeError):
            arb.explicit_schedule([None])
        with self.assertRaises(TypeError):
            arb.explicit_schedule([[1,2,3]])

class PoissonSchedule(unittest.TestCase):
    def test_freq_seed_contor_poisson_schedule(self):
        ps = arb.poisson_schedule(freq = 5., seed = 42)
        self.assertEqual(ps.freq, 5.)
        self.assertEqual(ps.seed, 42)

    def test_tstart_freq_seed_contor_poisson_schedule(self):
        ps = arb.poisson_schedule(10., 100., 1000)
        self.assertEqual(ps.tstart, 10.)
        self.assertEqual(ps.freq, 100.)
        self.assertEqual(ps.seed, 1000)

    def test_set_tstart_freq_seed_poisson_schedule(self):
        ps = arb.poisson_schedule()
        ps.tstart = 4.5
        ps.freq = 5.5
        ps.seed = 83
        self.assertAlmostEqual(ps.tstart, 4.5)
        self.assertAlmostEqual(ps.freq, 5.5)
        self.assertEqual(ps.seed, 83)

    def test_event_generator_poisson_schedule(self):
        cm = arb.cell_member()
        cm.gid = 4
        cm.index = 2
        ps = arb.poisson_schedule(0., 10., 0)
        pg = arb.event_generator(cm, 42., ps)
        self.assertEqual(pg.target.gid, 4)
        self.assertEqual(pg.target.index, 2)
        self.assertEqual(pg.weight, 42.)

    def test_exceptions_poisson_schedule(self):
        with self.assertRaisesRegex(RuntimeError,
            "tstart must be a non-negative number"):
            arb.poisson_schedule(tstart = -10.)
        with self.assertRaises(TypeError):
            arb.poisson_schedule(tstart = None)
        with self.assertRaises(TypeError):
            arb.poisson_schedule(tstart = 'tstart')
        with self.assertRaisesRegex(RuntimeError,
            "frequency must be a non-negative number"):
            arb.poisson_schedule(freq = -100.)
        with self.assertRaises(TypeError):
            arb.poisson_schedule(freq = 'freq')
        with self.assertRaises(TypeError):
            arb.poisson_schedule(seed = -1)
        with self.assertRaises(TypeError):
            arb.poisson_schedule(seed = 10.)
        with self.assertRaises(TypeError):
            arb.poisson_schedule(seed = 'seed')
        with self.assertRaises(TypeError):
            arb.poisson_schedule(seed = None)

def suite():
    # specify class and test functions in tuple (here: all tests starting with 'test' from classes RegularSchedule, ExplicitSchedule and PoissonSchedule
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(RegularSchedule, ('test')))
    suite.addTests(unittest.makeSuite(ExplicitSchedule, ('test')))
    suite.addTests(unittest.makeSuite(PoissonSchedule, ('test')))
    return suite

def run():
    v = options.parse_arguments().verbosity
    runner = unittest.TextTestRunner(verbosity = v)
    runner.run(suite())

if __name__ == "__main__":
    run()
