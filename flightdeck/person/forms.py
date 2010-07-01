from django.conf import settings
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm as ContribAuthenticationForm
from django.utils.translation import ugettext_lazy as _

class AuthenticationForm(ContribAuthenticationForm):
	username = forms.CharField(label=_("Email address"), max_length=255)
	
	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			try:
				self.user_cache = authenticate(username=username, password=password)
			except Exception as err:
				raise forms.ValidationError(_("Authentication process is broken please <a href=\"https://bugzilla.mozilla.org/show_bug.cgi?id=570360\">let us know</a>"))

			if self.user_cache is None:
				raise forms.ValidationError(_("""Your email and addons.mozilla.org password didn't match. 
Please try again.
Note that both fields are case-sensitive."""))

			elif not self.user_cache.is_active:
				raise forms.ValidationError(_("This account is inactive."))

		# TODO: determine whether this should move to its own method.
		if self.request:
			if not self.request.session.test_cookie_worked():
				raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

		return self.cleaned_data
