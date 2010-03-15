def create_test_user(username="test_username", password="password", email="test@example.com"):
	from django.contrib.auth.models import User
	from person.models import Profile

	user = User(
		username=username, 
		password=password,
		email=email
	)
	user.save()
	Profile(
		user=user
	).save()
	return user
	

