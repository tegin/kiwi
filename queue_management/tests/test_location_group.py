# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestLocationGroup(TransactionCase):
    def setUp(self):
        super().setUp()

    def test_creation_group(self):
        group1 = self.env["queue.location.group"].create({"name": "Test_Group1"})
        self.assertEqual(group1.name, "Test_Group1")

    def test_relation_location_group(self):
        group1 = self.env["queue.location.group"].create({"name": "Test_Group1"})
        group2 = self.env["queue.location.group"].create({"name": "Test_Group2"})

        location1 = self.env["queue.location"].create(
            {"name": "Test_Location", "group_ids": [(4, group1.id), (4, group2.id)]}
        )

        location2 = self.env["queue.location"].create({"name": "Test_Location2"})

        group1.location_ids += location2

        self.assertIn(group1, location1.group_ids)
        self.assertTrue(location1 in group1.location_ids)
        self.assertTrue(location2 in group1.location_ids)
