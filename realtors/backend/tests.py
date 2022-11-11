import email
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser('test@mail.com', 'username','firstname','lastname','phone','password')

        self.assertEqual(super_user.email, 'test@mail.com')
        self.assertEqual(super_user.user_name, 'username')
        self.assertEqual(super_user.first_name, 'firstname')
        self.assertEqual(super_user.last_name, 'lastname')
        self.assertEqual(super_user.phone, 'phone')

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)

        self.assertEqual(str(super_user), 'username')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test@mail.com',
                user_name='username',
                first_name='firstname',
                last_name='lastname',
                phone='0700222333',
                password='password',
                is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test@mail.com',
                user_name='username',
                first_name='firstname',
                last_name='lastname',
                phone='0700222333',
                password='password',
                is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='username', first_name='first_name', last_name='last_name', password='password', phone='phone',is_superuser=True)


    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'firstname', 'lastname','phone','password')
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.user_name, 'username')
        self.assertEqual(user.first_name, 'firstname')
        self.assertEqual(user.last_name, 'lastname')
        self.assertEqual(user.phone, 'phone')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', user_name='a', first_name='first_name',last_name = 'last_name', phone='phone',password='password')