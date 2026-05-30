"""
Seed modules, pre/post assessment quizzes, and simulation templates.
Usage:
    python manage.py seed_platform_data
    python manage.py seed_platform_data --clear   # wipe and re-seed
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify


# ─── Modules ──────────────────────────────────────────────────────────────────

MODULES = [
    {
        'title': 'Introduction to Phishing',
        'category_slug': 'phishing-fundamentals',
        'module_type': 'general',
        'difficulty': 'beginner',
        'description': 'Understand what phishing is, how it started, and why it remains one of the most dangerous cyber threats today.',
        'content': """<h4>What is Phishing?</h4>
<p>Phishing is a type of cyber attack where criminals impersonate legitimate organisations or people to trick victims into revealing sensitive information such as passwords, credit card numbers, or personal data.</p>
<h4>A Brief History</h4>
<p>Phishing started in the mid-1990s when hackers targeted AOL users by pretending to be AOL staff to steal passwords. The term "phishing" comes from "fishing" — casting a wide net hoping someone takes the bait.</p>
<h4>Why Is It So Common?</h4>
<ul>
<li>It exploits human psychology, not technical vulnerabilities</li>
<li>It is cheap and easy to launch at scale</li>
<li>It has a high success rate even against security-aware users</li>
<li>It does not require advanced hacking skills</li>
</ul>
<h4>Key Statistics</h4>
<p>Over 90% of successful cyber attacks begin with a phishing email. Billions of phishing emails are sent every day worldwide.</p>
<h4>What Attackers Want</h4>
<ul>
<li>Login credentials (username and password)</li>
<li>Banking and credit card details</li>
<li>Personal identification information</li>
<li>Access to corporate systems</li>
</ul>""",
        'duration_minutes': 10,
        'points': 10,
        'order': 1,
    },
    {
        'title': 'Recognising Phishing Emails',
        'category_slug': 'email-phishing',
        'module_type': 'email_phishing',
        'difficulty': 'beginner',
        'description': 'Learn the key red flags that identify a phishing email and how to verify suspicious messages.',
        'content': """<h4>Red Flags in Phishing Emails</h4>
<p>Phishing emails have tell-tale signs if you know what to look for:</p>
<h5>1. Suspicious Sender Address</h5>
<p>The display name may look legitimate (e.g. "PayPal Support") but the actual email address is different (e.g. support@paypa1-secure.com). Always check the full email address, not just the display name.</p>
<h5>2. Urgency and Threats</h5>
<p>Phrases like "Your account will be suspended in 24 hours", "Immediate action required", or "Verify now or lose access" are designed to panic you into acting without thinking.</p>
<h5>3. Suspicious Links</h5>
<p>Hover over any link before clicking. The URL shown in the bottom bar should match the expected domain. Watch out for:</p>
<ul>
<li>Misspelled domains: paypa1.com, g00gle.com</li>
<li>Extra subdomains: paypal.com.verify-account.net</li>
<li>URL shorteners hiding the real destination</li>
</ul>
<h5>4. Poor Grammar and Spelling</h5>
<p>Many phishing emails contain obvious spelling mistakes, awkward phrasing, or poor formatting.</p>
<h5>5. Generic Greetings</h5>
<p>"Dear Customer" or "Dear User" instead of your actual name can indicate a mass phishing campaign.</p>
<h5>6. Unexpected Attachments</h5>
<p>Never open unexpected attachments, especially .exe, .zip, .docm files. Even Word documents can contain macros that install malware.</p>
<h4>What To Do When You Receive a Suspicious Email</h4>
<ol>
<li>Do not click any links or download attachments</li>
<li>Do not reply to the email</li>
<li>Report it to your IT team or email provider</li>
<li>If it claims to be from a known company, contact them directly using their official website</li>
<li>Delete the email</li>
</ol>""",
        'duration_minutes': 15,
        'points': 15,
        'order': 1,
    },
    {
        'title': 'SMS Phishing (Smishing)',
        'category_slug': 'sms-mobile-phishing',
        'module_type': 'sms_phishing',
        'difficulty': 'beginner',
        'description': 'Learn how criminals use SMS text messages to steal your information and how to protect yourself.',
        'content': """<h4>What is Smishing?</h4>
<p>Smishing (SMS + phishing) is phishing carried out through text messages. Attackers send fake SMS messages pretending to be banks, delivery services, or government agencies.</p>
<h4>Common Smishing Scenarios</h4>
<ul>
<li><strong>Fake delivery notification:</strong> "Your parcel could not be delivered. Click here to reschedule: [link]"</li>
<li><strong>Bank alert:</strong> "URGENT: Your account has been compromised. Verify your identity now: [link]"</li>
<li><strong>Prize scam:</strong> "You have won £500! Claim your prize here: [link]"</li>
<li><strong>Government impersonation:</strong> "HMRC: You are owed a tax refund. Claim at: [link]"</li>
</ul>
<h4>Warning Signs of Smishing</h4>
<ul>
<li>Unexpected messages from unknown numbers</li>
<li>Shortened URLs (bit.ly, tinyurl) hiding the real destination</li>
<li>Requests for personal or financial information</li>
<li>Urgent language pressuring immediate action</li>
<li>Messages containing prizes or threats</li>
</ul>
<h4>How to Stay Safe</h4>
<ul>
<li>Never click links in unexpected SMS messages</li>
<li>Go directly to the official website if you want to check</li>
<li>Do not call phone numbers provided in suspicious texts</li>
<li>Report smishing attempts to your mobile provider (forward to 7726)</li>
<li>Enable spam filtering on your phone</li>
</ul>""",
        'duration_minutes': 12,
        'points': 12,
        'order': 1,
    },
    {
        'title': 'Social Engineering Tactics',
        'category_slug': 'social-engineering',
        'module_type': 'social_engineering',
        'difficulty': 'intermediate',
        'description': 'Understand the psychological manipulation techniques attackers use to bypass your defences.',
        'content': """<h4>What is Social Engineering?</h4>
<p>Social engineering is the art of manipulating people into revealing confidential information or taking actions that compromise security. It exploits human psychology rather than technical vulnerabilities.</p>
<h4>Core Psychological Triggers</h4>
<h5>1. Authority</h5>
<p>People tend to comply with requests from authority figures. Attackers impersonate CEOs, IT departments, police, or government agencies to gain trust and compliance.</p>
<h5>2. Urgency and Scarcity</h5>
<p>Creating time pressure removes the opportunity to think critically. "Act in the next 10 minutes or your account will be deleted" is designed to bypass rational decision-making.</p>
<h5>3. Fear</h5>
<p>Threats of consequences (account suspension, legal action, fines) trigger emotional responses that override logical thinking.</p>
<h5>4. Social Proof</h5>
<p>"Your colleagues have already verified their accounts" exploits the human tendency to follow what others are doing.</p>
<h5>5. Reciprocity</h5>
<p>Offering something (a free gift, useful information) creates a sense of obligation to give something in return.</p>
<h5>6. Familiarity and Liking</h5>
<p>Attackers research targets on social media to personalise attacks and build rapport before making their request.</p>
<h4>Spear Phishing vs Whaling</h4>
<p><strong>Spear phishing</strong> targets specific individuals with personalised messages. <strong>Whaling</strong> targets high-value targets such as executives (C-suite) for larger payoffs like wire transfers or sensitive data.</p>
<h4>Defence Strategies</h4>
<ul>
<li>Pause before acting on urgent requests — legitimate organisations allow time to verify</li>
<li>Verify the identity of anyone requesting sensitive actions through a separate channel</li>
<li>Follow established procedures even under pressure</li>
<li>Question requests that bypass normal processes</li>
</ul>""",
        'duration_minutes': 20,
        'points': 20,
        'order': 1,
    },
    {
        'title': 'Protecting Your Personal Information',
        'category_slug': 'information-protection',
        'module_type': 'general',
        'difficulty': 'beginner',
        'description': 'Practical steps to protect your passwords, financial data, and personal information online.',
        'content': """<h4>Your Digital Footprint</h4>
<p>Everything you share online — on social media, shopping sites, forums — can be used by attackers to personalise phishing attacks against you. Attackers research targets before striking.</p>
<h4>Password Security</h4>
<ul>
<li>Use a unique password for every account — reusing passwords means one breach exposes all your accounts</li>
<li>Use a password manager (Bitwarden, 1Password) to generate and store strong passwords</li>
<li>A strong password is long (12+ characters) and random — not based on personal information</li>
<li>Enable two-factor authentication (2FA) wherever possible</li>
</ul>
<h4>Two-Factor Authentication (2FA)</h4>
<p>2FA adds a second verification step beyond your password. Even if an attacker has your password, they cannot access your account without the second factor. Use an authenticator app (Google Authenticator, Authy) rather than SMS 2FA where possible.</p>
<h4>Recognising Fake Websites</h4>
<ul>
<li>Check the URL carefully — is it the exact official domain?</li>
<li>Look for HTTPS (padlock icon) — but note that phishing sites can also have HTTPS</li>
<li>Be suspicious if redirected from a link in an email or text</li>
<li>Bookmark official websites and use those bookmarks directly</li>
</ul>
<h4>What To Do If You've Been Phished</h4>
<ol>
<li>Change your password immediately on the affected account</li>
<li>Change passwords on any other accounts using the same password</li>
<li>Enable 2FA on the affected account</li>
<li>Contact your bank immediately if financial information was shared</li>
<li>Report the phishing attempt to the relevant organisation and authorities</li>
<li>Scan your device for malware if you downloaded anything</li>
</ol>""",
        'duration_minutes': 15,
        'points': 15,
        'order': 1,
    },
    {
        'title': 'Advanced Phishing Techniques',
        'category_slug': 'phishing-fundamentals',
        'module_type': 'general',
        'difficulty': 'advanced',
        'description': 'Explore sophisticated phishing methods including clone phishing, pharming, and AI-powered attacks.',
        'content': """<h4>Beyond Basic Phishing</h4>
<p>As awareness of basic phishing has grown, attackers have evolved more sophisticated techniques that are harder to detect.</p>
<h4>Clone Phishing</h4>
<p>Attackers take a legitimate email you previously received (e.g. a newsletter or notification), copy it exactly, replace the links with malicious ones, and resend it claiming to be a resend of the original. Because it looks identical to a real email you received, it is very convincing.</p>
<h4>Pharming</h4>
<p>Instead of tricking you into clicking a fake link, pharming attacks poison DNS servers or modify your hosts file so that when you type a real URL (e.g. your bank's website), you are silently redirected to a fake site — even if you typed the correct address.</p>
<h4>Business Email Compromise (BEC)</h4>
<p>Attackers compromise or spoof a business email account (often a CEO or finance director) and use it to instruct employees to transfer funds or share sensitive data. BEC attacks cost businesses billions annually.</p>
<h4>Adversary-in-the-Middle (AiTM) Phishing</h4>
<p>A proxy sits between you and the real website, relaying your login in real time. This allows attackers to steal session cookies even when 2FA is enabled, because the authentication has already occurred.</p>
<h4>AI-Powered Phishing</h4>
<p>Generative AI enables attackers to produce flawless, personalised phishing messages at scale in any language, eliminating the spelling and grammar errors that previously helped identify phishing.</p>
<h4>Defence Against Advanced Attacks</h4>
<ul>
<li>Use hardware security keys (FIDO2) for 2FA — they are resistant to AiTM attacks</li>
<li>Verify all wire transfer requests via phone using a known number</li>
<li>Use DNS-over-HTTPS to reduce pharming risk</li>
<li>Treat all unexpected communications with scepticism regardless of how convincing they appear</li>
</ul>""",
        'duration_minutes': 25,
        'points': 25,
        'order': 2,
    },
]

# ─── Assessment Questions ──────────────────────────────────────────────────────

PRE_ASSESSMENT_QUESTIONS = [
    {
        'text': 'What is phishing?',
        'type': 'multiple_choice',
        'answers': [
            ('A type of fishing sport', False),
            ('A cyber attack that tricks people into revealing sensitive information', True),
            ('A software virus that deletes files', False),
            ('A method of encrypting data', False),
        ],
        'explanation': 'Phishing is a cyber attack where criminals impersonate trusted entities to steal sensitive information such as passwords and credit card numbers.',
    },
    {
        'text': 'Which of the following is a warning sign of a phishing email?',
        'type': 'multiple_choice',
        'answers': [
            ('The email uses your full name in the greeting', False),
            ('The email is from a known company with a verified domain', False),
            ('The email creates urgency saying your account will be suspended', True),
            ('The email contains relevant information about your recent purchase', False),
        ],
        'explanation': 'Urgency and threats ("your account will be suspended") are classic social engineering tactics used in phishing to panic victims into acting without thinking.',
    },
    {
        'text': 'What does "smishing" refer to?',
        'type': 'multiple_choice',
        'answers': [
            ('Phishing attacks carried out via email', False),
            ('Phishing attacks carried out via SMS text messages', True),
            ('Phishing attacks carried out via phone calls', False),
            ('Phishing attacks carried out via social media', False),
        ],
        'explanation': 'Smishing = SMS + phishing. It refers to phishing attacks delivered through text messages.',
    },
    {
        'text': 'You receive an email from "paypal-secure.notifications.com" asking you to verify your account. What should you do?',
        'type': 'multiple_choice',
        'answers': [
            ('Click the link immediately to protect your account', False),
            ('Reply to the email asking if it is genuine', False),
            ('Do not click the link — go directly to paypal.com by typing it in your browser', True),
            ('Forward the email to your friends as a warning', False),
        ],
        'explanation': 'Always navigate to official websites by typing the URL directly into your browser rather than clicking links in emails. "paypal-secure.notifications.com" is not PayPal\'s domain.',
    },
    {
        'text': 'What is two-factor authentication (2FA)?',
        'type': 'multiple_choice',
        'answers': [
            ('Using two different passwords for the same account', False),
            ('A second verification step that adds security beyond just a password', True),
            ('Logging in from two different devices simultaneously', False),
            ('A type of firewall that blocks phishing websites', False),
        ],
        'explanation': '2FA requires a second form of verification (such as a code from an authenticator app) in addition to your password, making it much harder for attackers to access your account even if they have your password.',
    },
    {
        'text': 'Which URL is most likely to be a phishing website impersonating a bank?',
        'type': 'multiple_choice',
        'answers': [
            ('https://www.barclays.co.uk', False),
            ('https://barclays.co.uk.account-verify.com', True),
            ('https://online.barclays.co.uk', False),
            ('https://barclays.co.uk/login', False),
        ],
        'explanation': 'The domain "barclays.co.uk.account-verify.com" is actually the domain "account-verify.com" with "barclays.co.uk" as a subdomain — it is not affiliated with Barclays at all.',
    },
    {
        'text': 'What is spear phishing?',
        'type': 'multiple_choice',
        'answers': [
            ('Mass phishing emails sent to millions of random people', False),
            ('Phishing attacks targeting high-level executives only', False),
            ('Targeted phishing attacks personalised for specific individuals or organisations', True),
            ('Phishing attacks that use phone calls instead of emails', False),
        ],
        'explanation': 'Spear phishing is highly targeted. Attackers research their victims beforehand and craft personalised messages that are far more convincing than generic phishing emails.',
    },
    {
        'text': 'You accidentally clicked a phishing link and entered your password. What is the FIRST thing you should do?',
        'type': 'multiple_choice',
        'answers': [
            ('Wait and see if anything bad happens', False),
            ('Change the password on the affected account immediately', True),
            ('Delete your browser history', False),
            ('Restart your computer', False),
        ],
        'explanation': 'Changing your password immediately is the first priority to prevent the attacker from using the stolen credentials to access your account.',
    },
    {
        'text': 'True or False: A website with HTTPS (padlock icon) is always safe and cannot be a phishing site.',
        'type': 'true_false',
        'answers': [
            ('True', False),
            ('False', True),
        ],
        'explanation': 'False. HTTPS only means the connection between you and the website is encrypted — it does NOT verify that the website is legitimate. Phishing sites can and do use HTTPS.',
    },
    {
        'text': 'Which of the following best describes a "Business Email Compromise" (BEC) attack?',
        'type': 'multiple_choice',
        'answers': [
            ('Sending mass phishing emails to all employees of a company', False),
            ('Installing ransomware through a phishing email attachment', False),
            ('Impersonating a business executive via email to authorise fraudulent transfers', True),
            ('Creating a fake company website to collect credentials', False),
        ],
        'explanation': 'BEC attacks involve compromising or spoofing a business email account (often an executive) to trick employees into making wire transfers or sharing sensitive information.',
    },
]

POST_ASSESSMENT_QUESTIONS = [
    {
        'text': 'What psychological trigger does an attacker use when saying "Your account will be deleted in 1 hour"?',
        'type': 'multiple_choice',
        'answers': [
            ('Authority', False),
            ('Reciprocity', False),
            ('Urgency and Fear', True),
            ('Social Proof', False),
        ],
        'explanation': 'Creating urgency and fear is a core social engineering technique that bypasses rational thinking and pushes victims to act immediately without verifying the request.',
    },
    {
        'text': 'How can you verify a suspicious link in an email without clicking it?',
        'type': 'multiple_choice',
        'answers': [
            ('Open it in a private browsing window', False),
            ('Hover over the link to see the actual destination URL in the status bar', True),
            ('Copy and paste it into a new email', False),
            ('Forward the email to a friend to check', False),
        ],
        'explanation': 'Hovering over a link (without clicking) reveals the actual URL destination in the browser\'s status bar, allowing you to check whether it goes to a legitimate domain.',
    },
    {
        'text': 'Which type of 2FA is most resistant to phishing attacks?',
        'type': 'multiple_choice',
        'answers': [
            ('SMS one-time codes', False),
            ('Email verification codes', False),
            ('Hardware security keys (FIDO2)', True),
            ('Security questions', False),
        ],
        'explanation': 'Hardware security keys (FIDO2/WebAuthn) are bound to the legitimate domain and cannot be used on a phishing site, making them resistant to both phishing and adversary-in-the-middle attacks.',
    },
    {
        'text': 'What is "clone phishing"?',
        'type': 'multiple_choice',
        'answers': [
            ('Creating an exact copy of a legitimate website', False),
            ('Duplicating a real email previously received and replacing links with malicious ones', True),
            ('Using AI to clone a person\'s writing style in phishing emails', False),
            ('Sending the same phishing email multiple times', False),
        ],
        'explanation': 'Clone phishing involves copying a legitimate email you previously received, replacing the links with malicious ones, and resending it — often claiming to be a correction or resend of the original.',
    },
    {
        'text': 'A delivery company texts you: "Your parcel is on hold. Pay £2.99 to release it: bit.ly/xyz". What do you do?',
        'type': 'multiple_choice',
        'answers': [
            ('Pay the small amount — it is only £2.99', False),
            ('Click the link to check the tracking details', False),
            ('Do not click the link — check the delivery company\'s official website directly', True),
            ('Reply to the message asking for more details', False),
        ],
        'explanation': 'This is a classic smishing scam. The £2.99 fee is a lure and the link leads to a fake payment page that steals card details. Always check through official channels.',
    },
    {
        'text': 'True or False: Phishing attacks only target individuals, not organisations.',
        'type': 'true_false',
        'answers': [
            ('True', False),
            ('False', True),
        ],
        'explanation': 'False. Phishing attacks heavily target organisations. Business Email Compromise (BEC) and spear phishing campaigns specifically target companies, often costing millions in fraudulent transfers or data breaches.',
    },
    {
        'text': 'What is pharming?',
        'type': 'multiple_choice',
        'answers': [
            ('Sending phishing emails disguised as pharmacy orders', False),
            ('Redirecting users to fake websites even when they type the correct URL', True),
            ('Using farming-related themes in phishing emails', False),
            ('Collecting personal data through fake online surveys', False),
        ],
        'explanation': 'Pharming attacks corrupt DNS servers or local hosts files so that users are silently redirected to fake websites even when they type the correct address into their browser.',
    },
    {
        'text': 'An email appears to come from your CEO asking you to urgently transfer £10,000 to a supplier. What should you do?',
        'type': 'multiple_choice',
        'answers': [
            ('Transfer the money immediately as it is urgent', False),
            ('Reply to the email asking for confirmation', False),
            ('Call the CEO on a known phone number to verify the request independently', True),
            ('Transfer a smaller amount first to test', False),
        ],
        'explanation': 'Always verify financial requests through a completely separate channel (phone call to a known number). This is a BEC attack scenario. Replying to the email still communicates with the attacker.',
    },
    {
        'text': 'Which of the following is the safest practice for managing passwords?',
        'type': 'multiple_choice',
        'answers': [
            ('Use the same strong password for all accounts so you remember it', False),
            ('Write passwords in a notebook kept at your desk', False),
            ('Use a password manager to generate and store unique passwords for each account', True),
            ('Use your name and birth year as the base for all passwords', False),
        ],
        'explanation': 'A password manager generates unique, strong passwords for every account and stores them securely. This means a breach of one account does not compromise your other accounts.',
    },
    {
        'text': 'After completing phishing awareness training, what is the MOST important behaviour change?',
        'type': 'multiple_choice',
        'answers': [
            ('Never use email again', False),
            ('Report all suspicious messages and pause before acting on unexpected requests', True),
            ('Only open emails from people you personally know', False),
            ('Change all your passwords every day', False),
        ],
        'explanation': 'The most impactful change is developing a habit of pausing before acting on unexpected requests and reporting suspicious messages — this protects both you and your organisation.',
    },
]

# ─── Simulation Templates ─────────────────────────────────────────────────────

SIMULATION_TEMPLATES = [
    {
        'name': 'Fake Bank Security Alert',
        'template_type': 'email',
        'scenario': 'banking',
        'difficulty': 'easy',
        'sender_name': 'Barclays Security Team',
        'sender_email': 'security@barclays-secure-alerts.com',
        'subject': 'URGENT: Suspicious Activity Detected on Your Account',
        'content': """Dear Valued Customer,

We have detected unusual activity on your Barclays account and have temporarily limited access for your protection.

To restore full access, you must verify your identity within 24 hours by clicking the link below:

http://barclays.co.uk.account-verify-now.com/secure-login

Failure to verify will result in permanent account suspension.

Barclays Security Team
0800 400 100""",
        'indicators': ['Suspicious sender domain', 'Urgency and threat', 'Misleading URL structure'],
    },
    {
        'name': 'Parcel Delivery Fee Scam',
        'template_type': 'sms',
        'scenario': 'delivery',
        'difficulty': 'easy',
        'sender_number': '+44 7700 900123',
        'content': """Royal Mail: Your parcel (RQ847261GB) could not be delivered due to an unpaid customs fee of £2.99.

Reschedule delivery here: bit.ly/RM-parcel-fee

This link expires in 24hrs.""",
        'indicators': ['Unknown sender number', 'URL shortener', 'Urgency', 'Unexpected fee request'],
    },
    {
        'name': 'IT Department Password Reset',
        'template_type': 'email',
        'scenario': 'corporate',
        'difficulty': 'medium',
        'sender_name': 'IT Helpdesk',
        'sender_email': 'helpdesk@company-it-support.net',
        'subject': 'Action Required: Reset Your Password Before Friday',
        'content': """Hi,

Our IT team is conducting a mandatory security upgrade this weekend. All staff must reset their passwords before Friday 5pm.

Please use the link below to reset your password and avoid being locked out on Monday morning:

https://company-it-support.net/password-reset?user=employee

If you have any questions, reply to this email.

IT Helpdesk
Internal Extension: 5555""",
        'indicators': ['External domain not matching company', 'Deadline pressure', 'Credential harvesting link'],
    },
    {
        'name': 'Fake Prize Notification',
        'template_type': 'sms',
        'scenario': 'prize',
        'difficulty': 'easy',
        'sender_number': 'PRIZES UK',
        'content': """Congratulations! You have been selected to receive a £500 Amazon voucher.

To claim your prize visit: https://amazon-voucher-claim.co.uk/claim?id=UK500

Offer expires tonight at midnight. Only 3 prizes remaining!""",
        'indicators': ['Too-good-to-be-true offer', 'Fake urgency and scarcity', 'Non-Amazon domain', 'Unsolicited message'],
    },
    {
        'name': 'CEO Wire Transfer Request',
        'template_type': 'email',
        'scenario': 'corporate',
        'difficulty': 'hard',
        'sender_name': 'James Wilson (CEO)',
        'sender_email': 'j.wilson@company-corp.co',
        'subject': 'Confidential - Urgent Payment Required',
        'content': """Hi,

I'm currently in a board meeting and cannot talk by phone. I need you to process an urgent payment of £18,500 to a new supplier before close of business today.

This is time sensitive — please do not discuss this with anyone else as the deal is still confidential.

Transfer to:
Account Name: Global Supplies Ltd
Sort Code: 20-45-53
Account Number: 87654321

Send me confirmation once done. I'll explain everything after the meeting.

Thanks,
James Wilson
CEO""",
        'indicators': ['Spoofed sender email domain', 'Request for secrecy', 'No phone verification', 'Unusual urgency', 'Unknown payee'],
    },
    {
        'name': 'Social Media Account Verification',
        'template_type': 'email',
        'scenario': 'social_media',
        'difficulty': 'medium',
        'sender_name': 'Instagram Security',
        'sender_email': 'security@instagram-accounts-support.com',
        'subject': 'Your Instagram account has been flagged for review',
        'content': """Hi,

Your Instagram account has been reported for violating our Community Guidelines. We have temporarily restricted your account.

To appeal this decision and restore your account, please verify your identity within 48 hours:

Verify My Account → https://instagram-accounts-support.com/verify

If you do not verify within 48 hours, your account will be permanently deleted.

Instagram Security Team
© Meta Platforms Inc.""",
        'indicators': ['Non-official Instagram domain', 'Account deletion threat', 'Urgency deadline', 'Fake copyright footer'],
    },
]


class Command(BaseCommand):
    help = 'Seed modules, assessments, and simulation templates'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            self._clear_data()

        self._seed_modules()
        self._seed_assessments()
        self._seed_simulations()

        self.stdout.write(self.style.SUCCESS('\nAll platform data seeded successfully!'))

    def _clear_data(self):
        from education.models import Module
        from assessments.models import Quiz
        from simulations.models import PhishingTemplate

        Module.objects.all().delete()
        Quiz.objects.all().delete()
        PhishingTemplate.objects.all().delete()
        self.stdout.write('  Cleared existing modules, quizzes, and templates.')

    def _seed_modules(self):
        from education.models import Category, Module

        created = 0
        for data in MODULES:
            try:
                cat = Category.objects.get(slug=data['category_slug'])
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Category not found: {data["category_slug"]} — skipping module "{data["title"]}"'))
                continue

            slug = slugify(data['title'])
            base_slug = slug
            counter = 1
            while Module.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            Module.objects.create(
                title=data['title'],
                slug=slug,
                category=cat,
                module_type=data['module_type'],
                difficulty=data['difficulty'],
                description=data['description'],
                content=data['content'],
                duration_minutes=data['duration_minutes'],
                points=data['points'],
                order=data['order'],
                is_active=True,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'  Modules: created {created}'))

    def _seed_assessments(self):
        from assessments.models import Quiz, Question, Answer

        quizzes = [
            {
                'title': 'Phishing Awareness Pre-Assessment',
                'quiz_type': 'pre_assessment',
                'description': 'Test your current knowledge of phishing before starting the course.',
                'questions': PRE_ASSESSMENT_QUESTIONS,
            },
            {
                'title': 'Phishing Awareness Post-Assessment',
                'quiz_type': 'post_assessment',
                'description': 'Test what you have learned about phishing after completing the course.',
                'questions': POST_ASSESSMENT_QUESTIONS,
            },
        ]

        for qdata in quizzes:
            if Quiz.objects.filter(quiz_type=qdata['quiz_type']).exists():
                self.stdout.write(f'  Quiz already exists: {qdata["title"]} — skipping')
                continue

            quiz = Quiz.objects.create(
                title=qdata['title'],
                description=qdata['description'],
                quiz_type=qdata['quiz_type'],
                time_limit_minutes=20,
                passing_score=70.0,
                max_attempts=3,
                shuffle_questions=True,
                show_correct_answers=True,
                is_active=True,
            )

            for i, qinfo in enumerate(qdata['questions']):
                question = Question.objects.create(
                    quiz=quiz,
                    question_type=qinfo['type'],
                    text=qinfo['text'],
                    explanation=qinfo.get('explanation', ''),
                    points=1,
                    order=i + 1,
                )
                for j, (answer_text, is_correct) in enumerate(qinfo['answers']):
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=is_correct,
                        order=j,
                    )

            self.stdout.write(self.style.SUCCESS(f'  Created quiz: {quiz.title} ({len(qdata["questions"])} questions)'))

    def _seed_simulations(self):
        from simulations.models import PhishingTemplate

        created = 0
        for data in SIMULATION_TEMPLATES:
            if PhishingTemplate.objects.filter(name=data['name']).exists():
                continue

            PhishingTemplate.objects.create(
                name=data['name'],
                template_type=data['template_type'],
                scenario=data['scenario'],
                difficulty=data['difficulty'],
                sender_name=data.get('sender_name', ''),
                sender_email=data.get('sender_email', ''),
                subject=data.get('subject', ''),
                sender_number=data.get('sender_number', ''),
                content=data['content'],
                is_active=True,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'  Simulation templates: created {created}'))
