from django.contrib.auth.management.commands import createsuperuser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        def validate_password(password):
            if len(password) < 8:
                raise ValidationError(_("Password must be at least 8 characters long"))
            if not any(char.isdigit() for char in password):
                raise ValidationError(_("Password must contain at least one digit"))
            if not any(char.isupper() for char in password):
                raise ValidationError(_("Password must contain at least one uppercase letter"))
            if not any(char in "!@#$%^&*()" for char in password):
                raise ValidationError(_("Password must contain at least one special character"))
        
        username = options["username"]
        email = options["email"]
        password = options["password1"]
        
        try:
            validate_password(password)
        except ValidationError as e:
            self.stderr.write(str(e))
            return

        super().handle(*args, **options)