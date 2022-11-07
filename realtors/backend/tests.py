import email
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user  = db.objects.create_superuser('testuser@super.com', 'username', 'firstname', 'lastname', 'phone','password')

        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.user_name, 'username')
        self.assertEqual(super_user.first_name, 'firstname')
        self.assertEqual(super_user.last_name, 'lastname')
        self.assertEqual(super_user.phone, 'phone')
        self.assertEqual(super_user.password, 'password')

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)

        self.assertEqual(str(super_user), 'username')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test@super.com',
                user_name='username',
                first_name='firstname',
                last_name='lastname',
                phone='0700222333',
                password='password',
                is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test@super.com',
                user_name='username',
                first_name='firstname',
                last_name='lastname',
                phone='0700222333',
                password='password',
                is_staff=False)