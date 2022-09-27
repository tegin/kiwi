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
        We expect an error if the token has the wrong location.
        """
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.with_context(
                location_id=self.location_2.id
            ).action_assign()

    def test_assignation_location_not_in_group(self):
        """
        We are expecting an error if I try to assign a token to a wrong location.
        """
        with self.assertRaises(ValidationError):
            self.token_g1.location_ids.with_context(
                location_id=self.location_2.id
            ).action_assign()

    def test_assignation_error_assigned(self):
        """
        If we try to assign a token that is already assigned, an error will be raised.
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
        We want to test the use case when we assign a token directly to a location.
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
        """
        We expect that when a new token is assigned to the location, the state
        of the previous token will change to done.
        """
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
        We ensure that an error is raised if no location is defined on assignation
        """
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.action_assign()

    def test_leave_wrong_location(self):
        """
        An error is raised if we relase a token from a location that
        is not assigned to it.
        """
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g3.location_ids.with_context(
                location_id=self.location_2.id
            ).action_leave()

    def test_leave_error_leave_done(self):
        """
        We check that the token con only be released once.
        """
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
        """
        We ensure that we can only release if the token has already been assigned.
        """
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.with_context(
                location_id=self.location_1.id
            ).action_leave()

    def test_leave_exception_no_location(self):
        """
        We ensure that an error is raised when we release a token
        from an undefined location.
        """
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g3.location_ids.action_leave()

    def test_token_with_two_locations_error(self):
        """
        We cannot have a token with two different locations in state assigned
        """
        token = self.env["queue.token"].create({})
        token_location_1 = self.env["queue.token.location"].create(
            {"token_id": token.id, "location_id": self.location_1.id}
        )
        token_location_2 = self.env["queue.token.location"].create(
            {"token_id": token.id, "location_id": self.location_2.id}
        )
        token_location_1.with_context(location_id=self.location_1.id).action_assign()
        with self.assertRaises(ValidationError):
            token_location_2.with_context(
                location_id=self.location_2.id
            ).action_assign()

    def test_token_with_two_locations(self):
        """
        We check how to manage a token with two different locations

        First we manage one of them, then the other one
        """
        token = self.env["queue.token"].create({})
        token_location_1 = self.env["queue.token.location"].create(
            {"token_id": token.id, "location_id": self.location_1.id}
        )
        token_location_2 = self.env["queue.token.location"].create(
            {"token_id": token.id, "location_id": self.location_2.id}
        )
        token_location_1.with_context(location_id=self.location_1.id).action_assign()
        token_location_1.with_context(location_id=self.location_1.id).action_leave()
        token_location_2.with_context(location_id=self.location_2.id).action_assign()
        token_location_2.with_context(location_id=self.location_2.id).action_leave()
        self.assertEqual(token_location_1.state, "done")
        self.assertEqual(token_location_2.state, "done")

    def test_back_to_draft_group(self):
        """
        We check the back to draft functionality on assigned to group.

        We assign a token to location 1
        We set the token back to draft
        We assign the token to location 2
        """
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.assertEqual(self.token_g3.location_ids.location_id, self.location_1)
        self.assertEqual(self.token_g3.location_ids.state, "in-progress")
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_back_to_draft()
        self.assertEqual(self.token_g3.location_ids.state, "draft")
        self.assertFalse(self.token_g3.location_ids.location_id)
        # Now we are able to assign it to another location without any issues
        self.token_g3.location_ids.with_context(
            location_id=self.location_2.id
        ).action_assign()
        self.assertEqual(self.token_g3.location_ids.location_id, self.location_2)
        self.assertEqual(self.token_g3.location_ids.state, "in-progress")

    def test_back_to_draft_location(self):
        """
        We check the back to draft functionality on assigned to a specific location
        """
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.assertEqual(self.token_l1.location_ids.state, "in-progress")
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_back_to_draft()
        self.assertEqual(self.token_l1.location_ids.state, "draft")
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.assertEqual(self.token_l1.location_ids.state, "in-progress")

    def test_back_to_draft_error_bad_location(self):
        """
        We cannot set a token location back to draft from a wrong location
        """
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g3.location_ids.with_context(
                location_id=self.location_2.id
            ).action_back_to_draft()

    def test_back_to_draft_error_no_location(self):
        """
        We cannot set a token location back to draft from a wrong location
        """
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g3.location_ids.action_back_to_draft()

    def test_back_to_draft_error_bad_state(self):
        """
        We cannot back to draft a token that is not in "in-progress" state
        """
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_leave()
        with self.assertRaises(ValidationError):
            self.token_g3.location_ids.with_context(
                location_id=self.location_1.id
            ).action_back_to_draft()
