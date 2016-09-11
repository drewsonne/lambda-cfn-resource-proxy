from unittest import TestCase

from cfn_rscproxy import _build_tag_filters


class Test_build_tag_filters(TestCase):
    def test__build_tag_filters(self):
        tag_filters = _build_tag_filters({
            "Environment": "Testing"
        })

        self.assertEquals(tag_filters[0], {
            'Name': 'tag:Environment',
            'Values': ['Testing']
        })

    def test__build_tag_filters_multi(self):
        tag_filters = _build_tag_filters({
            "Environment": "Testing",
            "Tier": "Web"
        })

        self.assertEquals(tag_filters[0], {
            'Name': 'tag:Environment',
            'Values': ['Testing']
        })

        self.assertEquals(tag_filters[1], {
            'Name': 'tag:Tier',
            'Values': ['Web']
        })
