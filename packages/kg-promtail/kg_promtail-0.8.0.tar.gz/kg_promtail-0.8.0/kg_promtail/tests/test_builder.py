import unittest

from kubragen import KubraGen
from kubragen.jsonpatch import FilterJSONPatches_Apply, ObjectFilter, FilterJSONPatch
from kubragen.provider import Provider_Generic

from kg_promtail import PromtailBuilder, PromtailOptions


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.kg = KubraGen(provider=Provider_Generic())

    def test_empty(self):
        promtail_config = PromtailBuilder(kubragen=self.kg)
        self.assertEqual(promtail_config.object_name('config'), 'promtail-config')
        self.assertEqual(promtail_config.object_name('daemonset'), 'promtail')

    def test_basedata(self):
        promtail_config = PromtailBuilder(kubragen=self.kg, options=PromtailOptions({
            'namespace': 'myns',
            'basename': 'mypromtail',
        }))
        self.assertEqual(promtail_config.object_name('config'), 'mypromtail-config')
        self.assertEqual(promtail_config.object_name('daemonset'), 'mypromtail')

        FilterJSONPatches_Apply(items=promtail_config.build(promtail_config.BUILD_SERVICE), jsonpatches=[
            FilterJSONPatch(filters=ObjectFilter(names=[promtail_config.BUILDITEM_DAEMONSET]), patches=[
                {'op': 'check', 'path': '/metadata/name', 'cmp': 'equals', 'value': 'mypromtail'},
                {'op': 'check', 'path': '/metadata/namespace', 'cmp': 'equals', 'value': 'myns'},
            ]),
        ])
