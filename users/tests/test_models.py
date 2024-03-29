import pytest

from users.models import User, Address, get_file_path

pytestmark = pytest.mark.django_db


@pytest.fixture()
def user():
    return User.objects.create_user(
        email='user@email.com',
        password='4231django',
        first_name='User',
        last_name='Name',
        cpf='000.000.000-00',
    )


@pytest.fixture()
def superuser():
    return User.objects.create_superuser(
        email='superuser@email.com',
        password='4231django',
        first_name='Superuser',
        last_name='Name',
        cpf='111.111.111-11'
    )


@pytest.fixture()
def address():
    return Address(
        zip_code='00000-000',
        address='Address',
        house_number='123',
        complement='Complement',
        neighborhood='Neighborhood',
        city='City',
        state='State'
    )


def test_user_attributes(user):
    assert not user.is_staff
    assert not user.is_superuser
    assert user.email == 'user@email.com'
    assert user.first_name == 'User'
    assert user.last_name == 'Name'
    assert user.cpf == '000.000.000-00'


def test_superuser_attributes(superuser):
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.email == 'superuser@email.com'
    assert superuser.first_name == 'Superuser'
    assert superuser.last_name == 'Name'
    assert superuser.cpf == '111.111.111-11'


def test_user_model_str(user, superuser):
    assert user.email == str(user)
    assert superuser.email == str(superuser)


def test_superuser_with_superuser_attribute_false():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='superuserSuperuserFalse@email.com',
            password='4231django',
            first_name='SuperuserFalse',
            last_name='Name',
            cpf='222.222.222-22',
            is_superuser=False
        )


def test_superuser_with_is_staff_attribute_false():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='superuserStaffFalse@email.com',
            password='4231django',
            first_name='SuperuserStaffFalse',
            last_name='Name',
            cpf='333.333.333-33',
            is_staff=False
        )


def test_user_without_email():
    with pytest.raises(ValueError):
        User.objects.create_user(
            email=None,
            password='4231django',
            first_name='User',
            last_name='Last',
            cpf='444.444.444-44'
        )


def test_address_attributes(address):
    assert address.zip_code == '00000-000'
    assert address.address == 'Address'
    assert address.house_number == '123'
    assert address.complement == 'Complement'
    assert address.neighborhood == 'Neighborhood'
    assert address.city == 'City'
    assert address.state == 'State'


def test_address_str(address):
    assert str(address) == address.address


def test_get_file_path(user):
    image = get_file_path(user, 'image.ext')
    dir = image.split('.')[0].split('/')[0]
    image_name = image.split('.')[0].split('/')[1]
    ext = image.split('.')[-1]
    assert dir == 'users'
    assert len(image_name) == 36
    assert ext == 'ext'
