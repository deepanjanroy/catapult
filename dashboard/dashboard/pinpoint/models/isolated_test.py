# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from dashboard.pinpoint.models import isolated


class IsolatedTest(unittest.TestCase):

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    ndb.get_context().clear_cache()

  def tearDown(self):
    self.testbed.deactivate()

  def testPutAndGet(self):
    isolated.Put((
        ('Mac Builder', 'f9f2b720', 'telemetry_perf', '7c7e90be'),
        ('Mac Builder', 'f35be4f1', 'telemetry_perf', '38e2f262')))

    isolated_hash = isolated.Get('Mac Builder', 'f9f2b720', 'telemetry_perf')
    self.assertEqual(isolated_hash, '7c7e90be')

  def testUnknownIsolated(self):
    with self.assertRaises(KeyError):
      isolated.Get('Wrong Builder', 'f9f2b720', 'telemetry_perf')
