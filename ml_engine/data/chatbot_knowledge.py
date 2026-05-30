"""
Seed knowledge base for the phishing education chatbot.

Each entry contains a question, answer, category, and keywords.
The chatbot uses TF-IDF vectorization on questions + keywords to find
the best match for user queries via cosine similarity.
"""

PHISHING_QA_KNOWLEDGE = [
    # ===================================================================
    # BASICS - What is Phishing
    # ===================================================================
    {
        "question": "What is phishing?",
        "answer": "Phishing is a type of cyber attack where criminals impersonate legitimate organizations or people through emails, text messages, phone calls, or fake websites to trick victims into revealing sensitive information such as passwords, credit card numbers, or personal data. It is the most common form of cybercrime worldwide.",
        "category": "basics",
        "keywords": ["phishing", "definition", "cyber attack", "scam", "what is", "meaning", "explain"],
    },
    {
        "question": "How does phishing work?",
        "answer": "Phishing works by exploiting human trust and emotions. Attackers send messages that appear to come from trusted sources (banks, companies, colleagues) containing urgent requests or enticing offers. These messages include malicious links leading to fake websites or attachments containing malware, all designed to steal your credentials, install malware, or trick you into transferring money.",
        "category": "basics",
        "keywords": ["how", "works", "mechanism", "process", "method", "function"],
    },
    {
        "question": "Why is phishing dangerous?",
        "answer": "Phishing is dangerous because it can lead to: 1) Identity theft - criminals use your personal data to impersonate you, 2) Financial loss - stolen bank credentials or fraudulent transfers, 3) Data breaches - unauthorized access to sensitive corporate data, 4) Malware infections - ransomware, keyloggers, and trojans, 5) Account takeover - criminals control your email, social media, or banking accounts. It's the entry point for over 90% of data breaches.",
        "category": "basics",
        "keywords": ["dangerous", "risk", "threat", "impact", "why", "harm", "consequences", "damage"],
    },
    {
        "question": "How common is phishing?",
        "answer": "Phishing is extremely common and growing. Over 3.4 billion phishing emails are sent daily worldwide. About 36% of all data breaches involve phishing, and 1 in every 99 emails is a phishing attempt. In 2024, phishing attacks increased by 58% compared to the previous year. It remains the number one cyber threat for both individuals and organizations across all industries.",
        "category": "basics",
        "keywords": ["common", "statistics", "frequency", "how many", "prevalent", "numbers", "data", "stats"],
    },
    {
        "question": "Who are the targets of phishing?",
        "answer": "Anyone can be a target of phishing. However, common targets include: 1) Employees with access to financial systems, 2) IT administrators with privileged access, 3) Executives and senior management (whaling attacks), 4) New employees unfamiliar with company procedures, 5) Elderly people less familiar with technology, 6) Students and young adults on social media, 7) Small businesses with limited security resources. No one is immune.",
        "category": "basics",
        "keywords": ["target", "victim", "who", "vulnerable", "susceptible", "at risk"],
    },
    {
        "question": "What is the history of phishing?",
        "answer": "Phishing originated in the mid-1990s when hackers targeted AOL users with fake messages to steal passwords. The term 'phishing' comes from 'fishing' - casting bait to catch victims. Since then, it has evolved dramatically: from simple email scams to sophisticated spear phishing, business email compromise, and AI-generated attacks. Today it's a multi-billion dollar criminal industry affecting millions worldwide.",
        "category": "basics",
        "keywords": ["history", "origin", "started", "evolution", "when", "first", "began"],
    },
    {
        "question": "What information do phishers want?",
        "answer": "Phishers typically target: 1) Login credentials (usernames and passwords), 2) Credit card and bank account numbers, 3) Social Security numbers and national IDs, 4) Personal information (date of birth, address, phone), 5) Corporate data and trade secrets, 6) Email account access for further attacks, 7) Two-factor authentication codes, 8) Employee payroll information. This data is used for fraud, identity theft, or sold on the dark web.",
        "category": "basics",
        "keywords": ["information", "data", "steal", "want", "after", "target data", "personal information"],
    },

    # ===================================================================
    # TYPES OF PHISHING
    # ===================================================================
    {
        "question": "What are the different types of phishing?",
        "answer": "The main types of phishing are: 1) Email phishing - mass emails impersonating trusted entities, 2) Spear phishing - targeted attacks on specific individuals, 3) Whaling - targeting high-level executives, 4) Vishing - voice/phone phishing, 5) Smishing - SMS/text message phishing, 6) Clone phishing - duplicating legitimate emails with malicious content, 7) Pharming - redirecting website traffic to fake sites, 8) Angler phishing - using fake social media accounts, 9) Business Email Compromise - impersonating business partners.",
        "category": "types",
        "keywords": ["types", "kinds", "categories", "forms", "different", "varieties", "list"],
    },
    {
        "question": "What is spear phishing?",
        "answer": "Spear phishing is a targeted form of phishing where attackers research specific individuals or organizations to craft highly personalized and convincing messages. Unlike mass phishing, spear phishing emails use personal details like your name, job title, recent purchases, or activities to appear legitimate. For example, an attacker might reference a real conference you attended. These attacks are much harder to detect and have a significantly higher success rate than generic phishing.",
        "category": "types",
        "keywords": ["spear", "targeted", "personalized", "specific", "individual"],
    },
    {
        "question": "What is whaling?",
        "answer": "Whaling is a type of spear phishing that specifically targets high-profile individuals like CEOs, CFOs, and other senior executives. These attacks are meticulously crafted to look like critical business communications such as legal subpoenas, executive complaints, board meeting agendas, or urgent wire transfer requests. The goal is typically large financial fraud or access to sensitive corporate data. Whaling attacks are among the most costly, with single incidents sometimes exceeding millions of dollars.",
        "category": "types",
        "keywords": ["whaling", "executive", "CEO", "CFO", "high profile", "senior", "whale"],
    },
    {
        "question": "What is vishing?",
        "answer": "Vishing (voice phishing) is a type of phishing conducted over phone calls. Attackers call victims pretending to be from banks, government agencies (like the IRS), or tech support companies, creating urgency to trick victims into revealing personal information, account credentials, or making payments. Common vishing tactics include fake fraud alerts from your bank, IRS tax scam calls, tech support scams claiming your computer has a virus, and impersonating law enforcement.",
        "category": "types",
        "keywords": ["vishing", "voice", "phone", "call", "telephone", "phone call"],
    },
    {
        "question": "What is smishing?",
        "answer": "Smishing (SMS phishing) is phishing conducted through text messages on your mobile phone. Attackers send SMS messages containing malicious links or requests for personal information, often pretending to be delivery services (USPS, FedEx, DHL), banks, government agencies, or subscription services. Common examples include fake package delivery notifications, account verification codes you didn't request, and messages claiming you've won a prize.",
        "category": "types",
        "keywords": ["smishing", "SMS", "text message", "mobile", "phone text"],
    },
    {
        "question": "What is clone phishing?",
        "answer": "Clone phishing is when an attacker creates a nearly identical copy of a legitimate email that the victim previously received, but replaces the links or attachments with malicious ones. The attacker then sends this cloned email claiming it's an updated version, a correction, or a resend. It's particularly dangerous because the victim recognizes the original email content and trusts it. Attackers often gain access to the original email through a compromised email account.",
        "category": "types",
        "keywords": ["clone", "copy", "duplicate", "replica", "cloned"],
    },
    {
        "question": "What is pharming?",
        "answer": "Pharming is a cyber attack that redirects website traffic from a legitimate site to a fraudulent one, even when users type the correct URL in their browser. This is done by exploiting DNS servers (DNS poisoning) or modifying the hosts file on a victim's computer. Unlike phishing, pharming doesn't require the victim to click a malicious link - they're automatically and invisibly redirected to the fake site. This makes it extremely difficult to detect.",
        "category": "types",
        "keywords": ["pharming", "DNS", "redirect", "website redirect", "DNS poisoning"],
    },
    {
        "question": "What is business email compromise?",
        "answer": "Business Email Compromise (BEC) is a sophisticated phishing attack where criminals impersonate or hack into business email accounts to authorize fraudulent wire transfers, redirect payroll, or obtain sensitive data. BEC attacks often target employees in finance or HR departments. Common scenarios include: fake CEO requesting urgent wire transfer, vendor sending updated bank details, or attorney requesting confidential information. BEC has caused over $50 billion in global losses.",
        "category": "types",
        "keywords": ["BEC", "business email compromise", "wire transfer", "CEO fraud", "invoice fraud", "corporate"],
    },
    {
        "question": "What is angler phishing?",
        "answer": "Angler phishing uses fake social media accounts to target users who post complaints or questions to companies on platforms like Twitter, Facebook, or Instagram. Attackers create fake customer support accounts with similar names and logos, then respond to users' complaints with links to fake help pages designed to steal login credentials. Always verify social media support accounts by checking for verification badges and account age.",
        "category": "types",
        "keywords": ["angler", "social media", "twitter", "facebook", "instagram", "fake support", "customer service"],
    },
    {
        "question": "What is email phishing?",
        "answer": "Email phishing is the most common type of phishing where attackers send fraudulent emails to a large number of people, impersonating well-known companies like banks, online retailers, or government agencies. These emails contain malicious links to fake websites or infected attachments. They use urgency, fear, or enticing offers to get recipients to click. While less targeted than spear phishing, the sheer volume means many people fall victim.",
        "category": "types",
        "keywords": ["email phishing", "mass email", "bulk", "traditional", "standard phishing"],
    },
    {
        "question": "What is a watering hole attack?",
        "answer": "A watering hole attack is when hackers compromise a website that their target group frequently visits, rather than attacking the targets directly. For example, if attackers want to target employees of a specific company, they might hack an industry news site or forum those employees regularly visit. When employees visit the compromised site, malware is downloaded to their devices. This attack is named after predators who wait near water sources for prey.",
        "category": "types",
        "keywords": ["watering hole", "website compromise", "industry site", "targeted website"],
    },
    {
        "question": "What is a QR code phishing attack?",
        "answer": "QR code phishing (also called 'quishing') uses QR codes to redirect victims to malicious websites. Attackers place fake QR codes over legitimate ones on posters, menus, parking meters, or send them in emails. When scanned, the QR code takes the victim to a phishing site that steals credentials or installs malware. Always verify QR codes before scanning, especially in public places, and check the URL your phone shows before opening it.",
        "category": "types",
        "keywords": ["QR code", "quishing", "scan", "QR", "barcode"],
    },

    # ===================================================================
    # HOW TO IDENTIFY / SPOT / RECOGNIZE PHISHING
    # ===================================================================
    {
        "question": "How do I spot a phishing email?",
        "answer": "To spot a phishing email, look for these warning signs: 1) Suspicious sender address with misspelled domains (e.g., support@amaz0n.com), 2) Generic greetings like 'Dear Customer' instead of your name, 3) Urgent or threatening language pressuring immediate action, 4) Grammar and spelling errors, 5) Suspicious links - hover to check the real URL before clicking, 6) Unexpected attachments, 7) Requests for personal information that legitimate companies wouldn't ask via email, 8) Too-good-to-be-true offers, 9) Mismatched display name and email address, 10) Pressure to bypass normal procedures.",
        "category": "identification",
        "keywords": ["spot", "identify", "recognize", "detect", "tell", "know", "warning signs", "red flags", "find", "notice", "catch", "distinguish", "phishing email", "fake email", "scam email"],
    },
    {
        "question": "What are the red flags of phishing?",
        "answer": "Key red flags that indicate a phishing attempt: 1) Urgency - 'Your account will be suspended in 24 hours', 2) Suspicious sender - email domain doesn't match the company, 3) Generic greeting - 'Dear Sir/Madam' instead of your name, 4) Bad grammar and typos - professional companies proofread their emails, 5) Suspicious links - hover to reveal the real URL, 6) Request for sensitive data - passwords, SSN, credit cards, 7) Threatening tone - legal action or account closure, 8) Unexpected attachments - especially .exe, .zip, or .docm files, 9) Too good to be true - prizes, free money, 10) Impersonation of authority - fake CEO or government emails.",
        "category": "identification",
        "keywords": ["red flags", "warning signs", "indicators", "clues", "signals", "telltale", "giveaway"],
    },
    {
        "question": "How do I check if a link is safe?",
        "answer": "To check if a link is safe: 1) Hover over it without clicking to see the actual URL in the bottom-left of your browser, 2) Look for misspellings in the domain name (e.g., 'paypa1.com' instead of 'paypal.com'), 3) Check if it uses HTTPS (look for the padlock icon), 4) Use URL scanning tools like VirusTotal or Google Safe Browsing, 5) Verify the domain matches the claimed sender's organization, 6) Be wary of shortened URLs (bit.ly, tinyurl) - use a URL expander to see the real link, 7) When in doubt, navigate to the website directly by typing the URL yourself instead of clicking the link.",
        "category": "identification",
        "keywords": ["link", "URL", "check link", "safe link", "verify link", "hover", "click", "suspicious link"],
    },
    {
        "question": "What are signs of a phishing website?",
        "answer": "Signs of a phishing website include: 1) Misspelled domain names (e.g., 'amaz0n.com' or 'bankofamerica-login.com'), 2) Missing or invalid SSL certificate (no padlock in address bar), 3) Poor design quality, broken images, or misaligned elements, 4) No contact information, about page, or privacy policy, 5) Unusual pop-ups immediately asking for login credentials, 6) URL doesn't match the organization it claims to be, 7) Recently created domain (check with WHOIS lookup), 8) Asks for more information than the real site would, 9) Login page looks slightly different from the real one.",
        "category": "identification",
        "keywords": ["website", "fake site", "fake website", "phishing site", "fraudulent site", "bogus site"],
    },
    {
        "question": "How can I tell if an email is legitimate or fake?",
        "answer": "To verify if an email is legitimate: 1) Check the sender's full email address, not just the display name, 2) Look for personalization - legitimate emails usually address you by name, 3) Verify by contacting the company directly through their official website (not using contact info from the email), 4) Check for consistent branding and formatting, 5) Hover over all links to check their real destinations, 6) Be suspicious of any email requesting sensitive information, 7) Check your account directly by typing the company's URL in your browser instead of clicking email links, 8) Look at email headers for signs of spoofing.",
        "category": "identification",
        "keywords": ["legitimate", "real", "fake", "tell", "verify", "authentic", "genuine", "trustworthy", "legit"],
    },
    {
        "question": "What is a suspicious email address?",
        "answer": "A suspicious email address often has: 1) Misspelled company names (support@amaz0n.com instead of @amazon.com), 2) Extra characters or numbers (paypal-security123@gmail.com), 3) Free email provider for business communication (microsoft.support@yahoo.com), 4) Unfamiliar domain extensions (.xyz, .top instead of .com), 5) Long random strings before the @ symbol (a8x9k2@company.com), 6) Slight variations that are easy to miss (rn looks like m). Always check the full email address by clicking on the sender's name, not just the display name.",
        "category": "identification",
        "keywords": ["suspicious email address", "sender address", "fake sender", "spoofed sender", "email from"],
    },
    {
        "question": "What does a phishing text message look like?",
        "answer": "Phishing text messages (smishing) typically: 1) Come from unknown or short-code numbers, 2) Contain shortened URLs (bit.ly links), 3) Create false urgency ('Your account will be locked in 2 hours'), 4) Claim you've won a prize or contest you never entered, 5) Pretend to be delivery notifications ('Your package could not be delivered'), 6) Request identity verification you didn't initiate, 7) Contain grammar mistakes, 8) Ask you to call an unfamiliar number. Never click links in unexpected text messages - go directly to the company's website or app.",
        "category": "identification",
        "keywords": ["text message", "SMS look like", "smishing example", "fake text", "scam text"],
    },
    {
        "question": "How do I recognize a phishing phone call?",
        "answer": "Signs of a phishing phone call (vishing): 1) Caller creates extreme urgency or pressure, 2) They claim to be from your bank, IRS, or tech support, 3) They ask for sensitive information (SSN, passwords, PINs), 4) They threaten arrest, account closure, or legal action, 5) They ask you to install remote access software, 6) They request payment via gift cards or cryptocurrency, 7) Caller ID shows a spoofed legitimate number, 8) They don't let you hang up and call back. Legitimate organizations never demand immediate action over the phone.",
        "category": "identification",
        "keywords": ["phone call", "recognize", "vishing signs", "fake call", "scam call", "telephone scam"],
    },
    {
        "question": "How to spot a fake login page?",
        "answer": "To spot a fake login page: 1) Check the URL carefully - it should exactly match the official website domain, 2) Look for HTTPS and a valid security certificate (padlock icon), 3) Compare the page design to the real website - fake pages may have slight differences in colors, fonts, or layout, 4) Try entering a fake password first - a phishing page will accept any input, while the real page won't, 5) Check if the rest of the website works - fake pages usually only have the login form, 6) Use your password manager - it won't auto-fill on a fake domain.",
        "category": "identification",
        "keywords": ["fake login", "login page", "fake page", "phishing page", "credential page"],
    },

    # ===================================================================
    # WHAT TO DO / RESPONSE
    # ===================================================================
    {
        "question": "What should I do if I clicked a phishing link?",
        "answer": "If you clicked a phishing link: 1) Don't enter any information on the page - close it immediately, 2) Disconnect from the internet to prevent malware communication, 3) Run a full antivirus/anti-malware scan on your device, 4) Change passwords for any accounts you may have exposed, starting with email and banking, 5) Enable two-factor authentication on all important accounts, 6) Monitor your accounts and credit reports for suspicious activity, 7) Report the incident to your IT department (if at work) or email provider, 8) Check for any unauthorized transactions or changes to your accounts.",
        "category": "response",
        "keywords": ["clicked", "click link", "what to do clicked", "accidentally clicked", "opened link"],
    },
    {
        "question": "What should I do if I gave my password to a phishing site?",
        "answer": "If you entered your password on a phishing site, act fast: 1) Change that password immediately on the real website, 2) Change the password on ALL other accounts where you used the same or similar password, 3) Enable two-factor authentication everywhere possible, 4) Check for unauthorized account activity (login history, sent emails, transactions), 5) Contact the service's support team to report the compromise, 6) Monitor your email for password reset attempts you didn't make, 7) Check if your credentials appear on haveibeenpwned.com, 8) Consider using a password manager to prevent future password reuse.",
        "category": "response",
        "keywords": ["gave password", "entered password", "password stolen", "compromised password", "submitted password", "typed password"],
    },
    {
        "question": "How do I report a phishing email?",
        "answer": "To report a phishing email: 1) Use your email client's built-in 'Report Phishing' or 'Report Spam' button, 2) Forward the email to your email provider (e.g., reportphishing@apple.com, phishing@paypal.com), 3) Report to the Anti-Phishing Working Group at reportphishing@apwg.org, 4) Forward to the FTC at spam@uce.gov (US), 5) Report to the impersonated company through their official website, 6) Report to your IT security team if you received it at work, 7) In the UK, forward to report@phishing.gov.uk. Do NOT reply directly to the phishing email.",
        "category": "response",
        "keywords": ["report", "report phishing", "forward phishing", "notify", "where to report", "submit report"],
    },
    {
        "question": "What if I downloaded a phishing attachment?",
        "answer": "If you downloaded a phishing attachment: 1) If you haven't opened it, delete it immediately without opening, 2) Disconnect from the internet right away to prevent malware from spreading, 3) Run a full antivirus/anti-malware scan (use Malwarebytes or Windows Defender), 4) Delete the file and empty your recycle bin, 5) Check for any newly installed programs you don't recognize, 6) Change your passwords from a DIFFERENT clean device, 7) Monitor your accounts for unusual activity, 8) Contact IT security if on a work device, 9) If you opened it, consider the device potentially compromised and get professional help.",
        "category": "response",
        "keywords": ["downloaded", "attachment", "file download", "opened file", "malware file", "suspicious file"],
    },
    {
        "question": "What to do if my email account was hacked?",
        "answer": "If your email account was hacked: 1) Change your password immediately (use your phone or another device), 2) Enable two-factor authentication, 3) Check and remove any unfamiliar forwarding rules or filters, 4) Review connected apps and revoke unknown ones, 5) Check your sent folder for emails the hacker sent from your account, 6) Warn your contacts that your account was compromised, 7) Update passwords on accounts linked to that email, 8) Check recovery phone number and backup email - hackers may have changed these, 9) Review recent login activity for unauthorized locations.",
        "category": "response",
        "keywords": ["hacked", "email hacked", "account hacked", "compromised account", "taken over", "hijacked"],
    },
    {
        "question": "What should I do if I fell for a phishing scam?",
        "answer": "If you fell for a phishing scam: 1) Stay calm - acting quickly is more important than panicking, 2) Change all potentially compromised passwords immediately, 3) Contact your bank if you shared financial information - they can freeze your account, 4) Enable 2FA on all accounts, 5) Run anti-malware scans on your devices, 6) Report the scam to relevant authorities (FTC, local police, IC3.gov), 7) Place a fraud alert on your credit reports with the credit bureaus, 8) Monitor your accounts and credit for months afterward, 9) Learn from the experience to avoid future attacks.",
        "category": "response",
        "keywords": ["fell for", "victim", "scammed", "tricked", "deceived", "fooled", "phished"],
    },
    {
        "question": "Should I pay a ransomware demand?",
        "answer": "Cybersecurity experts and law enforcement strongly advise against paying ransomware demands because: 1) There's no guarantee you'll get your data back, 2) It funds criminal organizations and encourages more attacks, 3) You may be targeted again since you've shown willingness to pay, 4) It may violate sanctions laws. Instead: disconnect infected systems, report to law enforcement (FBI's IC3.gov), restore from backups, and get professional incident response help. Prevention is key - maintain regular offline backups.",
        "category": "response",
        "keywords": ["ransomware", "pay", "ransom", "encrypted files", "locked files", "demand"],
    },

    # ===================================================================
    # SOCIAL ENGINEERING
    # ===================================================================
    {
        "question": "What is social engineering?",
        "answer": "Social engineering is the psychological manipulation of people into performing actions or divulging confidential information. Instead of hacking computers, social engineers hack human psychology by exploiting emotions like trust, fear, curiosity, greed, and urgency. Phishing is the most common form of social engineering. Other types include pretexting (fabricated scenarios), baiting (tempting offers), tailgating (following people into secure areas), and quid pro quo (offering something in exchange for information).",
        "category": "social_engineering",
        "keywords": ["social engineering", "manipulation", "psychology", "human hacking", "psychological"],
    },
    {
        "question": "What tactics do phishers use to trick people?",
        "answer": "Phishers exploit these psychological tactics: 1) Urgency - 'Act within 24 hours or your account will be closed', 2) Authority - impersonating bosses, banks, IRS, or police, 3) Fear - threatening legal action, fines, or account suspension, 4) Curiosity - 'You won't believe this photo of you', 5) Greed - fake lottery wins, tax refunds, or job offers, 6) Helpfulness - pretending to be tech support solving your 'problem', 7) Familiarity - using personal details to build trust, 8) Reciprocity - offering a favor before asking for information, 9) Scarcity - limited time offers to prevent careful thinking.",
        "category": "social_engineering",
        "keywords": ["tactics", "tricks", "techniques", "psychology", "manipulation methods", "strategies"],
    },
    {
        "question": "What is pretexting?",
        "answer": "Pretexting is a social engineering technique where an attacker creates a fabricated scenario (pretext) to engage the victim and gain their trust before extracting information. For example, calling an employee while pretending to be from the IT department needing their login credentials to 'fix a system issue', or posing as a vendor who needs to verify bank details. The attacker invests time building a convincing backstory to make the interaction seem natural and legitimate.",
        "category": "social_engineering",
        "keywords": ["pretexting", "scenario", "fabricated story", "fake identity", "impersonate", "pretext"],
    },
    {
        "question": "What is baiting?",
        "answer": "Baiting is a social engineering attack that lures victims with a false promise or enticing item. Physical baiting: leaving infected USB drives labeled 'Salary Data' or 'Confidential' in parking lots or lobbies hoping someone will plug them into their computer. Online baiting: fake free software downloads, pirated movie sites, or too-good-to-be-true offers that install malware or steal credentials. The attacker relies on human curiosity and greed to get victims to take the bait.",
        "category": "social_engineering",
        "keywords": ["baiting", "lure", "USB drive", "free download", "entice", "tempt", "bait"],
    },
    {
        "question": "What is tailgating in security?",
        "answer": "Tailgating (also called piggybacking) is a physical social engineering attack where an unauthorized person follows an authorized employee through a secure door or entrance. The attacker might carry boxes and ask someone to hold the door, or pretend to have forgotten their access badge. To prevent tailgating: never hold doors for strangers in secure areas, always use your own access card, report suspicious individuals, and politely ask unknown people to badge in themselves.",
        "category": "social_engineering",
        "keywords": ["tailgating", "piggybacking", "physical security", "door", "access", "building"],
    },
    {
        "question": "What is a quid pro quo attack?",
        "answer": "A quid pro quo attack is a social engineering technique where the attacker offers something in exchange for information or access. Common examples: 1) Fake IT support calling employees offering to help fix problems in exchange for login credentials, 2) Offering free software or services that require account details to activate, 3) Fake surveys offering gift cards in exchange for personal information. The 'favor' creates a sense of obligation, making victims more likely to comply.",
        "category": "social_engineering",
        "keywords": ["quid pro quo", "exchange", "favor", "trade", "offer"],
    },

    # ===================================================================
    # PASSWORD SECURITY
    # ===================================================================
    {
        "question": "How do I create a strong password?",
        "answer": "To create a strong password: 1) Use at least 12-16 characters - longer is always better, 2) Mix uppercase, lowercase, numbers, and special symbols, 3) Never use personal information (names, birthdays, pet names), 4) Avoid common patterns (password123, qwerty, abc123), 5) Use a passphrase - a series of random unrelated words (e.g., 'purple-elephant-bicycle-sunset'), 6) Make every password unique for each account, 7) Use a password manager to generate and securely store complex passwords, 8) Never share your password with anyone.",
        "category": "password_security",
        "keywords": ["strong password", "create password", "good password", "secure password", "password tips", "make password"],
    },
    {
        "question": "What is two-factor authentication?",
        "answer": "Two-factor authentication (2FA) adds an extra layer of security beyond just a password. It requires two different types of verification: something you know (password) AND something you have (phone, security key) or something you are (fingerprint, face). Even if a phisher steals your password, they can't access your account without the second factor. Use authenticator apps (Google Authenticator, Authy) rather than SMS-based 2FA when possible, as SMS can be intercepted through SIM swapping.",
        "category": "password_security",
        "keywords": ["2FA", "two factor", "MFA", "multi factor", "authentication", "verification", "second factor"],
    },
    {
        "question": "What is a password manager?",
        "answer": "A password manager is a secure application that generates, stores, and auto-fills strong unique passwords for all your accounts. You only need to remember one master password. Benefits: 1) Creates random complex passwords you don't need to memorize, 2) Prevents password reuse across sites, 3) Auto-fills only on the correct domain (won't fill on phishing sites!), 4) Stores notes and other sensitive data securely, 5) Syncs across all your devices. Recommended options: Bitwarden (free/open-source), 1Password, KeePass, or Dashlane.",
        "category": "password_security",
        "keywords": ["password manager", "password vault", "store passwords", "bitwarden", "1password", "lastpass", "keepass"],
    },
    {
        "question": "Why should I use unique passwords for every account?",
        "answer": "Using unique passwords is critical because of credential stuffing attacks. When one service gets hacked (and breaches happen regularly), attackers automatically test those stolen username/password combinations on hundreds of other websites. If you reuse the same password for your email, bank, and social media, one breach compromises ALL your accounts. A 2023 study found that 65% of people reuse passwords. A password manager makes unique passwords effortless to maintain.",
        "category": "password_security",
        "keywords": ["unique passwords", "different passwords", "reuse", "same password", "credential stuffing", "password reuse"],
    },
    {
        "question": "How often should I change my password?",
        "answer": "Modern security guidance (from NIST and Microsoft) no longer recommends regular password changes unless there's a reason to believe your account has been compromised. Forced periodic changes often lead to weaker passwords. Instead: 1) Use strong, unique passwords from the start, 2) Change immediately if a service reports a data breach, 3) Change if you notice suspicious account activity, 4) Change if you shared it with someone, 5) Use 2FA as additional protection. Focus on password quality over frequency of changes.",
        "category": "password_security",
        "keywords": ["change password", "how often", "password rotation", "update password", "reset password"],
    },
    {
        "question": "What is a passphrase?",
        "answer": "A passphrase is a password made up of multiple random words strung together, like 'correct-horse-battery-staple' or 'purple-mountain-toaster-bicycle'. Passphrases are both more secure and easier to remember than traditional complex passwords. A 4-word passphrase is extremely difficult for computers to crack (trillions of possible combinations) but simple for humans to remember. The key is using truly random, unrelated words - not phrases from songs, books, or common sayings.",
        "category": "password_security",
        "keywords": ["passphrase", "word password", "multiple words", "easy to remember", "diceware"],
    },

    # ===================================================================
    # PROTECTION & PREVENTION
    # ===================================================================
    {
        "question": "How can I protect myself from phishing?",
        "answer": "To protect yourself from phishing: 1) Be skeptical of unexpected messages, especially those creating urgency, 2) Verify sender identities through official channels before responding, 3) Never click links in suspicious emails - navigate to websites directly, 4) Use two-factor authentication on all important accounts, 5) Keep your operating system, browser, and antivirus updated, 6) Use a password manager with unique passwords, 7) Hover over links to check URLs before clicking, 8) Enable email filtering and spam protection, 9) Don't download unexpected attachments, 10) Educate yourself about current phishing tactics regularly.",
        "category": "prevention",
        "keywords": ["protect", "prevent", "safe", "security", "avoid", "defense", "guard", "stay safe", "protection tips"],
    },
    {
        "question": "What security software should I use?",
        "answer": "Essential security software for phishing protection: 1) Antivirus/anti-malware - Windows Defender (built-in), Malwarebytes, or Bitdefender, 2) Web browser with phishing protection - Chrome, Firefox, or Edge (all have built-in safe browsing), 3) Email client with spam filtering - Gmail, Outlook, or ProtonMail, 4) Password manager - Bitwarden, 1Password, or KeePass, 5) VPN for public Wi-Fi - ProtonVPN, Mullvad, or NordVPN, 6) Browser extensions - uBlock Origin for ad blocking, HTTPS Everywhere. Keep ALL software updated to patch vulnerabilities.",
        "category": "prevention",
        "keywords": ["software", "antivirus", "tools", "security tools", "applications", "programs", "apps"],
    },
    {
        "question": "How do I keep my email safe?",
        "answer": "To keep your email account secure: 1) Use a strong unique password (at least 16 characters), 2) Enable two-factor authentication (preferably with authenticator app), 3) Never open unexpected attachments, 4) Be cautious with links - hover to check before clicking, 5) Use your email provider's spam/phishing filters (don't turn them off), 6) Don't share your email address on public forums unnecessarily, 7) Use separate email addresses for important accounts vs. newsletters/signups, 8) Regularly review connected apps and revoke access to ones you don't use, 9) Always log out of email on shared or public devices.",
        "category": "prevention",
        "keywords": ["email safe", "secure email", "protect email", "email security", "inbox protection"],
    },
    {
        "question": "Is it safe to use public Wi-Fi?",
        "answer": "Public Wi-Fi carries significant security risks because attackers can intercept your data through man-in-the-middle attacks or set up fake 'evil twin' hotspots that look like legitimate networks. To stay safe on public Wi-Fi: 1) Always use a VPN to encrypt your connection, 2) Only visit HTTPS websites, 3) Avoid logging into banking or email accounts, 4) Never make financial transactions, 5) Turn off auto-connect to Wi-Fi networks, 6) Verify the network name with staff before connecting, 7) Use your mobile data instead for sensitive activities, 8) Disable file sharing.",
        "category": "prevention",
        "keywords": ["public wifi", "Wi-Fi", "hotspot", "wireless", "coffee shop", "airport wifi", "hotel wifi"],
    },
    {
        "question": "How do I protect my phone from phishing?",
        "answer": "To protect your phone from phishing: 1) Don't click links in unexpected text messages, 2) Only install apps from official app stores (Google Play, Apple App Store), 3) Keep your phone's operating system and apps updated, 4) Enable biometric authentication (fingerprint/face), 5) Be cautious of QR codes from unknown sources, 6) Don't grant unnecessary permissions to apps, 7) Use a mobile security app, 8) Be wary of phone calls requesting personal information, 9) Enable spam call/text filtering, 10) Don't jailbreak or root your device as it removes security protections.",
        "category": "prevention",
        "keywords": ["phone", "mobile", "smartphone", "android", "iPhone", "mobile security", "cell phone"],
    },
    {
        "question": "How can I browse the internet safely?",
        "answer": "Safe browsing practices to avoid phishing: 1) Keep your browser updated to the latest version, 2) Only enter sensitive information on HTTPS sites (padlock icon), 3) Use a reputable ad blocker (uBlock Origin) to block malicious ads, 4) Don't download software from unknown websites, 5) Verify website URLs before entering any information, 6) Use your browser's built-in phishing/malware protection (don't disable it), 7) Clear cookies and browsing data regularly, 8) Be suspicious of pop-ups requesting login credentials, 9) Use a privacy-focused search engine, 10) Consider using DNS-level protection like Cloudflare (1.1.1.1) or Quad9.",
        "category": "prevention",
        "keywords": ["browse safely", "internet safety", "web browsing", "online safety", "safe surfing", "browser security"],
    },
    {
        "question": "How do I protect my social media accounts?",
        "answer": "To protect your social media from phishing: 1) Enable two-factor authentication on all accounts, 2) Use unique strong passwords for each platform, 3) Be skeptical of friend requests from unknown people, 4) Don't click suspicious links in messages or posts, 5) Limit personal information in your public profile, 6) Review privacy settings and connected apps regularly, 7) Be cautious of quizzes and games that ask for account access, 8) Verify account handles before responding to 'official' support messages, 9) Don't share location data in real-time, 10) Watch for fake profiles impersonating friends.",
        "category": "prevention",
        "keywords": ["social media", "facebook", "instagram", "twitter", "linkedin", "social accounts", "online accounts"],
    },

    # ===================================================================
    # REAL-WORLD EXAMPLES
    # ===================================================================
    {
        "question": "What are common phishing email examples?",
        "answer": "Common phishing email scenarios include: 1) 'Your PayPal/Apple account has been limited - verify now', 2) 'Package delivery failed - click to reschedule' (fake DHL/FedEx/UPS), 3) 'Verify your Microsoft 365 account or lose access', 4) 'You have a new unpaid invoice attached', 5) 'Your Netflix/Spotify subscription has expired', 6) 'CEO: Please wire transfer $50,000 urgently', 7) 'IRS: You're eligible for a tax refund', 8) 'Your bank detected suspicious activity - confirm your identity', 9) 'LinkedIn: Someone viewed your profile', 10) 'Google: Unusual sign-in detected on your account'.",
        "category": "examples",
        "keywords": ["examples", "common phishing", "real examples", "typical", "sample", "common scams"],
    },
    {
        "question": "What is the Nigerian prince scam?",
        "answer": "The Nigerian prince scam (also called 419 scam or advance-fee fraud) is one of the oldest phishing scams, dating back to the 1990s. An email claims to be from a wealthy individual (often a prince, government official, or dying widow) who needs your help to transfer millions of dollars out of their country, promising you a generous share (usually 20-30%). To receive the money, you must first pay various 'fees' (legal fees, taxes, bribes). These fees keep escalating until the victim realizes the promised fortune will never arrive. Despite being well-known, this scam still generates hundreds of millions in losses annually.",
        "category": "examples",
        "keywords": ["Nigerian prince", "419 scam", "advance fee", "money transfer scam", "inheritance scam"],
    },
    {
        "question": "What is a tech support scam?",
        "answer": "Tech support scams involve criminals contacting you (by phone, email, or browser pop-up) claiming your computer has a virus, has been hacked, or needs urgent repair. They pose as Microsoft, Apple, or your ISP and pressure you to: 1) Grant remote access to your computer, 2) Install 'security' software that is actually malware, 3) Pay hundreds of dollars for fake repairs or subscriptions. Red flags: legitimate companies NEVER make unsolicited calls about computer problems, never ask for remote access, and never demand payment via gift cards. If you see a scary browser pop-up with a phone number, it's always a scam - close the tab.",
        "category": "examples",
        "keywords": ["tech support", "technical support", "Microsoft scam", "computer virus", "remote access scam", "pop-up scam"],
    },
    {
        "question": "What is a romance scam?",
        "answer": "Romance scams (also called catfishing) are social engineering attacks where criminals create fake profiles on dating sites or social media to develop romantic relationships with victims. After weeks or months of building emotional trust, they start requesting money for fake emergencies (medical bills, travel costs, investment opportunities). Warning signs: 1) They can never video call, 2) The relationship moves unusually fast, 3) They always have excuses not to meet in person, 4) They eventually ask for money or gift cards, 5) Their photos may be stolen from other profiles (reverse image search to verify).",
        "category": "examples",
        "keywords": ["romance scam", "dating scam", "catfishing", "love scam", "online dating"],
    },
    {
        "question": "What is a job offer phishing scam?",
        "answer": "Job offer phishing scams exploit job seekers with fake employment opportunities. Common tactics: 1) Unsolicited job offers with high pay and minimal requirements, 2) Requests for personal information (SSN, bank details) during 'onboarding', 3) Asking you to purchase equipment with a company check that bounces, 4) Fake recruiters on LinkedIn, 5) Work-from-home offers requiring upfront fees, 6) Interview conducted only via text/chat (never video). Legitimate employers don't ask for banking info before hiring, don't require payments from candidates, and will conduct formal interviews.",
        "category": "examples",
        "keywords": ["job offer", "employment scam", "fake job", "hiring scam", "recruitment scam", "work from home"],
    },
    {
        "question": "What is a cryptocurrency phishing scam?",
        "answer": "Cryptocurrency phishing scams target digital asset holders through: 1) Fake exchange websites that steal wallet credentials, 2) Fraudulent airdrop offers requiring wallet connection to malicious sites, 3) Impersonation of crypto projects on Discord/Telegram, 4) Fake wallet apps that steal private keys, 5) Phishing emails about 'suspicious activity' on your crypto account, 6) Social media giveaway scams ('Send 1 ETH, get 2 back'), 7) Fake NFT minting sites. Never share your seed phrase/private keys, verify URLs carefully, and be extremely skeptical of unsolicited crypto offers.",
        "category": "examples",
        "keywords": ["cryptocurrency", "crypto", "bitcoin", "ethereum", "wallet", "blockchain", "NFT", "crypto scam"],
    },

    # ===================================================================
    # ORGANIZATION & WORKPLACE
    # ===================================================================
    {
        "question": "How can organizations prevent phishing?",
        "answer": "Organizations can prevent phishing by: 1) Conducting regular security awareness training for all employees, 2) Running simulated phishing exercises to test and improve awareness, 3) Implementing email authentication protocols (SPF, DKIM, DMARC), 4) Deploying email filtering and anti-phishing tools, 5) Enforcing multi-factor authentication company-wide, 6) Creating clear incident reporting procedures, 7) Implementing least-privilege access policies, 8) Keeping all systems patched and updated, 9) Having a tested incident response plan, 10) Using web filtering to block known malicious sites, 11) Implementing a zero-trust security model.",
        "category": "organization",
        "keywords": ["organization", "company", "business", "workplace", "corporate", "enterprise", "prevent"],
    },
    {
        "question": "What is security awareness training?",
        "answer": "Security awareness training educates employees about cyber threats like phishing and teaches them to recognize and respond to attacks. An effective program includes: 1) Regular training sessions (not just annual), 2) Simulated phishing tests with immediate feedback, 3) Clear step-by-step reporting procedures, 4) Real-world examples relevant to your industry, 5) Short engaging modules (microlearning), 6) Metrics to measure improvement, 7) Gamification to encourage participation, 8) Role-specific training for high-risk teams (finance, HR). Studies show organizations with regular training reduce phishing click rates by up to 75%.",
        "category": "organization",
        "keywords": ["training", "awareness", "education", "employees", "learn", "program", "course"],
    },
    {
        "question": "What is DMARC?",
        "answer": "DMARC (Domain-based Message Authentication, Reporting, and Conformance) is an email authentication protocol that protects your domain from being used in phishing attacks. It works alongside SPF (verifies sending server) and DKIM (verifies email hasn't been altered) to confirm emails genuinely come from the claimed domain. With DMARC, organizations can instruct receiving mail servers to reject or quarantine emails that fail authentication, preventing attackers from spoofing their domain in phishing campaigns. Implementing DMARC can block up to 98% of spoofed emails.",
        "category": "organization",
        "keywords": ["DMARC", "SPF", "DKIM", "email authentication", "domain spoofing", "email protocol"],
    },
    {
        "question": "What is a phishing simulation?",
        "answer": "A phishing simulation is a security training exercise where an organization sends fake phishing emails to its own employees to test their ability to recognize and report phishing attempts. Benefits: 1) Identifies employees who need additional training, 2) Provides measurable security metrics, 3) Creates a learning opportunity with immediate feedback, 4) Builds a security-conscious culture, 5) Reduces real phishing success rates over time. Simulations should be conducted regularly, vary in difficulty, and always include educational follow-up for those who click.",
        "category": "organization",
        "keywords": ["simulation", "phishing test", "fake phishing", "exercise", "drill", "simulated"],
    },
    {
        "question": "What should an organization do after a phishing attack?",
        "answer": "After a phishing attack on an organization: 1) Activate your incident response plan, 2) Isolate affected systems from the network, 3) Reset compromised credentials immediately, 4) Investigate the scope - how many employees were affected?, 5) Preserve evidence for forensic analysis, 6) Notify affected parties and relevant authorities (as required by regulations), 7) Block the phishing domain/sender across the organization, 8) Scan for malware on all affected devices, 9) Conduct a post-incident review, 10) Update security controls based on lessons learned, 11) Provide additional training to affected employees.",
        "category": "organization",
        "keywords": ["after attack", "incident response", "breach response", "organization attacked", "company phished"],
    },

    # ===================================================================
    # ADVANCED TOPICS
    # ===================================================================
    {
        "question": "What is a man-in-the-middle attack?",
        "answer": "A man-in-the-middle (MITM) attack is when an attacker secretly positions themselves between two communicating parties, intercepting and potentially altering their data exchange. In phishing contexts, MITM attacks can capture login credentials in real-time, even bypassing some forms of 2FA by relaying authentication tokens. Common MITM techniques: 1) Evil twin Wi-Fi hotspots, 2) ARP spoofing on local networks, 3) DNS hijacking, 4) SSL stripping (downgrading HTTPS to HTTP). Protection: use VPNs, verify HTTPS, and use hardware security keys for 2FA.",
        "category": "advanced",
        "keywords": ["man in the middle", "MITM", "intercept", "eavesdrop", "proxy attack"],
    },
    {
        "question": "What is a zero-day phishing attack?",
        "answer": "A zero-day phishing attack exploits brand new, previously unknown vulnerabilities or techniques that security tools haven't seen before, making them undetectable by traditional signature-based defenses. These attacks may use: 1) New email formatting tricks to bypass filters, 2) Freshly registered domains with no reputation data, 3) Novel social engineering narratives, 4) Newly discovered browser vulnerabilities. Protection relies on user awareness training, behavior-based detection systems, AI-powered email security, and a defense-in-depth approach rather than any single security tool.",
        "category": "advanced",
        "keywords": ["zero day", "zero-day", "unknown attack", "new vulnerability", "novel technique"],
    },
    {
        "question": "What is credential harvesting?",
        "answer": "Credential harvesting is the systematic collection of usernames and passwords through various attack methods. Primary techniques: 1) Phishing emails directing victims to convincing fake login pages for Microsoft 365, Google, banking sites, 2) Keyloggers that record every keystroke, 3) Credential dumps from data breaches sold on the dark web, 4) Fake Wi-Fi hotspots that intercept login data, 5) Malicious browser extensions. Stolen credentials are used for account takeover, sold to other criminals, or used in credential stuffing attacks against multiple services.",
        "category": "advanced",
        "keywords": ["credential harvesting", "steal credentials", "login theft", "password theft", "harvest"],
    },
    {
        "question": "What is URL spoofing?",
        "answer": "URL spoofing is a deception technique where attackers create web addresses that closely resemble legitimate ones: 1) Typosquatting - registering misspelled domains (gooogle.com, amazom.com), 2) Homograph attacks - using visually similar Unicode characters (using Cyrillic 'а' instead of Latin 'a'), 3) Subdomain tricks - legitimate-looking subdomains (paypal.attacker.com), 4) URL shorteners - hiding malicious destinations behind bit.ly links, 5) URL encoding - using %hexadecimal values to obscure the real URL. Always check URLs character by character and type important websites directly.",
        "category": "advanced",
        "keywords": ["URL spoofing", "fake URL", "domain spoofing", "typosquatting", "homograph attack"],
    },
    {
        "question": "What is AI-powered phishing?",
        "answer": "AI-powered phishing uses artificial intelligence and large language models to create more convincing and scalable attacks. AI enables: 1) Perfectly written phishing emails without grammar errors, 2) Deepfake voice calls impersonating real people (CEO's voice), 3) Automated personalization using scraped social media data, 4) Real-time translation for targeting multiple languages, 5) Chatbot-powered phishing that adapts responses, 6) AI-generated fake profile photos, 7) Automated reconnaissance of targets. Defense: be skeptical even of well-written messages, verify requests through separate channels, and use AI-powered defense tools.",
        "category": "advanced",
        "keywords": ["AI phishing", "artificial intelligence", "deepfake", "machine learning", "automated phishing", "GPT"],
    },
    {
        "question": "What is SIM swapping?",
        "answer": "SIM swapping is an attack where criminals convince your mobile carrier to transfer your phone number to a SIM card they control. This allows them to receive your SMS messages, including 2FA codes, password reset links, and verification texts. The process: 1) Attacker gathers your personal info through phishing or data breaches, 2) Calls your carrier pretending to be you, 3) Claims lost/damaged phone and requests SIM transfer, 4) Receives all your calls and texts. Prevention: use authenticator apps instead of SMS for 2FA, set a PIN/password with your carrier, and limit personal info shared online.",
        "category": "advanced",
        "keywords": ["SIM swapping", "SIM swap", "phone number hijack", "mobile attack", "SMS interception"],
    },

    # ===================================================================
    # DATA PRIVACY & IDENTITY PROTECTION
    # ===================================================================
    {
        "question": "How can I protect my personal information online?",
        "answer": "To protect your personal information online: 1) Limit what you share on social media (birthdates, locations, employer), 2) Use privacy settings on all platforms, 3) Be cautious about which websites you create accounts on, 4) Read privacy policies before providing data, 5) Use temporary or disposable email addresses for signups, 6) Opt out of data broker sites that sell your info, 7) Use a VPN to protect your browsing activity, 8) Enable privacy features in your browser, 9) Use encrypted messaging apps (Signal), 10) Regularly Google yourself to see what's publicly available about you.",
        "category": "privacy",
        "keywords": ["personal information", "privacy", "data protection", "online privacy", "protect data", "identity"],
    },
    {
        "question": "What is identity theft?",
        "answer": "Identity theft occurs when someone steals your personal information to commit fraud - opening bank accounts, filing tax returns, making purchases, or taking out loans in your name. Phishing is the primary method criminals use to steal identities. Warning signs: 1) Unfamiliar charges on your statements, 2) Bills for accounts you didn't open, 3) Tax return rejected because one was already filed, 4) Calls from debt collectors about unknown debts, 5) Missing mail. Prevention: monitor credit reports, freeze your credit, use strong security on all accounts, and be cautious about sharing personal information.",
        "category": "privacy",
        "keywords": ["identity theft", "identity fraud", "stolen identity", "impersonation", "fraud"],
    },
    {
        "question": "What is the dark web?",
        "answer": "The dark web is a hidden part of the internet only accessible through special software like Tor. In the context of phishing, the dark web is where: 1) Stolen credentials are bought and sold in bulk, 2) Phishing kits and tools are available for purchase, 3) Personal data from breaches is traded, 4) Credit card numbers and bank details are sold, 5) Identity documents are forged and sold. You can check if your data has been leaked using services like Have I Been Pwned (haveibeenpwned.com). If your data appears in a breach, change those passwords immediately.",
        "category": "privacy",
        "keywords": ["dark web", "darknet", "data breach", "stolen data", "credentials for sale", "haveibeenpwned"],
    },

    # ===================================================================
    # MALWARE RELATED TO PHISHING
    # ===================================================================
    {
        "question": "What is ransomware?",
        "answer": "Ransomware is malware that encrypts your files and demands payment (usually in cryptocurrency) for the decryption key. It's commonly delivered through phishing emails containing malicious attachments or links. Types: 1) Crypto ransomware - encrypts your files, 2) Locker ransomware - locks you out of your device, 3) Double extortion - encrypts AND threatens to leak your data. Prevention: maintain regular offline backups, keep software updated, use email filtering, don't open unexpected attachments, and train employees to recognize phishing.",
        "category": "malware",
        "keywords": ["ransomware", "encrypt", "ransom", "locked files", "WannaCry", "malware"],
    },
    {
        "question": "What is a keylogger?",
        "answer": "A keylogger is malware that secretly records every keystroke you make, capturing passwords, credit card numbers, messages, and other sensitive data. Keyloggers can be delivered through phishing emails with malicious attachments or links to compromised websites. They run silently in the background and send captured data to the attacker. Protection: use antivirus software, keep systems updated, use password managers (which auto-fill rather than type), enable 2FA, and use virtual keyboards for sensitive inputs.",
        "category": "malware",
        "keywords": ["keylogger", "keystroke", "logging", "recording", "spyware", "keyboard"],
    },
    {
        "question": "What is a trojan horse in cybersecurity?",
        "answer": "A trojan horse (or trojan) is malware disguised as legitimate software. Unlike viruses, trojans don't replicate themselves - they rely on users being tricked into installing them. In phishing, trojans are often delivered as: 1) Fake software updates, 2) Email attachments disguised as documents, 3) Free software downloads. Once installed, trojans can: steal data, create backdoors for remote access, install additional malware, or spy on your activities. Prevention: only download software from official sources, verify email attachments, and use antivirus protection.",
        "category": "malware",
        "keywords": ["trojan", "trojan horse", "disguised malware", "fake software", "backdoor"],
    },

    # ===================================================================
    # SPECIFIC SCENARIOS & HOW-TO
    # ===================================================================
    {
        "question": "Is this email from my bank real?",
        "answer": "To verify if a bank email is legitimate: 1) Check the sender's full email address - banks use official domains, not Gmail/Yahoo, 2) Banks NEVER ask for your full password, PIN, or SSN via email, 3) Don't click any links in the email - open a new browser tab and go to your bank's website directly, 4) Call your bank using the number on the back of your card (not a number from the email), 5) Check for generic greetings vs. your actual name, 6) Look for grammatical errors, 7) Banks typically don't send urgent threats via email, 8) Log into your actual bank account to check for any real alerts or messages.",
        "category": "scenarios",
        "keywords": ["bank email", "bank real", "legitimate bank", "bank message", "bank notification"],
    },
    {
        "question": "I received a suspicious email from a colleague. What should I do?",
        "answer": "If you receive a suspicious email from a colleague: 1) Don't click any links or open attachments, 2) Check the sender's actual email address (not just the display name), 3) Contact the colleague through a different channel (phone call, in-person, or separate email) to verify they sent it, 4) Look for signs of compromise: unusual language, unexpected requests, or links to external sites, 5) Report it to your IT security team, 6) The colleague's account may have been compromised - alerting IT helps protect the entire organization. Never forward the suspicious email to others.",
        "category": "scenarios",
        "keywords": ["colleague email", "coworker", "work email", "business email", "suspicious work email"],
    },
    {
        "question": "How do I know if my computer has malware from phishing?",
        "answer": "Signs your computer may have malware from a phishing attack: 1) Computer running unusually slow, 2) Unexpected pop-ups or ads, 3) Programs crashing frequently, 4) New programs or browser extensions you didn't install, 5) Browser homepage changed without your action, 6) High CPU or network usage when idle, 7) Antivirus software disabled or unable to run, 8) Files missing or encrypted, 9) Webcam light turning on unexpectedly, 10) Unusual outgoing network traffic. If you suspect malware: disconnect from the internet, run a full antivirus scan (or boot from a rescue USB), and change all passwords from a clean device.",
        "category": "scenarios",
        "keywords": ["computer malware", "infected", "virus", "malware signs", "compromised computer", "hacked computer"],
    },
    {
        "question": "How to shop online safely?",
        "answer": "To shop online safely and avoid phishing: 1) Only buy from reputable websites you know, 2) Check the URL for HTTPS and verify the domain spelling, 3) Never click shopping links in emails - go directly to the retailer's website, 4) Use credit cards instead of debit cards (better fraud protection), 5) Be wary of deals that seem too good to be true, 6) Use a payment service like PayPal for additional protection, 7) Check reviews of unfamiliar online stores, 8) Monitor your statements after purchases, 9) Avoid saving card details on websites, 10) Don't shop on public Wi-Fi without a VPN.",
        "category": "scenarios",
        "keywords": ["online shopping", "buy online", "ecommerce", "shopping safely", "credit card", "purchase"],
    },

    # ===================================================================
    # CHILDREN & ELDERLY SAFETY
    # ===================================================================
    {
        "question": "How do I teach children about phishing?",
        "answer": "Teaching children about phishing: 1) Use age-appropriate language - compare it to stranger danger online, 2) Teach them never to share personal information (name, school, address, photos) with strangers online, 3) Show them examples of phishing emails and messages, 4) Create a rule: always ask a parent before clicking links or downloading anything, 5) Explain that not everything online is true - people can pretend to be anyone, 6) Use interactive cybersecurity games designed for kids, 7) Set up parental controls and safe browsing, 8) Make it a regular conversation, not a one-time talk, 9) Praise them when they come to you with suspicious messages.",
        "category": "demographics",
        "keywords": ["children", "kids", "teach", "young", "child safety", "parental", "family"],
    },
    {
        "question": "How can elderly people stay safe from phishing?",
        "answer": "Helping elderly adults stay safe from phishing: 1) Set up their devices with updated antivirus and spam filters, 2) Teach them the golden rule: never click links in unexpected emails or texts, 3) Help them recognize common scams (tech support, IRS, grandchild in trouble), 4) Create a 'verify first' habit - call the company directly using a known number, 5) Set up two-factor authentication on their accounts, 6) Be patient and non-judgmental - shame prevents reporting, 7) Install a password manager for them, 8) Regularly check in about suspicious contacts, 9) Set up fraud alerts on their financial accounts, 10) Remind them that legitimate organizations never ask for gift card payments.",
        "category": "demographics",
        "keywords": ["elderly", "seniors", "older adults", "grandparents", "aging", "older people"],
    },

    # ===================================================================
    # GREETINGS & META
    # ===================================================================
    {
        "question": "Hello",
        "answer": "Hello! I'm PhishGuard's security education assistant. I can help you learn about phishing attacks, how to identify them, and how to protect yourself online. Here are some things you can ask me about:\n\n- Types of phishing attacks (spear phishing, vishing, smishing)\n- How to spot phishing emails and fake websites\n- What to do if you've been phished\n- Password security and two-factor authentication\n- Social engineering tactics\n- Protecting your organization\n\nWhat would you like to know?",
        "category": "greeting",
        "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy"],
    },
    {
        "question": "Good morning",
        "answer": "Good morning! I'm your PhishGuard security assistant. I'm here to help you learn about phishing and cybersecurity. Feel free to ask me any question about online safety, phishing attacks, or how to protect yourself and your organization from cyber threats!",
        "category": "greeting",
        "keywords": ["good morning", "morning"],
    },
    {
        "question": "Who are you?",
        "answer": "I'm PhishGuard's AI-powered security education assistant! I'm designed to help you learn about phishing attacks, cybersecurity best practices, and online safety. I can answer questions about different types of phishing, help you identify suspicious emails, and provide guidance on what to do if you've been targeted. I'm part of the PhishGuard education platform, and my knowledge is focused specifically on phishing and cybersecurity topics. How can I help you today?",
        "category": "meta",
        "keywords": ["who are you", "what are you", "your name", "introduce", "about you"],
    },
    {
        "question": "What can you help me with?",
        "answer": "I'm PhishGuard's phishing education chatbot! I can help you with:\n\n1) **Understanding phishing** - What it is, how it works, and why it's dangerous\n2) **Types of attacks** - Email phishing, spear phishing, vishing, smishing, whaling, and more\n3) **Identifying threats** - How to spot phishing emails, fake websites, and suspicious links\n4) **Responding to attacks** - What to do if you clicked a phishing link or gave away your password\n5) **Password security** - Strong passwords, 2FA, and password managers\n6) **Social engineering** - Understanding manipulation tactics attackers use\n7) **Prevention** - How to protect yourself, your family, and your organization\n8) **Real-world examples** - Common scam scenarios to watch out for\n\nAsk me anything about phishing and cybersecurity!",
        "category": "meta",
        "keywords": ["help", "what can you do", "capabilities", "features", "assist", "topics"],
    },
    {
        "question": "Thank you",
        "answer": "You're welcome! Remember, staying informed and vigilant is your best defense against phishing attacks. Key takeaways: always verify before you click, use strong unique passwords with 2FA, and don't hesitate to report suspicious messages. If you have more questions about cybersecurity, I'm always here to help. Stay safe online!",
        "category": "meta",
        "keywords": ["thank", "thanks", "appreciate", "grateful", "thank you"],
    },
    {
        "question": "Goodbye",
        "answer": "Goodbye! Stay safe online and remember: when in doubt, don't click! If you ever need help with phishing or cybersecurity questions, feel free to come back anytime. Take care!",
        "category": "meta",
        "keywords": ["goodbye", "bye", "see you", "later", "farewell", "quit", "exit"],
    },
]
