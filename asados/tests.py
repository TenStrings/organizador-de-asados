from django.test import TestCase
from django.utils import timezone
from .models import (
    User, Asado, Invitation, Assignment, Supply, AssignmentValidationError
)
from django.core.exceptions import ValidationError
from datetime import datetime


class AsadooTest(TestCase):

    def setUp(self):
        self.pyetr = User.objects.create(name='Pyetr')
        self.balalaika = User.objects.create(name='Balalaika')

        self.asado = Asado.objects.create(
            organizer=self.pyetr,
            datetime=timezone.now(),
            place='Russya'
        )

    def test01_new_asado_has_no_invites(self):
        self.assertFalse(self.asado.attendee.all())

    def test02_can_invite_people_to_asado(self):
        Invitation.objects.create(
            asado=self.asado,
            invite=self.balalaika
        )

    def test03_can_not_invite_organizer_to_his_own_asado(self):
        with self.assertRaises(
            ValidationError,
            msg=Invitation.VALIDATION_ERROR_MSG
        ):
            Invitation.objects.create(
                asado=self.asado,
                invite=self.pyetr
            )


class AssignmentTestCase(TestCase):
    def setUp(self):

        space_cola = Supply.objects.create(
            kind='drink',
            description='Space-Cola',
            estimated_cost=25
        )

        colugo_head = Supply.objects.create(
            kind='food',
            description="Colugo's head",
            estimated_cost=100
        )

        alibaba = User.objects.create(name="Alibaba")
        sinbad = User.objects.create(name="Sinbad")
        aladdin = User.objects.create(name="Aladdin")

        date = timezone.now()
        asado = Asado.objects.create(
            organizer=alibaba,
            datetime=date,
            place='Arabia'
        )

        Invitation.objects.create(asado=asado, invite=sinbad)
        Invitation.objects.create(asado=asado, invite=aladdin)

        self.drink_assignment = Assignment.objects.create(
            asado=asado,
            designated_user=sinbad,
            comment='2L',
            required_supply=space_cola,
            required_quantity=3
        )

        self.food_assignment = Assignment.objects.create(
            asado=asado,
            designated_user=aladdin,
            required_supply=colugo_head,
            comment='spicy please',
            required_quantity=4
        )

    def test01_creation_works(self):
        pass

    def test02_can_finish_drink_with_any_quantity(self):
        assignment = self.drink_assignment
        assignment.finished_with(12)
        self.assertTrue(assignment.fullfilled)

    def test03_can_finish_food_with_proper_quantity(self):
        assignment = self.food_assignment
        assignment.finished_with(4)
        self.assertTrue(assignment.fullfilled)

    def test04_can_not_finish_food_with_any_quantity(self):
        assignment = self.food_assignment
        with self.assertRaises(AssignmentValidationError):
            assignment.finished_with(25)
            self.assertFalse(assignment.fullfilled)
