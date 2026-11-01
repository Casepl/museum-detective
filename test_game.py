import unittest
from copy import deepcopy
from unittest.mock import patch

from main import (
    CLUES,
    CULPRIT_ID,
    FINGERPRINT_LIKELIHOODS,
    SUSPECTS,
    accuse_suspect,
    examine_clue,
    update_probabilities,
)


class TestProbabilities(unittest.TestCase):
    def test_fingerprints_update_probabilities(self):
        suspects = deepcopy(SUSPECTS)

        update_probabilities(
            suspects,
            FINGERPRINT_LIKELIHOODS,
        )

        total_probability = sum(
            suspect["probability"]
            for suspect in suspects.values()
        )

        self.assertAlmostEqual(
            suspects["maria"]["probability"],
            0.73118,
            places=4,
        )

        self.assertAlmostEqual(
            total_probability,
            1.0,
            places=7,
        )

    def test_zero_likelihoods_raise_error(self):
        suspects = deepcopy(SUSPECTS)
        zero_likelihoods = {
            "alexey": 0.0,
            "maria": 0.0,
            "viktor": 0.0,
        }

        with self.assertRaises(ValueError):
            update_probabilities(suspects, zero_likelihoods)

    def test_every_clue_has_likelihoods_for_every_suspect(self):
        suspect_ids = set(SUSPECTS)

        for clue in CLUES.values():
            self.assertEqual(set(clue["likelihoods"]), suspect_ids)


class TestClues(unittest.TestCase):
    def setUp(self):
        self.suspects = deepcopy(SUSPECTS)
        self.clues = deepcopy(CLUES)
        self.used_evidence_groups = set()

    def test_dependent_evidence_group_is_applied_once(self):
        with patch("builtins.input", side_effect=["1", "4"]), patch(
            "builtins.print"
        ):
            examine_clue(
                self.clues,
                self.suspects,
                self.used_evidence_groups,
            )
            probability_after_camera = self.suspects["alexey"]["probability"]

            examine_clue(
                self.clues,
                self.suspects,
                self.used_evidence_groups,
            )

        self.assertAlmostEqual(
            self.suspects["alexey"]["probability"],
            probability_after_camera,
            places=7,
        )
        self.assertEqual(
            self.used_evidence_groups,
            {"corridor_presence"},
        )
        self.assertTrue(self.clues["1"]["examined"])
        self.assertTrue(self.clues["4"]["examined"])

    def test_same_clue_is_not_applied_twice(self):
        with patch("builtins.input", side_effect=["2", "2"]), patch(
            "builtins.print"
        ):
            examine_clue(
                self.clues,
                self.suspects,
                self.used_evidence_groups,
            )
            probability_after_first_examination = self.suspects["maria"][
                "probability"
            ]

            examine_clue(
                self.clues,
                self.suspects,
                self.used_evidence_groups,
            )

        self.assertAlmostEqual(
            self.suspects["maria"]["probability"],
            probability_after_first_examination,
            places=7,
        )

    def test_unknown_clue_does_not_change_state(self):
        initial_suspects = deepcopy(self.suspects)

        with patch("builtins.input", return_value="9"), patch(
            "builtins.print"
        ):
            examine_clue(
                self.clues,
                self.suspects,
                self.used_evidence_groups,
            )

        self.assertEqual(self.suspects, initial_suspects)
        self.assertEqual(self.used_evidence_groups, set())
        self.assertFalse(any(clue["examined"] for clue in self.clues.values()))


class TestAccusation(unittest.TestCase):
    def test_correct_accusation_finishes_investigation(self):
        with patch("builtins.input", return_value=CULPRIT_ID), patch(
            "builtins.print"
        ):
            result = accuse_suspect(SUSPECTS, CULPRIT_ID)

        self.assertTrue(result)

    def test_wrong_known_accusation_finishes_investigation(self):
        with patch("builtins.input", return_value="alexey"), patch(
            "builtins.print"
        ):
            result = accuse_suspect(SUSPECTS, CULPRIT_ID)

        self.assertTrue(result)

    def test_unknown_suspect_does_not_finish_investigation(self):
        with patch("builtins.input", return_value="sergey"), patch(
            "builtins.print"
        ):
            result = accuse_suspect(SUSPECTS, CULPRIT_ID)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
