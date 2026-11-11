import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import UserProfile
from detection.models import MessageAnalysis, Feedback
from reports.models import CyberbullyingReport
from detection.services import process_and_save_analysis


class Command(BaseCommand):
    help = "Seeds database with admin user, demo users, sample analyses, and incident reports."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding for CyberShield AI..."))

        # 1. Create Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@cybershield.ai',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
            admin_profile.role = 'admin'
            admin_profile.bio = 'Chief CyberShield Safety Administrator and Security Architect.'
            admin_profile.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Create Moderator & Demo User
        mod_user, _ = User.objects.get_or_create(
            username='moderator_alice',
            defaults={
                'email': 'alice@cybershield.ai',
                'first_name': 'Alice',
                'last_name': 'Moderator',
                'is_staff': True,
            }
        )
        mod_user.set_password('moderator123')
        mod_user.save()
        mod_profile, _ = UserProfile.objects.get_or_create(user=mod_user)
        mod_profile.role = 'moderator'
        mod_profile.save()

        demo_user, _ = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )
        demo_user.set_password('user1234')
        demo_user.save()

        # 3. Seed Sample Message Analyses
        seed_messages = [
            ("Great tutorial! Really helped me understand machine learning concepts easily.", demo_user),
            ("Delete your account loser, nobody here wants you around. Go disappear.", demo_user),
            ("I will find where you live and beat you unconscious tonight. Watch your back.", None),
            ("You are an extraordinarily dumb clown who fails at everything you touch.", demo_user),
            ("Filthy subhuman parasites need to be kicked out of our country right now.", None),
            ("Shut your fucking face you absolute piece of shit, go drown yourself.", demo_user),
            ("Send your naked photos right now or I will leak all your private data online.", None),
            ("Looking forward to the hackathon this weekend! Good luck to every participant.", mod_user),
            ("Stop posting your disgusting face, it makes everyone feel sick looking at you.", demo_user),
            ("I swear I will break your neck if I ever see you walking down our street.", None),
            ("Can anyone recommend a good open-source library for interactive chart visualization?", mod_user),
            ("You are a pathetic waste of oxygen, why are you even still breathing?", None),
            ("We need to purge these foreign rats before they destroy our pure society.", None),
            ("Fuck off and stop crying like a little bitch every single day.", demo_user),
            ("Wonderful community initiative to help kids learn coding and digital safety.", admin_user),
            ("I am outside your apartment building right now with a knife, come down.", None),
            ("You are the ugliest human alive, mirrors probably crack when you look at them.", demo_user),
            ("Thank you for your constructive review on my GitHub pull request!", mod_user),
        ]

        now = timezone.now()
        count = 0
        for text, user in seed_messages:
            res = process_and_save_analysis(text, user=user)
            if res.get('success') and 'id' in res:
                analysis = MessageAnalysis.objects.get(id=res['id'])
                # Randomize timestamp over past 6 days to populate Chart.js trends
                days_offset = random.randint(0, 6)
                hours_offset = random.randint(1, 23)
                fake_time = now - timedelta(days=days_offset, hours=hours_offset)
                MessageAnalysis.objects.filter(id=analysis.id).update(created_at=fake_time)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {count} realistic MessageAnalysis records."))

        # 4. Seed Cyberbullying Reports
        report_seeds = [
            {
                'title': "Repeated Death Threats in Discord Direct Messages",
                'offensive_message': "I will find where you live and break your neck tonight. Sleep with one eye open.",
                'platform': "Discord",
                'category': "Threatening Language",
                'description': "User 'dark_phantom' joined our university server and began sending direct messages threatening physical violence after a debate.",
                'status': "Under Review",
                'admin_notes': "IP logs preserved. Discord safety trust report filed. Incident escalated to campus security.",
                'user': demo_user
            },
            {
                'title': "Severe Cyberstalking and Body Shaming on Instagram",
                'offensive_message': "You look like a disgusting fat pig who should never show their face in public again.",
                'platform': "Instagram",
                'category': "Personal Attack",
                'description': "An anonymous account has been reposting my personal vacation photos with abusive captions and tagging all my followers.",
                'status': "Pending",
                'admin_notes': "",
                'user': demo_user
            },
            {
                'title': "Nonconsensual Image Sharing Extortion on WhatsApp",
                'offensive_message': "Send me $500 or more explicit photos right now or I leak everything to your family.",
                'platform': "WhatsApp / Telegram",
                'category': "Sexual Harassment",
                'description': "Blackmail attempt using stolen private media from an old phone backup.",
                'status': "Resolved",
                'admin_notes': "Advised victim to freeze contact, do not pay, and reported through national cybercrime portal.",
                'user': None
            },
            {
                'title': "Organized Hate Raid on YouTube Live Stream",
                'offensive_message': "All immigrants of your filthy race are subhumans who need to be eliminated.",
                'platform': "YouTube",
                'category': "Hate Speech",
                'description': "A group of 30 bots flooded my cultural education stream with racial slurs and Nazi imagery.",
                'status': "Resolved",
                'admin_notes': "Automated filter rules added, video comment moderation enabled.",
                'user': mod_user
            }
        ]

        for rep_data in report_seeds:
            CyberbullyingReport.objects.get_or_create(
                title=rep_data['title'],
                defaults=rep_data
            )

        self.stdout.write(self.style.SUCCESS("Seeded sample Cyberbullying incident reports."))
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
