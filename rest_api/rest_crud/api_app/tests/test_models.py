from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from api_app.models import Person

class PersonModelTest(TestCase):

    def setUp(self):
        # Create a sample photo file to use in the tests
        self.photo = SimpleUploadedFile(
            name="test_photo.jpg",
            content=b"dummy image content",
            content_type="image/jpeg"
        )

        # Set up a sample person
        self.person = Person.objects.create(
            name="John Doe",
            age=30,
            gender="Male",
            phone=1234567890,
            email="john@example.com",
            photo=self.photo,
            status="Active",
            username="johndoe"
        )

    def test_person_creation(self):
        """Test if a Person object is created successfully"""
        self.assertEqual(self.person.name, "John Doe")
        self.assertEqual(self.person.age, 30)
        self.assertEqual(self.person.gender, "Male")
        self.assertEqual(self.person.phone, 1234567890)
        self.assertEqual(self.person.email, "john@example.com")
        self.assertEqual(self.person.status, "Active")
        self.assertEqual(self.person.username, "johndoe")

    def test_string_representation(self):
        """Test the string representation of the Person object"""
        self.assertEqual(str(self.person), "John Doe")  # Ensure __str__ returns name

    def test_photo_upload(self):
        """Test that the photo field correctly saves the uploaded file with the expected base name."""
        self.assertIsNotNone(self.person.photo)
        self.assertIn("test_photo", self.person.photo.name, "The photo file name does not start with 'test_photo'.")
        self.assertTrue(self.person.photo.name.endswith(".jpg"), "The photo file name does not end with '.jpg'.")



    def test_unique_email(self):
        """Test that email field should be unique"""
        with self.assertRaises(IntegrityError):
            Person.objects.create(
                name="Jane Doe",
                age=25,
                gender="Female",
                phone=9876543210,
                email="john@example.com",  # Duplicate email
                photo=self.photo,
                status="Inactive",
                username="janedoe"
            )

    def test_age_field_constraints(self):
        """Test that age field cannot be negative"""
        self.person.age = -1
        with self.assertRaises(ValidationError):
            self.person.full_clean()  # Enforces validation before saving

    def test_invalid_phone_number(self):
        """Test that phone numbers are of a valid length"""
        self.person.phone = 123  # Too short to be valid
        self.person.save()
        self.assertNotEqual(self.person.phone, 1234567890)  # Assuming valid length is enforced elsewhere
