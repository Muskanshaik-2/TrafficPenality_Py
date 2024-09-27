

class Penalty:
    def __init__(self, penalty_id, amount, penalty_description):
        self.penalty_id = penalty_id
        self.amount = amount
        self.penalty_description = penalty_description
        self.is_paid = False

    def __repr__(self):
        return f"Penalty(id={self.penalty_id}, amount={self.amount}, description='{self.penalty_description}', is_paid={self.is_paid})"


class Payment:
    def __init__(self, payment_id, penalty_id, amount_paid, payment_status):
        self.payment_id = payment_id
        self.penalty_id = penalty_id
        self.amount_paid = amount_paid
        self.payment_status = payment_status

    def __repr__(self):
        return f"Payment(id={self.payment_id}, penalty_id={self.penalty_id}, amount_paid={self.amount_paid}, status='{self.payment_status}')"


class TrafficPenaltySystem:
    def __init__(self):
        self.penalties = {}  # dictionary to store penalties
        self.payments = {}   # dictionary to store payments
        self.penalty_counter = 1
        self.payment_counter = 1

    def create_penalty(self, amount, penalty_description):
        penalty_id = self.penalty_counter
        penalty = Penalty(penalty_id, amount, penalty_description)
        self.penalties[penalty_id] = penalty
        self.penalty_counter += 1
        return penalty

    def read_penalty(self, penalty_id):
        return self.penalties.get(penalty_id, None)

    def update_penalty(self, penalty_id, amount=None, penalty_description=None):
        penalty = self.penalties.get(penalty_id)
        if penalty:
            if amount is not None:
                penalty.amount = amount
            if penalty_description is not None:
                penalty.penalty_description = penalty_description
            return penalty
        return None

    def delete_penalty(self, penalty_id):
        return self.penalties.pop(penalty_id, None)

    def process_payment(self, penalty_id, amount_paid):
        penalty = self.penalties.get(penalty_id)
        if penalty and not penalty.is_paid:
            payment_id = self.payment_counter
            payment_status = "Completed" if amount_paid >= penalty.amount else "Pending"
            payment = Payment(payment_id, penalty_id, amount_paid, payment_status)
            self.payments[payment_id] = payment

            if payment_status == "Completed":
                penalty.is_paid = True

            self.payment_counter += 1
            return payment
        return None

    def track_payments(self, penalty_id):
        return [payment for payment in self.payments.values() if payment.penalty_id == penalty_id]

    def get_all_penalties(self):
        return list(self.penalties.values())

    def get_all_payments(self):
        return list(self.payments.values())
# test_traffic_penalty.py

import unittest

class TestTrafficPenaltySystem(unittest.TestCase):
    def setUp(self):
        self.system = TrafficPenaltySystem()

    def test_create_penalty(self):
        penalty = self.system.create_penalty(100, "Speeding")
        self.assertEqual(len(self.system.penalties), 1)
        self.assertEqual(penalty.penalty_description, "Speeding")

    def test_read_penalty(self):
        self.system.create_penalty(100, "Speeding")
        penalty = self.system.read_penalty(1)
        self.assertEqual(penalty.penalty_description, "Speeding")

    def test_update_penalty(self):
        self.system.create_penalty(100, "Speeding")
        updated_penalty = self.system.update_penalty(1, amount=120)
        self.assertEqual(updated_penalty.amount, 120)

    def test_delete_penalty(self):
        self.system.create_penalty(100, "Speeding")
        self.system.delete_penalty(1)
        self.assertIsNone(self.system.read_penalty(1))

    def test_process_payment(self):
        self.system.create_penalty(100, "Speeding")
        payment = self.system.process_payment(1, 100)
        self.assertEqual(payment.payment_status, "Completed")
        self.assertTrue(self.system.read_penalty(1).is_paid)

    def test_track_payments(self):
        self.system.create_penalty(100, "Speeding")
        self.system.process_payment(1, 100)
        payments = self.system.track_payments(1)
        self.assertEqual(len(payments), 1)
        self.assertEqual(payments[0].amount_paid, 100)

if __name__ == "__main__":
    unittest.main()

