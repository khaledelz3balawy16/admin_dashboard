from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Create individual coach accounts with restricted access'

    def handle(self, *args, **options):
        # List of coach names with emails - each can log in with name or email
        coaches = [
            {"name": "Omar Elshafey", "email": "contact@example.com"},
            {"name": "Radwa Samir", "email": "contact@example.com"},
            {"name": "Omar Badr", "email": "contact@example.com"},
            {"name": "Ahmed Maher", "email": "contact@example.com"},
            {"name": "Femi Falodun", "email": "contact@example.com"},
            {"name": "Nathan Shields", "email": "contact@example.com"},
            {"name": "Hannen Mostafa", "email": "contact@example.com"},
            {"name": "Nouran Abdalla", "email": "contact@example.com"},
            {"name": "Afaan Khan", "email": "contact@example.com"},
            {"name": "Adeyemi Adeshina", "email": "contact@example.com"},
            {"name": "Marwa Mahmoud", "email": "contact@example.com"},
            {"name": "Mahinor Hesham", "email": "contact@example.com"},
            {"name": "Omar Ham", "email": "contact@example.com"},
            {"name": "Aryan Harikumar", "email": "contact@example.com"},
            {"name": "Elaf Mansour", "email": "contact@example.com"},
            {"name": "Olivia Evans", "email": "contact@example.com"},
            {"name": "Patryk Zajac", "email": "contact@example.com"},
        ]

        password = "CHANGE_ME"
        created_count = 0
        updated_count = 0

        for idx, coach_data in enumerate(coaches, start=1):
            # Use coach_id as the sequential number
            coach_id = str(idx)
            coach_name = coach_data["name"]
            coach_email = coach_data["email"]

            # Check if user already exists
            user, created = User.objects.get_or_create(
                username=coach_name,
                defaults={
                    'first_name': coach_name.split()[0],
                    'last_name': ' '.join(coach_name.split()[1:]) if len(coach_name.split()) > 1 else '',
                    'email': coach_email,
                }
            )

            # Set password and email (will update if user already exists)
            user.set_password(password)
            user.email = coach_email
            user.save()

            # Create or update profile
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'coach',
                    'coach_id': coach_id,
                }
            )

            # Update profile if it already exists
            if not profile_created:
                profile.role = 'coach'
                profile.coach_id = coach_id
                profile.save()
                updated_count += 1
            else:
                created_count += 1

            status = "created" if created else "updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ {status.capitalize()} coach account: {coach_name} | Email: {coach_email} (coach_id: {coach_id})'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Done! Created {created_count} new accounts, updated {updated_count} existing accounts.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Password for all coach accounts: {password}'
            )
        )
