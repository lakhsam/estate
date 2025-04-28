from odoo.tests.common import TransactionCase

class TestProperty(TransactionCase):

    def setUp(self):
        super(TestProperty, self).setUp()
        self.Property = self.env['property']
        self.Owner = self.env['owner']

    def test_create_property(self):
        # Create an owner
        owner = self.Owner.create({
            'name': 'John Doe',
            'phone': '123456789',
            'address': '123 Main St',
        })

        # Create a property
        property = self.Property.create({
            'name': 'Test Property',
            'postcode': '12345',
            'owner_id': owner.id,
            'expected_price': 100000,
            'selling_price': 95000,
            'bedrooms': 3,
        })

        # Check that the property was created
        self.assertEqual(property.name, 'Test Property')
        self.assertEqual(property.owner_id.name, 'John Doe')
        self.assertEqual(property.bedrooms, 3)

    def test_property_state_change(self):
        # Create a property
        property = self.Property.create({
            'name': 'State Test Property',
            'postcode': '54321',
            'expected_price': 200000,
            'selling_price': 190000,
            'bedrooms': 4,
        })

        # Change state to 'sold'
        property.action_sold()
        self.assertEqual(property.state, 'sold')

        # Change state to 'closed'
        property.action_closed()
        self.assertEqual(property.state, 'closed') 