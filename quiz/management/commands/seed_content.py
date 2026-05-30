"""
Seed quiz categories, questions, badges, videos, and learning modules.
Usage:
    python manage.py seed_content
    python manage.py seed_content --clear   # wipe and re-seed
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify


CATEGORIES = [
    {
        'name': 'Phishing Fundamentals',
        'slug': 'phishing-fundamentals',
        'description': 'Learn the basics of phishing attacks, their history, and how they work.',
        'icon': 'BookOpenIcon',
        'color': 'blue',
        'sort_order': 1,
    },
    {
        'name': 'Email Phishing Detection',
        'slug': 'email-phishing',
        'description': 'Identify phishing emails and understand attacker techniques.',
        'icon': 'EnvelopeIcon',
        'color': 'red',
        'sort_order': 2,
    },
    {
        'name': 'SMS & Mobile Phishing',
        'slug': 'sms-mobile-phishing',
        'description': 'Protect yourself from smishing and mobile-based phishing attacks.',
        'icon': 'DevicePhoneMobileIcon',
        'color': 'green',
        'sort_order': 3,
    },
    {
        'name': 'Social Engineering Defense',
        'slug': 'social-engineering',
        'description': 'Understand psychological manipulation tactics used in phishing.',
        'icon': 'ShieldExclamationIcon',
        'color': 'orange',
        'sort_order': 4,
    },
    {
        'name': 'Information Protection',
        'slug': 'information-protection',
        'description': 'Learn how to safeguard your personal and financial information.',
        'icon': 'LockClosedIcon',
        'color': 'purple',
        'sort_order': 5,
    },
    {
        'name': 'Incident Reporting',
        'slug': 'incident-reporting',
        'description': 'Know what to do and who to contact when you encounter phishing.',
        'icon': 'FlagIcon',
        'color': 'teal',
        'sort_order': 6,
    },
]

QUESTIONS_BY_CATEGORY = {
    'phishing-fundamentals': [
        {
            'question': 'What is the primary goal of a phishing attack?',
            'options': ['To install antivirus software', 'To trick people into revealing sensitive information', 'To improve internet speed', 'To test website security'],
            'correct_answer': 1,
            'explanation': 'Phishing attacks are designed to deceive victims into revealing sensitive information such as passwords, credit card numbers, or personal data by impersonating trusted entities.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'Which of these is NOT a common type of phishing?',
            'options': ['Email phishing', 'Smishing (SMS phishing)', 'Fishing (catching fish)', 'Vishing (voice phishing)'],
            'correct_answer': 2,
            'explanation': 'Fishing with a rod is not related to cybersecurity. The main types of phishing include email phishing, smishing (SMS), vishing (voice calls), and spear phishing (targeted attacks).',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.15,
        },
        {
            'question': 'What does "vishing" mean in cybersecurity?',
            'options': ['Visual phishing through images', 'Voice phishing through phone calls', 'Virtual phishing through VR', 'Video phishing through streaming'],
            'correct_answer': 1,
            'explanation': 'Vishing (voice + phishing) involves attackers using phone calls to impersonate legitimate organisations and trick victims into sharing personal information or transferring money.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'What is "spear phishing"?',
            'options': ['A mass email campaign sent to millions', 'A targeted attack aimed at a specific individual or organisation', 'Phishing using fishing equipment as a prop', 'A type of malware that spreads via USB drives'],
            'correct_answer': 1,
            'explanation': 'Spear phishing is a highly targeted form of phishing where attackers research specific individuals or organisations to craft convincing, personalised messages.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.4,
        },
        {
            'question': 'What is "whaling" in the context of phishing?',
            'options': ['Phishing attacks targeting marine animals', 'Highly targeted phishing aimed at senior executives or high-value targets', 'Mass phishing campaigns sent to millions', 'A type of ransomware attack'],
            'correct_answer': 1,
            'explanation': 'Whaling targets high-value individuals (the "big fish") such as CEOs, CFOs, and other executives. These attacks are highly personalised and use sophisticated social engineering.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'Which psychological principle do phishing attackers most commonly exploit?',
            'options': ['Logic and rational thinking', 'Urgency and fear', 'Patience and reflection', 'Mathematical precision'],
            'correct_answer': 1,
            'explanation': 'Phishing attacks exploit urgency and fear by creating time pressure (e.g., "Your account will be closed in 24 hours!") to prevent victims from thinking critically or verifying the message.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'What is "pharming" and how does it differ from phishing?',
            'options': ['They are the same thing', 'Pharming redirects users to fake websites through DNS manipulation, without requiring the victim to click a malicious link', 'Pharming only targets farmers', 'Pharming uses physical mail instead of email'],
            'correct_answer': 1,
            'explanation': 'Pharming compromises DNS settings to automatically redirect users to fake websites even when they type the correct URL. It is more dangerous because the victim does not need to click a malicious link.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.65,
        },
        {
            'question': 'What does "smishing" stand for?',
            'options': ['Social media phishing', 'SMS phishing', 'Smart phishing', 'Software phishing'],
            'correct_answer': 1,
            'explanation': 'Smishing is phishing conducted through SMS (text messages). Attackers send fake messages pretending to be from banks, delivery companies, or government agencies.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What is a "clone phishing" attack?',
            'options': ['Creating duplicate websites that look identical to legitimate ones', 'Replicating a legitimate email that was previously delivered, replacing attachments or links with malicious ones', 'Cloning a user\'s identity completely', 'Making multiple copies of phishing emails'],
            'correct_answer': 1,
            'explanation': 'Clone phishing creates an almost identical copy of a legitimate, previously delivered email. The attacker replaces legitimate attachments or links with malicious ones and resends it, often claiming to be a resend.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.6,
        },
        {
            'question': 'How can you verify if a suspicious email from your bank is genuine?',
            'options': ['Click the link in the email to check', 'Reply to the email asking for confirmation', 'Call your bank using the official number on their website or your card', 'Forward the email to your friends to check'],
            'correct_answer': 2,
            'explanation': 'Always verify by contacting the organisation directly using contact details you already know (official website, back of your card). Never use contact information provided in a suspicious email.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What makes phishing attacks particularly dangerous in mobile banking contexts in Zambia?',
            'options': ['Mobile phones are less secure than computers', 'High mobile money usage (Airtel Money, MTN MoMo, Zamtel Kwacha) and limited cybersecurity awareness create ideal conditions for attackers', 'Zambian banks have weak security systems', 'Mobile data is cheaper than internet'],
            'correct_answer': 1,
            'explanation': 'The widespread adoption of mobile money services combined with limited cybersecurity education creates significant vulnerability. Attackers exploit the trust users place in mobile financial services.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'What is the "419 scam" and how is it related to phishing?',
            'options': ['A Nigerian law number', 'An advance-fee fraud (often via email) where victims are promised large sums of money in exchange for a small upfront payment', 'A type of computer virus', 'A Zambian mobile money code'],
            'correct_answer': 1,
            'explanation': 'The "419 scam" (named after Section 419 of Nigerian law) is an advance-fee fraud. It is a form of phishing that uses email to promise large rewards in exchange for upfront fees, which are then stolen.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.4,
        },
        {
            'question': 'Which of these best describes a "business email compromise" (BEC) attack?',
            'options': ['Hacking a business email server', 'Impersonating a business executive or vendor to manipulate employees into transferring funds or sensitive data', 'Sending bulk spam from business email accounts', 'Installing malware through business email attachments only'],
            'correct_answer': 1,
            'explanation': 'BEC attacks involve impersonating trusted business entities (executives, vendors, partners) to convince employees to make wire transfers, change payment details, or share sensitive information.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.65,
        },
        {
            'question': 'What is multi-factor authentication (MFA) and how does it help against phishing?',
            'options': ['Using multiple passwords', 'A security system requiring two or more verification methods, limiting attacker access even if credentials are stolen', 'Installing multiple antivirus programs', 'Checking emails on multiple devices'],
            'correct_answer': 1,
            'explanation': 'MFA requires something you know (password), something you have (phone/token), or something you are (biometric). Even if phishing steals your password, attackers still cannot access your account without the second factor.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'What is a "watering hole attack" in the context of phishing?',
            'options': ['Attacking water infrastructure', 'Compromising a website frequently visited by a target group to deliver malware when members visit', 'Flooding email servers with phishing messages', 'Targeting fishing communities with fake fishing gear ads'],
            'correct_answer': 1,
            'explanation': 'A watering hole attack compromises websites that the target group frequently visits. When victims visit the compromised site, malware is delivered. It exploits trust in familiar websites.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.7,
        },
        {
            'question': 'What percentage of cyber attacks are estimated to begin with phishing?',
            'options': ['Around 10%', 'Around 30%', 'Over 90%', 'Around 50%'],
            'correct_answer': 2,
            'explanation': 'Research consistently shows that over 90% of cyber attacks begin with a phishing email. This makes phishing awareness the single most important cybersecurity skill for individuals and organisations.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
    ],

    'email-phishing': [
        {
            'question': 'What should you look for in the sender\'s email address to identify a phishing email?',
            'options': ['The sender\'s name matches a company you know', 'The actual email domain differs from the legitimate company\'s domain (e.g., support@paypa1.com instead of support@paypal.com)', 'The email was sent during business hours', 'The email has a professional signature'],
            'correct_answer': 1,
            'explanation': 'Always check the actual email address, not just the display name. Phishers use lookalike domains (paypa1.com, arnazon.com) or completely different domains while displaying a legitimate company name.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'You receive an email from "support@zra-zambia.org" claiming your tax refund is ready. The legitimate ZRA website is zra.org.zm. What is suspicious?',
            'options': ['The email claims there is a tax refund', 'The domain "zra-zambia.org" does not match the legitimate ZRA domain "zra.org.zm"', 'The email is about taxes', 'Nothing is suspicious'],
            'correct_answer': 1,
            'explanation': 'Government and official domains in Zambia typically use .gov.zm or specific country domains. "zra-zambia.org" is a suspicious domain that attempts to mimic the legitimate ZRA but is almost certainly fraudulent.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'Which of these subject lines is MOST likely to be a phishing attempt?',
            'options': ['Monthly newsletter from your bank', 'URGENT: Your account has been compromised - Verify immediately or lose access!', 'Your statement for October 2024 is ready', 'Thank you for your recent transaction'],
            'correct_answer': 1,
            'explanation': 'Extreme urgency combined with threats ("lose access") is a hallmark of phishing. Legitimate organisations do not create panic through email subject lines. This is designed to bypass rational thinking.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What is an "email header" and why is it useful in detecting phishing?',
            'options': ['The visible subject line of an email', 'Technical metadata attached to every email showing routing information, originating servers, and authentication status - revealing if an email is spoofed', 'The company logo at the top of an email', 'The first paragraph of the email body'],
            'correct_answer': 1,
            'explanation': 'Email headers contain technical routing information including originating IP addresses and authentication results (SPF, DKIM, DMARC). IT professionals use headers to identify spoofed or malicious emails.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.65,
        },
        {
            'question': 'What is "domain spoofing" in phishing emails?',
            'options': ['Creating a fake email account with a free service', 'Forging the sender\'s email address to appear as if it comes from a trusted domain', 'Buying a domain name similar to a legitimate one', 'Spoofing only applies to websites, not emails'],
            'correct_answer': 1,
            'explanation': 'Domain spoofing manipulates the "From" header in an email to display a legitimate domain name while the actual sending address is different. This is combated by DMARC, SPF, and DKIM email authentication.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'You receive an email with a link. Before clicking, you hover over the link and see "http://www.secure-zanaco.malicious.ru/login". What is the most suspicious element?',
            'options': ['The use of "http" instead of "https"', 'The domain is "malicious.ru" (a Russian domain) - the "zanaco" part is just a subdomain to deceive you', 'The word "secure" in the URL', 'The word "login" at the end'],
            'correct_answer': 1,
            'explanation': 'In a URL, the actual domain is the part just before the first forward slash (e.g., "malicious.ru"). Everything before it (secure-zanaco) is a subdomain. Attackers add legitimate-sounding subdomains to deceive victims.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.55,
        },
        {
            'question': 'What does DMARC stand for and what does it help prevent?',
            'options': ['Digital Mail Access and Recovery Control', 'Domain-based Message Authentication, Reporting and Conformance - it prevents email spoofing by validating sender authenticity', 'Direct Mail Attack and Response Center', 'Data Management and Reporting Committee'],
            'correct_answer': 1,
            'explanation': 'DMARC is an email authentication protocol that helps prevent domain spoofing. When properly configured, it tells receiving email servers what to do with messages that fail authentication checks.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.7,
        },
        {
            'question': 'An email from "noreply@stanbic-bank-zambia.support" asks you to verify your account. What should you do?',
            'options': ['Click the verification link immediately', 'Check the actual Stanbic website (stanbic.com/zm) directly and contact them through official channels', 'Reply to the email to confirm your identity', 'Forward it to all your contacts to warn them'],
            'correct_answer': 1,
            'explanation': 'The domain "stanbic-bank-zambia.support" is not the legitimate Stanbic domain. Never click links in suspicious emails. Always navigate directly to the official website and use official contact numbers.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'What is a "malicious attachment" in phishing emails and what file types are commonly used?',
            'options': ['Any large file over 10MB', 'Files designed to execute malware when opened, commonly .exe, .doc/.docx with macros, .pdf, .zip, and .js files', 'Only .exe files contain viruses', 'PDF files cannot be malicious'],
            'correct_answer': 1,
            'explanation': 'Malicious attachments execute malware when opened. Common types include: Office documents with macros enabled, PDFs with embedded scripts, ZIP files containing executables, and JavaScript files. Never open unexpected attachments.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'What should you do if you accidentally clicked a link in a phishing email?',
            'options': ['Nothing — just close the browser tab', 'Immediately disconnect from internet, run antivirus scan, change passwords on any accounts accessed, and report to IT/bank', 'Click the unsubscribe button in the email', 'Wait to see if anything bad happens'],
            'correct_answer': 1,
            'explanation': 'Immediate action is critical: disconnect to stop potential data exfiltration, scan for malware, change passwords (especially banking), enable MFA, and notify relevant parties including your IT department or bank.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.3,
        },
        {
            'question': 'What is "typosquatting" and how is it used in phishing?',
            'options': ['Squatting on physical property using typos in legal documents', 'Registering domain names with common misspellings of legitimate sites (e.g., gooogle.com, amazn.com) to capture mistyped URLs', 'A technique to slow down typing speed', 'Creating fake keyboard layouts'],
            'correct_answer': 1,
            'explanation': 'Typosquatting registers domains with common misspellings or character substitutions of legitimate websites. When users accidentally mistype a URL, they land on a phishing site designed to look like the real one.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'What is "email harvesting" and why should you be cautious about where you post your email address?',
            'options': ['Collecting agricultural data via email', 'Automatically collecting email addresses from websites, forums, and public sources to build lists for phishing campaigns', 'Harvesting spam from your inbox', 'A technique to organise email folders'],
            'correct_answer': 1,
            'explanation': 'Email harvesting bots scan websites, social media, and public forums to collect email addresses. The more visible your email, the more likely it is to end up on phishing lists. Use contact forms instead of displaying emails publicly.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
    ],

    'sms-mobile-phishing': [
        {
            'question': 'You receive an SMS: "Your MTN MoMo account has been limited. Click bit.ly/mtn-verify to restore access immediately." What should you do?',
            'options': ['Click the link to restore access', 'Do NOT click the link; contact MTN directly using their official number (100 for MTN Zambia)', 'Forward the SMS to MTN customer care', 'Reply STOP to the message'],
            'correct_answer': 1,
            'explanation': 'This is a classic smishing (SMS phishing) attack. Shortened URLs (bit.ly) hide the real destination. Always contact MTN directly using the official number on their website, never through links in SMS messages.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What makes shortened URLs in SMS messages dangerous?',
            'options': ['They are always malicious', 'They hide the true destination — you cannot tell where you will be taken until you click, making it impossible to verify legitimacy beforehand', 'They expire after 24 hours', 'They use more mobile data'],
            'correct_answer': 1,
            'explanation': 'URL shorteners (bit.ly, tinyurl, etc.) mask the real URL. You have no way to know if the destination is legitimate or malicious without clicking. Use URL expansion tools like checkshorturl.com to preview the destination.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'You receive an SMS claiming to be from the Zambia Revenue Authority (ZRA) saying you have a tax refund. It asks you to provide your NRC number and bank details via a link. What is this?',
            'options': ['A legitimate government service', 'A smishing attack — ZRA does not request personal details via SMS links and does not initiate refunds this way', 'An automated banking service', 'A mobile money verification process'],
            'correct_answer': 1,
            'explanation': 'Government agencies like ZRA never request personal details (NRC, bank info) through SMS links. This is a smishing attack designed to steal your identity and financial information. Report to ZRA and ZM-CIRT.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'What is "SIM swapping" and how is it used in conjunction with phishing?',
            'options': ['Physically swapping SIM cards between phones', 'Convincing a mobile operator to transfer a victim\'s phone number to an attacker-controlled SIM, allowing them to intercept OTPs and bypass MFA', 'Using multiple SIM cards for better signal', 'A promotional offer from mobile companies'],
            'correct_answer': 1,
            'explanation': 'SIM swapping (also called SIM hijacking) is when attackers impersonate victims to mobile operators to transfer the phone number. This allows them to receive OTPs and bypass 2FA, giving access to banking and email accounts.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.7,
        },
        {
            'question': 'You receive an SMS: "Congratulations! You have won K10,000 in the Zamtel Lucky Draw. Reply with your full name, NRC and Kwacha account number to claim." What should you do?',
            'options': ['Reply with your details immediately to claim the prize', 'Delete the message — this is a scam. Legitimate prize draws never request sensitive personal data via SMS', 'Forward it to your family so they can enter too', 'Call the number provided to verify'],
            'correct_answer': 1,
            'explanation': 'This is a prize scam (a form of smishing). Legitimate prize draws: (1) you must enter first, (2) never ask for NRC via SMS, (3) never ask for bank details via text. This is designed to steal your identity and money.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.15,
        },
        {
            'question': 'What is "one-time password (OTP) phishing" and why is it increasingly common in Zambia?',
            'options': ['Stealing physical passwords written on paper', 'Tricking victims into sharing OTPs (sent for mobile money or banking authentication) through fake urgency or fake support calls, giving attackers access to accounts', 'A password that can only be used on one device', 'Sharing passwords with family members'],
            'correct_answer': 1,
            'explanation': 'OTP phishing is critical in Zambia due to mobile money adoption. Attackers pose as bank/MNO support, create fake urgency ("Your account is being hacked, share your OTP to stop it"), then use the OTP to access and drain accounts.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'How can you verify if an SMS claiming to be from your bank is legitimate?',
            'options': ['Check if it mentions your account balance', 'Call the bank\'s official number (on your card or their website), NOT any number in the SMS, to verify the message', 'Check if the grammar is correct', 'See if your friends received the same SMS'],
            'correct_answer': 1,
            'explanation': 'Always verify by calling your bank\'s official number (printed on your debit/credit card or official website). Never call numbers provided in the suspicious SMS. Banks have dedicated fraud lines for exactly this purpose.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What is a "smishing kit" and why do they make SMS phishing more dangerous?',
            'options': ['A physical kit for testing SMS signals', 'Pre-built tools available on dark web marketplaces that make it easy for attackers with minimal technical skills to launch professional-looking SMS phishing campaigns', 'A customer service kit for mobile companies', 'A legitimate SMS marketing tool'],
            'correct_answer': 1,
            'explanation': 'Smishing kits have lowered the technical barrier for SMS phishing. These ready-made packages include fake website templates, SMS sending infrastructure, and victim data collection. Anyone can now launch convincing campaigns.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.65,
        },
        {
            'question': 'What should you do if you receive a suspicious SMS while your phone is on a public Wi-Fi network?',
            'options': ['Click any links in the SMS immediately', 'Disconnect from public Wi-Fi before investigating — public networks are often monitored by attackers', 'Reply to the SMS to unsubscribe', 'Nothing special — public Wi-Fi is safe'],
            'correct_answer': 1,
            'explanation': 'Public Wi-Fi networks can be monitored by attackers using man-in-the-middle attacks. If you are on public Wi-Fi and receive suspicious messages, disconnect first. Avoid accessing sensitive accounts on public Wi-Fi altogether.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
    ],

    'social-engineering': [
        {
            'question': 'What is "pretexting" in social engineering?',
            'options': ['Sending text messages before the main attack', 'Creating a fabricated scenario (pretext) to manipulate victims into revealing information or taking actions they otherwise would not', 'Pre-screening text messages for viruses', 'A legal term for fraudulent contracts'],
            'correct_answer': 1,
            'explanation': 'Pretexting involves creating a believable false scenario. Examples: pretending to be IT support needing your password, an auditor requiring financial records, or a new employee needing system access.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'Which of these is an example of "baiting" in social engineering?',
            'options': ['Sending threatening emails', 'Leaving a USB drive labelled "Salary Information 2024" in a public place hoping someone will plug it in and unknowingly install malware', 'Posting fishing content online', 'Offering free food to get people to fill out a form'],
            'correct_answer': 1,
            'explanation': 'Baiting exploits human curiosity or greed. A USB drive labelled with something enticing is a classic bait. When plugged in, it automatically installs malware. Never plug in unknown USB drives.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'What is "quid pro quo" as a social engineering technique?',
            'options': ['A legal Latin phrase with no cyber relevance', 'Offering something valuable (like free IT support) in exchange for information or access, then using that access maliciously', 'A type of malware', 'A legitimate business practice'],
            'correct_answer': 1,
            'explanation': '"Quid pro quo" (something for something) in social engineering involves offering a service or benefit in exchange for information. Example: "I\'m from IT — I can fix your computer if you give me your login credentials."',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'What is "tailgating" or "piggybacking" in physical security?',
            'options': ['Following someone\'s car too closely', 'Gaining physical access to a restricted area by following an authorised person through a secure door without authentication', 'Mounting a pig on your back', 'A type of shoulder surfing attack'],
            'correct_answer': 1,
            'explanation': 'Tailgating involves physically following an authorised person through a secure door before it closes. It bypasses electronic access controls. Employees should never hold doors open for people they do not know.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.3,
        },
        {
            'question': 'A caller claims to be from your company\'s IT department and says your account was compromised. They ask for your password to "secure your account". What should you do?',
            'options': ['Provide the password quickly to secure your account', 'Refuse — IT departments never need your password. Call the IT helpdesk back using the official internal number to verify', 'Ask them to send a confirmation email first', 'Give them only part of your password'],
            'correct_answer': 1,
            'explanation': 'Legitimate IT departments never need your password. They have administrative access to reset accounts without it. This is a classic vishing/social engineering attack. Always verify by calling back on a known number.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What is the principle of "authority" in social engineering and how is it exploited?',
            'options': ['Hackers need government authority to attack', 'Attackers impersonate authority figures (managers, police, tax authorities, IT managers) because people are psychologically conditioned to obey authority', 'Authority figures cannot be phished', 'Only employees in positions of authority are targeted'],
            'correct_answer': 1,
            'explanation': 'The authority principle exploits our tendency to comply with requests from perceived authority figures. Attackers impersonate CEOs, government officials, police, or IT managers to make requests seem mandatory and bypass critical thinking.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'What is "shoulder surfing" and in what contexts is it most dangerous?',
            'options': ['Surfing the internet while sitting on someone\'s shoulders', 'Observing someone\'s screen or keyboard to steal PINs, passwords, or sensitive information, most dangerous at ATMs, on public transport, and in coffee shops', 'A type of email phishing', 'Network surveillance from a remote location'],
            'correct_answer': 1,
            'explanation': 'Shoulder surfing is observing someone enter sensitive information. High-risk locations: ATMs (stealing PINs), public transport (viewing work emails), coffee shops (capturing login credentials). Always use privacy screens and shield keypads.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'What does "social proof" mean in social engineering attacks?',
            'options': ['Providing proof of your social media accounts', 'Exploiting the tendency to follow others\' actions — fake claims like "1,000 people already updated their details" to make the attack seem normal and safe', 'A legal document proving social status', 'Proof that a social network is legitimate'],
            'correct_answer': 1,
            'explanation': 'Social proof exploits our tendency to look to others\' actions when unsure. In phishing: "Other users have already confirmed their details." This makes the deception seem routine and normalises compliance.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
    ],

    'information-protection': [
        {
            'question': 'What is a strong password? Which of these examples is strongest?',
            'options': ['Password123', 'P@ssw0rd', 'K9#mPq!2$Xv&3nL', 'MyBirthday1990'],
            'correct_answer': 2,
            'explanation': 'Strong passwords combine: length (12+ characters), uppercase, lowercase, numbers, and special characters, and avoid dictionary words or personal information. "K9#mPq!2$Xv&3nL" meets all criteria.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What is "credential stuffing" and why is using unique passwords for each account important?',
            'options': ['Filling forms with random credentials', 'Attackers using stolen username/password combinations from one breach to automatically try logging into other services — unique passwords prevent this', 'Storing all passwords in one document', 'A technique for remembering multiple passwords'],
            'correct_answer': 1,
            'explanation': 'Credential stuffing uses leaked credentials from one breach to attack other services. If you reuse passwords and one site is breached, all your accounts become vulnerable. A password manager helps maintain unique passwords.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'What personal information should you NEVER share in response to an unsolicited contact?',
            'options': ['Your favourite colour', 'NRC number, bank account details, PINs, OTPs, passwords, or full date of birth in response to any unsolicited call, email, or SMS', 'Your hometown', 'Your first name'],
            'correct_answer': 1,
            'explanation': 'In Zambia, your NRC number is a critical identifier used for banking and government services. Combined with other personal details, it enables identity theft. Legitimate services initiate contact through known channels, not unsolicited messages.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'What is a "data breach" and how does it increase your phishing risk?',
            'options': ['A physical break-in at a data centre', 'Unauthorised access and exposure of personal data, which provides attackers with accurate personal details to craft convincing targeted phishing attacks', 'A break in your internet connection', 'Losing your phone containing personal data'],
            'correct_answer': 1,
            'explanation': 'Data breaches expose your email, name, phone number, and sometimes passwords. Attackers use this information to create highly personalised phishing attacks (spear phishing) that reference your real details to seem legitimate.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'What is a "password manager" and why is it recommended for security?',
            'options': ['A person who manages your passwords for you', 'Encrypted software that generates, stores, and autofills strong unique passwords for each site — eliminating the need to remember them', 'Writing passwords in a secure notebook', 'A browser feature that saves passwords'],
            'correct_answer': 1,
            'explanation': 'Password managers generate and store unique, complex passwords for every site. You only need to remember one master password. They also autofill forms, making them faster than typing and immune to keyloggers on trusted devices.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.4,
        },
        {
            'question': 'What does HTTPS in a web address indicate and does it guarantee a site is safe?',
            'options': ['The site is completely safe and cannot be phishing', 'HTTPS means the connection is encrypted, but it does NOT mean the site itself is legitimate — phishing sites frequently use HTTPS', 'The site belongs to a government', 'The site has been verified by Google'],
            'correct_answer': 1,
            'explanation': 'HTTPS encrypts data in transit but only means data between your browser and the server is encrypted — not that the site itself is trustworthy. Phishing sites routinely obtain SSL certificates to display the padlock icon. Always verify the domain.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.55,
        },
        {
            'question': 'What is "two-factor authentication" (2FA) and which type is most secure?',
            'options': ['Using two different passwords', 'An additional verification step after password login; hardware security keys (FIDO2/WebAuthn) are most secure, followed by authenticator apps, then SMS codes', 'Logging in from two devices simultaneously', 'Two-step email verification'],
            'correct_answer': 1,
            'explanation': 'MFA adds a second verification layer. Security hierarchy (most to least secure): hardware keys > authenticator apps (Google Authenticator, Authy) > SMS codes. SMS can be intercepted via SIM swapping, while hardware keys resist phishing completely.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.6,
        },
        {
            'question': 'What should you do with old bank statements, utility bills, and documents containing personal information?',
            'options': ['Throw them in the recycling bin', 'Shred them using a cross-cut shredder before disposal — physical documents can be used for identity theft via "dumpster diving"', 'Keep them indefinitely', 'Burn them'],
            'correct_answer': 1,
            'explanation': 'Physical documents with personal/financial information should be shredded. "Dumpster diving" (searching through discarded materials) is a real technique used for identity theft and social engineering. Cross-cut shredding makes reconstruction impossible.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
    ],

    'incident-reporting': [
        {
            'question': 'What is ZM-CIRT and what is its role in Zambia\'s cybersecurity?',
            'options': ['A private cybersecurity company in Zambia', 'Zambia\'s Computer Incident Response Team — the national body responsible for coordinating responses to cybersecurity incidents and receiving phishing reports', 'A mobile network operator', 'A law enforcement unit'],
            'correct_answer': 1,
            'explanation': 'ZM-CIRT (Zambia Computer Incident Response Team) operates under ZICTA and is responsible for monitoring cyber threats, coordinating incident responses, and providing cybersecurity advice. Report incidents to incident@zm-cirt.zm.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'What should you do FIRST if you believe you have fallen victim to a phishing attack?',
            'options': ['Post about it on social media', 'Immediately change all passwords (starting with email and banking), contact your bank to freeze accounts if financial data was compromised, and document everything', 'Wait 24 hours to see if anything happens', 'Delete all your emails'],
            'correct_answer': 1,
            'explanation': 'Speed is critical. First: change passwords (email first, as it can reset others). If financial data was shared, call your bank immediately to freeze accounts. Document everything (screenshots, timestamps) for reporting.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.2,
        },
        {
            'question': 'To whom should you report a phishing email that impersonates Zanaco Bank in Zambia?',
            'options': ['Only to the police', 'To Zanaco\'s fraud department directly, and also to ZICTA/ZM-CIRT (incident@zm-cirt.zm)', 'To Google or Microsoft only', 'To your friends on WhatsApp'],
            'correct_answer': 1,
            'explanation': 'Report to multiple channels: (1) The impersonated organisation\'s fraud department, (2) ZM-CIRT for national tracking, (3) ZICTA if the phishing constitutes a cybercrime under the Zambia Cyber Security and Cyber Crimes Act.',
            'difficulty': 'beginner',
            'difficulty_parameter': 0.25,
        },
        {
            'question': 'What evidence should you preserve when reporting a phishing incident?',
            'options': ['Delete all evidence to protect your privacy', 'Preserve the original email (with headers), screenshots of suspicious websites, SMS messages, transaction records, and communication logs — do not delete originals', 'Only keep financial transaction records', 'You do not need evidence to report'],
            'correct_answer': 1,
            'explanation': 'Evidence preservation is critical for investigation and prosecution. Keep: original emails (do not forward — forward loses headers), screenshots with timestamps, SMS screenshots, bank statements. This evidence is essential for authorities.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.4,
        },
        {
            'question': 'Under which Zambian law can phishing attackers be prosecuted?',
            'options': ['The Banking and Financial Services Act', 'The Cyber Security and Cyber Crimes Act No. 2 of 2021, which criminalises phishing and related computer fraud offences', 'The Electronic Communications Act only', 'There is no law against phishing in Zambia'],
            'correct_answer': 1,
            'explanation': 'Zambia\'s Cyber Security and Cyber Crimes Act No. 2 of 2021 specifically addresses cybercrime including phishing, computer fraud, and identity theft. Offenders face significant prison sentences and fines.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'What is the role of ZICTA in cybersecurity in Zambia?',
            'options': ['ZICTA is a mobile network operator', 'Zambia Information and Communications Technology Authority — the regulatory body that oversees ICT including cybersecurity regulations and enforcement', 'ZICTA provides free internet access', 'ZICTA is only responsible for radio broadcasting'],
            'correct_answer': 1,
            'explanation': 'ZICTA is Zambia\'s ICT regulator, responsible for cybersecurity oversight, internet governance, and enforcement of cybercrime laws. They work with ZM-CIRT on national cybersecurity incidents.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
        {
            'question': 'How should you safely forward a suspicious email to report it without infecting others?',
            'options': ['Forward it normally with "FWD:" in the subject line', 'Forward as an attachment (not inline) so the malicious links/code are contained, or use email reporting buttons if available', 'Copy and paste the text into a new email', 'Print and scan it then send the image'],
            'correct_answer': 1,
            'explanation': 'Forwarding as an attachment preserves the original headers for analysis and prevents accidentally clicking links. Many email clients and anti-phishing services (like reportphishing@apwg.org) prefer attachments for forensic analysis.',
            'difficulty': 'advanced',
            'difficulty_parameter': 0.6,
        },
        {
            'question': 'What is the APWG and how can Zambians use it to fight phishing?',
            'options': ['A Zambian government agency', 'Anti-Phishing Working Group — an international coalition where anyone can report phishing by forwarding emails to reportphishing@apwg.org', 'A private security firm', 'A social media reporting platform'],
            'correct_answer': 1,
            'explanation': 'APWG is a global coalition of industry, government, and law enforcement fighting phishing. Anyone worldwide can forward phishing emails to reportphishing@apwg.org. This contributes to global threat intelligence that helps shut down phishing sites.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.5,
        },
        {
            'question': 'What should an organisation do AFTER recovering from a phishing incident?',
            'options': ['Keep it secret to avoid reputational damage', 'Conduct a post-incident review, update security measures, provide additional training, notify affected parties as legally required, and share lessons learned without blame', 'Blame and discipline the employee who fell for it', 'Only change the victim\'s password'],
            'correct_answer': 1,
            'explanation': 'Post-incident activities are crucial for improvement: review what happened (without blame), update controls, provide targeted training, notify affected individuals, comply with legal reporting requirements, and document lessons to prevent recurrence.',
            'difficulty': 'intermediate',
            'difficulty_parameter': 0.45,
        },
    ],
}

BADGES = [
    {
        'name': 'First Steps',
        'description': 'Completed your first lesson on the platform.',
        'icon': 'AcademicCapIcon',
        'requirement': 'Complete 1 lesson',
        'category': 'learning',
        'criteria': {'type': 'lessons_completed', 'count': 1},
        'sort_order': 1,
    },
    {
        'name': 'Eager Learner',
        'description': 'Completed 5 lessons across the platform.',
        'icon': 'BookOpenIcon',
        'requirement': 'Complete 5 lessons',
        'category': 'learning',
        'criteria': {'type': 'lessons_completed', 'count': 5},
        'sort_order': 2,
    },
    {
        'name': 'Knowledge Seeker',
        'description': 'Completed 10 lessons across the platform.',
        'icon': 'StarIcon',
        'requirement': 'Complete 10 lessons',
        'category': 'learning',
        'criteria': {'type': 'lessons_completed', 'count': 10},
        'sort_order': 3,
    },
    {
        'name': 'Quiz Starter',
        'description': 'Completed your first quiz.',
        'icon': 'CheckCircleIcon',
        'requirement': 'Complete 1 quiz',
        'category': 'quiz',
        'criteria': {'type': 'quiz_attempts', 'count': 1},
        'sort_order': 4,
    },
    {
        'name': 'Quiz Champion',
        'description': 'Completed 5 quizzes.',
        'icon': 'TrophyIcon',
        'requirement': 'Complete 5 quizzes',
        'category': 'quiz',
        'criteria': {'type': 'quiz_attempts', 'count': 5},
        'sort_order': 5,
    },
    {
        'name': 'Email Detective',
        'description': 'Scored 80% or higher on an Email Phishing Detection quiz.',
        'icon': 'EnvelopeIcon',
        'requirement': 'Score 80%+ on Email Phishing quiz',
        'category': 'mastery',
        'criteria': {'type': 'quiz_score', 'category_slug': 'email-phishing', 'min_score': 80},
        'sort_order': 6,
    },
    {
        'name': 'SMS Shield',
        'description': 'Scored 80% or higher on the SMS & Mobile Phishing quiz.',
        'icon': 'DevicePhoneMobileIcon',
        'requirement': 'Score 80%+ on SMS Phishing quiz',
        'category': 'mastery',
        'criteria': {'type': 'quiz_score', 'category_slug': 'sms-mobile-phishing', 'min_score': 80},
        'sort_order': 7,
    },
    {
        'name': 'Social Defender',
        'description': 'Scored 80% or higher on the Social Engineering Defense quiz.',
        'icon': 'ShieldCheckIcon',
        'requirement': 'Score 80%+ on Social Engineering quiz',
        'category': 'mastery',
        'criteria': {'type': 'quiz_score', 'category_slug': 'social-engineering', 'min_score': 80},
        'sort_order': 8,
    },
    {
        'name': 'Perfect Score',
        'description': 'Achieved 100% on any quiz.',
        'icon': 'SparklesIcon',
        'requirement': 'Score 100% on any quiz',
        'category': 'mastery',
        'criteria': {'type': 'perfect_score'},
        'sort_order': 9,
    },
    {
        'name': 'Video Learner',
        'description': 'Watched all available educational videos.',
        'icon': 'PlayCircleIcon',
        'requirement': 'Watch all published videos',
        'category': 'engagement',
        'criteria': {'type': 'all_videos_watched'},
        'sort_order': 10,
    },
    {
        'name': 'Platform Master',
        'description': 'Completed 10+ lessons and maintained a 70%+ quiz average.',
        'icon': 'CrownIcon',
        'requirement': 'Complete 10 lessons and 70%+ quiz average',
        'category': 'mastery',
        'criteria': {'type': 'platform_complete'},
        'sort_order': 11,
    },
    {
        'name': 'High Achiever',
        'description': 'Maintained an average quiz score of 85% or above.',
        'icon': 'ChartBarIcon',
        'requirement': 'Maintain 85%+ average across all quizzes',
        'category': 'quiz',
        'criteria': {'type': 'all_quizzes_avg', 'min_avg': 85},
        'sort_order': 12,
    },
]

VIDEOS = [
    {
        'category_slug': 'phishing-fundamentals',
        'title': 'Introduction to Phishing Attacks',
        'url': 'https://www.youtube.com/watch?v=Y3r2DFz9sMo',
        'duration': '8:32',
        'description': 'A comprehensive introduction to phishing — what it is, how it works, and why it is so effective.',
    },
    {
        'category_slug': 'phishing-fundamentals',
        'title': 'The Psychology Behind Phishing',
        'url': 'https://www.youtube.com/watch?v=aQxPxQ_Ber4',
        'duration': '12:15',
        'description': 'Understand the psychological manipulation techniques used by phishing attackers.',
    },
    {
        'category_slug': 'email-phishing',
        'title': 'How to Spot a Phishing Email',
        'url': 'https://www.youtube.com/watch?v=XBkzBrXlle0',
        'duration': '6:47',
        'description': 'Practical guide on identifying red flags in phishing emails — subject lines, sender addresses, links, and attachments.',
    },
    {
        'category_slug': 'sms-mobile-phishing',
        'title': 'Smishing: SMS Phishing Explained',
        'url': 'https://www.youtube.com/watch?v=5i5JIamGz5E',
        'duration': '7:20',
        'description': 'How SMS phishing works and how to protect your mobile money accounts.',
    },
    {
        'category_slug': 'social-engineering',
        'title': 'Social Engineering Tactics',
        'url': 'https://www.youtube.com/watch?v=lc7scxvKQOo',
        'duration': '15:33',
        'description': 'Deep dive into social engineering — pretexting, baiting, and psychological manipulation tactics.',
    },
    {
        'category_slug': 'information-protection',
        'title': 'Password Security Best Practices',
        'url': 'https://www.youtube.com/watch?v=aEmXKYVmECk',
        'duration': '9:11',
        'description': 'How to create and manage strong passwords and enable two-factor authentication.',
    },
    {
        'category_slug': 'incident-reporting',
        'title': 'What To Do After a Phishing Attack',
        'url': 'https://www.youtube.com/watch?v=3lEPiDJRIH8',
        'duration': '11:05',
        'description': 'Step-by-step guide on how to respond when you have fallen for a phishing attack.',
    },
]


class Command(BaseCommand):
    help = 'Seed quiz categories, questions, badges, videos, and ML training data'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing quiz data before seeding')
        parser.add_argument('--skip-ml', action='store_true', help='Skip ML model training step')

    def handle(self, *args, **options):
        if options['clear']:
            self._clear_data()

        self._seed_categories()
        self._seed_questions()
        self._seed_badges()
        self._seed_videos()

        if not options['skip_ml']:
            self._train_ml_models()

        self.stdout.write(self.style.SUCCESS('\nSeeding complete! Platform is ready.'))

    def _clear_data(self):
        from quiz.models import AdaptiveQuizAnswer, AdaptiveQuizAttempt, UserKnowledgeProfile, AdaptiveQuestion
        from badges.models import UserBadge, Badge
        from education.models import Video
        self.stdout.write('Clearing existing data...')
        AdaptiveQuizAnswer.objects.all().delete()
        AdaptiveQuizAttempt.objects.all().delete()
        UserKnowledgeProfile.objects.all().delete()
        AdaptiveQuestion.objects.all().delete()
        UserBadge.objects.all().delete()
        Badge.objects.all().delete()
        Video.objects.all().delete()

    def _seed_categories(self):
        from education.models import Category
        self.stdout.write('Seeding categories...')
        for data in CATEGORIES:
            cat, created = Category.objects.update_or_create(
                slug=data['slug'],
                defaults=data,
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status}: {cat.name}')

    def _seed_questions(self):
        from education.models import Category
        from quiz.models import AdaptiveQuestion
        self.stdout.write('Seeding questions...')
        total = 0
        for cat_slug, questions in QUESTIONS_BY_CATEGORY.items():
            try:
                cat = Category.objects.get(slug=cat_slug)
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Category not found: {cat_slug}'))
                continue

            for q in questions:
                AdaptiveQuestion.objects.update_or_create(
                    category=cat,
                    question=q['question'],
                    defaults={
                        'options': q['options'],
                        'correct_answer': q['correct_answer'],
                        'explanation': q['explanation'],
                        'difficulty': q['difficulty'],
                        'difficulty_parameter': q.get('difficulty_parameter', 0.5),
                        'discrimination_index': q.get('discrimination_index', 1.0),
                        'is_active': True,
                    }
                )
                total += 1

        self.stdout.write(f'  Seeded {total} questions across {len(QUESTIONS_BY_CATEGORY)} categories')

    def _seed_badges(self):
        from badges.models import Badge
        self.stdout.write('Seeding badges...')
        for data in BADGES:
            badge, created = Badge.objects.update_or_create(
                name=data['name'],
                defaults=data,
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status}: {badge.name}')

    def _seed_videos(self):
        from education.models import Category, Video
        self.stdout.write('Seeding videos...')
        for data in VIDEOS:
            cat_slug = data.pop('category_slug')
            try:
                cat = Category.objects.get(slug=cat_slug)
                Video.objects.update_or_create(
                    category=cat,
                    title=data['title'],
                    defaults={**data, 'category': cat},
                )
                self.stdout.write(f'  Created/Updated: {data["title"]}')
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Category not found: {cat_slug}'))
            data['category_slug'] = cat_slug  # restore for next potential run

    def _train_ml_models(self):
        self.stdout.write('Training ML models...')
        try:
            from ml_engine.models.difficulty_predictor import DifficultyPredictor
            from ml_engine.data.seed_data import SEED_TRAINING_DATA
            predictor = DifficultyPredictor()
            predictor.train(SEED_TRAINING_DATA)
            self.stdout.write('  Difficulty predictor trained')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  Difficulty predictor skipped: {e}'))

        try:
            from ml_engine.models.chatbot import chatbot
            self.stdout.write(f'  Chatbot loaded with {len(chatbot.qa_pairs)} Q&A pairs')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  Chatbot skipped: {e}'))
