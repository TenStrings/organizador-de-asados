from django.test import TestCase
from django.utils import timezone
from .models import User,Asado,Invitation,Assignment,Supply
from datetime import datetime
# Create your tests here.

class AssignmentTestCase(TestCase):
    def setUp(self):

        space_cola = Supply.objects.create(kind="drink",
                              description='Space-Cola',
                              estimated_cost=25)

        colugo_head = Supply.objects.create(kind="food",
                              description="Colugo's head",
                              estimated_cost=100)

        alibaba = User.objects.create(name="Alibaba")
        sinbad = User.objects.create(name="Sinbad")
        aladdin = User.objects.create(name="Aladdin")

        date = timezone.now()
        asado = Asado.objects.create( organizer=alibaba,
                                      datetime=date,
                                      place='Arabia',
                                      estimated_cost=200)

        Invitation(asado=asado,invite=sinbad)
        Invitation(asado=asado,invite=aladdin)

        self.drink_assignment = Assignment.objects.create(
                                                      asado=asado,
                                                      designated_user=sinbad,
                                                      comment="2L",
                                                      required_supply=space_cola,
                                                      required_quantity=3)

        self.food_assignment = Assignment.objects.create(
                                                     asado=asado,
                                                     designated_user=aladdin,
                                                     required_supply=colugo_head,
                                                     comment="spicy please",
                                                     required_quantity=4)


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
        assignment.finished_with(25)
        self.assertFalse(assignment.fullfilled)
