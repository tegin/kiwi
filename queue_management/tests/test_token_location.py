# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestTokenLocation(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_1 = cls.env["queue.location.group"].create({"name": "G1"})
        cls.group_2 = cls.env["queue.location.group"].create({"name": "G2"})
        cls.group_3 = cls.env["queue.location.group"].create({"name": "G3"})
        cls.location_1 = cls.env["queue.location"].create(
            {"name": "L1", "group_ids": [(4, cls.group_1.id), (4, cls.group_3.id)]}
        )
        cls.location_2 = cls.env["queue.location"].create(
            {"name": "L2", "group_ids": [(4, cls.group_2.id), (4, cls.group_3.id)]}
        )

        cls.token_l1 = cls.env["queue.token"].create(
            {"location_ids": [(0, 0, {"location_id": cls.location_1.id})]}
        )
        cls.token_l2 = cls.env["queue.token"].create(
            {"location_ids": [(0, 0, {"location_id": cls.location_2.id})]}
        )
        cls.token_g1 = cls.env["queue.token"].create(
            {"location_ids": [(0, 0, {"group_id": cls.group_1.id})]}
        )
        cls.token_g2 = cls.env["queue.token"].create(
            {"location_ids": [(0, 0, {"group_id": cls.group_2.id})]}
        )
        cls.token_g3 = cls.env["queue.token"].create(
            {"location_ids": [(0, 0, {"group_id": cls.group_3.id})]}
        )

    def test_location_items(self):
        self.assertIn(
            self.token_g1, self.location_1.token_location_ids.mapped("token_id")
        )
        self.assertNotIn(
            self.token_g1, self.location_2.token_location_ids.mapped("token_id")
        )
        self.assertNotIn(
            self.token_g2, self.location_1.token_location_ids.mapped("token_id")
        )
        self.assertIn(
            self.token_g2, self.location_2.token_location_ids.mapped("token_id")
        )
        self.assertIn(
            self.token_g3, self.location_1.token_location_ids.mapped("token_id")
        )
        self.assertIn(
            self.token_g3, self.location_2.token_location_ids.mapped("token_id")
        )
        self.assertIn(
            self.token_l1, self.location_1.token_location_ids.mapped("token_id")
        )
        self.assertNotIn(
            self.token_l1, self.location_2.token_location_ids.mapped("token_id")
        )
        self.assertNotIn(
            self.token_l2, self.location_1.token_location_ids.mapped("token_id")
        )
        self.assertIn(
            self.token_l2, self.location_2.token_location_ids.mapped("token_id")
        )

    def test_assignation_wrong_location(self):
        """
        En el contexto l2 sale un error al asignar token_l1 (que solo esta en l1).
        """
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.with_context(
                location_id=self.location_2.id
            ).action_assign()

    def test_assignation_location_not_in_group(self):
        """
        En el contexto l2 sale un error al asignar token_g1 (l2 no forma parte de g1).
        """
        with self.assertRaises(ValidationError):
            self.token_g1.location_ids.with_context(
                location_id=self.location_2.id
            ).action_assign()

    def test_assignation_error_assigned(self):
        """
        Se assignan que l1 a token_g1. En el contexto l1 sale un error al assignar
        token_g1 pq ya esta asigando previamente en el 1r passo.
        """
        self.token_g1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g1.location_ids.with_context(
                location_id=self.location_1.id
            ).action_assign()

    def test_group(self):
        """
        We want to test how it will be managed in a token assigned to a Group
        1-  Token will be assigned to a location related to the group.
            Location of the token will be forced as the assigned location
        2-  Token leaves the location, then the state changes

        Also, we test the done tokens of the location.
        Before step 2 it should be empty, after step 2 it should be the token
        """
        self.assertFalse(self.token_g1.location_ids.location_id)
        self.assertEqual(self.token_g1.location_ids.state, "draft")

        self.token_g1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.assertEqual(self.token_g1.location_ids.location_id, self.location_1)
        self.assertEqual(self.token_g1.location_ids.state, "in-progress")
        self.assertNotIn(
            self.token_g1.location_ids, self.location_1.token_location_done_ids
        )
        self.token_g1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_leave()
        self.assertEqual(self.token_g1.location_ids.state, "done")
        # We need to refresh the location because depends are not related to token.location
        self.location_1.refresh()
        self.assertIn(
            self.token_g1, self.location_1.token_location_done_ids.mapped("token_id")
        )

    def test_location(self):
        """
        Sale error estado de token_l1 s draft
         al intentar asignar una localizacion que ya existe, cunado el estado
        del token es in-progress, y

        """
        self.assertEqual(self.token_l1.location_ids.state, "draft")

        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.assertEqual(self.token_l1.location_ids.state, "in-progress")
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_leave()
        self.assertEqual(self.token_l1.location_ids.state, "done")

    def test_assign_chained(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.assertEqual(self.token_l1.location_ids.state, "in-progress")
        self.token_g1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.assertEqual(self.token_l1.location_ids.state, "done")

    def test_assignation_exception_no_location(self):
        """
        Sale error al intentar asignar una localizacion que no existe
        """
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.action_assign()

    def test_leave_wrong_location(self):
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g3.location_ids.with_context(
                location_id=self.location_2.id
            ).action_leave()

    def test_leave_error_leave_done(self):
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_leave()
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.with_context(
                location_id=self.location_1.id
            ).action_leave()

    def test_leave_error_leave_draft(self):
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.with_context(
                location_id=self.location_1.id
            ).action_leave()

    def test_leave_exception_no_location(self):
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g3.location_ids.action_leave()
