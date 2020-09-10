from django.contrib.auth.mixins import UserPassesTestMixin

class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='library_admins').exists()

