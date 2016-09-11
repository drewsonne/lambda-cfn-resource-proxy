from unittest import TestCase

from cfn_rscproxy import _get_resource_finder


class Test_get_resource_finder(TestCase):
    def test__get_resource_finder_vpc(self):
        rsc_finder = _get_resource_finder('AWS::EC2::VPC')
        self.assertEquals(
            'filter',
            rsc_finder.__name__
        )

        self.assertEquals(
            'ec2.vpcsCollectionManager',
            rsc_finder.im_class.__name__
        )

    def test__get_resource_finder_subnet(self):
        rsc_finder = _get_resource_finder('AWS::EC2::Subnet')
        self.assertEquals(
            'filter',
            rsc_finder.__name__
        )

        self.assertEquals(
            'ec2.subnetsCollectionManager',
            rsc_finder.im_class.__name__
        )
