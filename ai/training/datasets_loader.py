"""
Curated Training & Benchmark Dataset for AI ScamShield.
Contains realistic scam/phishing patterns and legitimate control messages.
"""

import pandas as pd
import numpy as np

# 1. Real-world scam messages across major fraud taxonomies
SCAM_MESSAGES = [
    # Bank & KYC Scams
    ("Dear SBI user, your net banking will be deactivated today. Click http://sbi-kyc-update.xyz to update Aadhaar/PAN immediately.", "bank_kyc"),
    ("URGENT: Your HDFC bank account is blocked due to unverified KYC. Click http://hdfc-netverify.top to prevent permanent closure.", "bank_kyc"),
    ("ICICI Alert: Your credit card reward points worth Rs 9,850 will expire tonight. Redeem cash directly to your account at http://icici-rewards.online", "bank_kyc"),
    ("Dear Customer, your bank account is suspended for suspicious activity. Complete KYC verification within 24 hours at http://secure-bank-update.info", "bank_kyc"),
    ("Axis Bank Notice: Pan Card not linked to Account 4829. Your account will be restricted today. Update here: http://axis-panlink.cc", "bank_kyc"),
    ("Attention: ₹15,000 debited from your account. If you did not authorize this, click http://cancel-txn-alert.co to freeze transaction immediately.", "bank_kyc"),
    ("Dear customer, your PNB debit card is blocked. Kindly click http://pnb-card-reactivate.xyz to verify your 16 digit card number and CVV.", "bank_kyc"),
    ("Your Bank A/C has been locked by RBI directives. Pay verification fee of Rs 50 at http://rbi-verify-portal.top to unlock.", "bank_kyc"),
    ("Dear SBI customer, your YONO account is locked today. Update your pan card immediately on http://yono-kyc-login.click", "bank_kyc"),
    ("Bank Alert: Unauthorized attempt to change mobile number on your Kotak account. Stop this change immediately: http://kotak-security-halt.cc", "bank_kyc"),

    # Electricity / Utility Scams
    ("Dear Consumer, your electricity power will be disconnected tonight at 9:30 PM because previous month bill was not updated. Contact Electricity Officer at 9876543210 immediately.", "utility"),
    ("Electricity Department Alert: Urgent notice! Your power supply will be cut off in 2 hours. Call power manager Sharma at 9123456789 to pay overdue bill.", "utility"),
    ("BSES Power Alert: Unpaid bill of Rs 3,420 pending. Power disconnection scheduled at 8:00 PM. Call our bill desk at 8877665544 now.", "utility"),
    ("Torrent Power: Connection #98420 will be suspended tonight at 9 PM. Call helpline 9988771122 to avoid blackout.", "utility"),
    ("Gas Connection Notice: Your Indane LPG subscription is paused due to Aadhaar non-compliance. Call 9012345678 to update before service cutoff.", "utility"),
    ("Mahanagar Gas Alert: Your gas pipeline meter will be disconnected today. Pay pending fee of Rs 850 immediately via link: http://mgl-paybill.xyz", "utility"),

    # Delivery & Parcel Scams
    ("India Post: Your parcel IND93821 cannot be delivered due to incomplete address. Please update your address and pay Rs 25 redelivery fee at http://indiapost-update.top", "delivery"),
    ("FedEx Delivery Alert: Shipment #FX99214 on hold at customs. Pay clearance tax of Rs 49 within 12 hours: http://fedex-customs-track.site", "delivery"),
    ("BlueDart Express: Delivery attempt failed for package #BD7842. Update delivery preferences and pay redelivery charges: http://bluedart-reschedule.click", "delivery"),
    ("DHL Express: Package #920184 delivery fee unpaid. Click http://dhl-parcel-release.me to settle invoice and receive delivery tomorrow.", "delivery"),
    ("Amazon Logistics: Courier could not reach your home. Confirm delivery location and pay ₹10 reschedule fee: http://amzn-deliv-loc.pw", "delivery"),
    ("DTDC Courier: Your document parcel is held at depot. Final warning before return to sender. Pay Rs 15 at http://dtdc-redeliver.online", "delivery"),

    # Job & Work-From-Home / Part-Time Scams
    ("Earn ₹3000 to ₹8000 daily by simply liking YouTube videos and rating hotels on Google Maps. No experience needed. Join Telegram: t.me/daily_cash_jobs", "fake_job"),
    ("Amazon is hiring Part-Time / Full-Time product reviewers! Work 1-2 hours from home, earn Rs 50,000/month. WhatsApp your resume to 9876501234 now.", "fake_job"),
    ("Flipkart Part-time Job Offer: Daily payout of Rs 2500 for order processing tasks. Registration closing soon. Contact HR Priya on Telegram: @FlipkartHR_Priya", "fake_job"),
    ("Work From Home Opportunity: Simple copy-paste jobs, typing projects. Daily income ₹1500 - ₹5000 directly to UPI. WhatsApp 'JOB' to 9112233445.", "fake_job"),
    ("Congratulations! You have been shortlisted for International Data Entry Operator. Monthly salary ₹65,000. Deposit ₹1,500 laptop insurance fee to begin.", "fake_job"),
    ("Google India remote vacancy: Earn Rs 4500 per day by reviewing websites. Free registration. Message recruiter at wa.me/919988001122", "fake_job"),

    # Lottery, Prize & KBC Scams
    ("CONGRATULATIONS! Your mobile number won 1st prize of Rs 25,00,000 in KBC WhatsApp Lucky Draw 2026. Contact KBC Manager Rana Pratap on WhatsApp 9811223344.", "lottery"),
    ("Dear User, your mobile number has won a brand new Tata Safari car in Diwali Mega Lucky Contest. Call lottery officer at 9765432100 to claim prize.", "lottery"),
    ("Shoppers Stop Mega Win: You have been selected to win iPhone 16 Pro Max for just Rs 99 shipping fee! Claim before timer expires: http://claim-apple-gift.top", "lottery"),
    ("WhatsApp Lottery Bureau London: Your number won £500,000 in international promo. Send your full name, bank details, and passport copy to claim.", "lottery"),
    ("Flipkart Lucky Winner: Spin & Win Rs 50,000 gift card! Click http://flipkart-spinwheel-lucky.xyz and enter your UPI PIN to claim reward.", "lottery"),

    # Loan & Quick Credit Scams
    ("Instant Pre-Approved Personal Loan of ₹5,00,000 at 1% interest rate without CIBIL score! Download loan app immediately: http://quick-cash-loan.apk", "loan"),
    ("Dhani Loan Approval: Rs 3,00,000 loan approved. Pay processing fee of Rs 1,999 to bank account to release loan amount within 15 minutes.", "loan"),
    ("Bajaj Finance: Instant 0% EMI loan ready for disbursement. Install our official verification app from http://bajaj-fastloan.online", "loan"),
    ("Need cash urgently? Get instant Rs 50,000 in your bank account in 2 minutes without document check. Click http://fast-rupee-loan.click", "loan"),

    # Impersonation & Fear / Legal Threats
    ("Cyber Crime Police Branch Notice: A cyber pornography and illegal money transfer case has been registered against you. Pay settlement fine or police will arrest you in 2 hours.", "police_threat"),
    ("Income Tax Department Notice: Tax evasion inquiry initiated on PAN. Penalty of Rs 50,000 pending. Pay online immediately to avoid prosecution: http://incometax-settle.top", "police_threat"),
    ("CBI Notice: Urgent inquiry into suspicious transactions. Join mandatory interrogation video call immediately or face immediate non-bailable warrant.", "police_threat"),
    ("Telecom Authority TRAI: Your SIM card will be permanently blocked in 24 hours for illegal marketing complaints. Dial 9 to connect with verification officer.", "police_threat"),

    # Customer Support & Refund Impersonation
    ("Paytm Customer Care: Your pending cashback of Rs 4,999 could not be credited. Enter your UPI PIN on http://paytm-refund-claim.cc to receive money.", "refund"),
    ("PhonePe Support: Refund failed for order #7819. Share the 6 digit OTP received on your phone to credit money directly to your wallet.", "refund"),
    ("Google Pay Alert: Scratch card reward worth ₹3,500 is waiting for you. Click link and enter your UPI PIN to transfer money into your account.", "refund"),
    ("Netflix Account Suspended: Your subscription payment failed. Update billing information within 24 hours to keep streaming: http://netflix-billing-renew.xyz", "refund"),
]

# 2. Legitimate Everyday Control Messages (Normal Messages - Low Risk)
LEGITIMATE_MESSAGES = [
    # E-Commerce & Deliveries
    ("Your Amazon order #402-9182301 has been dispatched with delivery partner ATS. Track your package on your Amazon mobile app.", "ecommerce"),
    ("Your package from Flipkart has been delivered to your doorstep. Thank you for shopping with us.", "ecommerce"),
    ("Swiggy: Your order from Chai Point is on the way! Delivery partner Ramesh is arriving in 12 minutes.", "delivery"),
    ("Zomato: Delivery executive has arrived at your location with your food. Please collect your order.", "delivery"),
    ("Blinkit: Order #BL8291 delivered successfully in 9 minutes. Hope you enjoyed the quick delivery!", "delivery"),
    ("BlueDart tracking: Shipment 9823101 has arrived at Bangalore Hub and is out for delivery today.", "delivery"),
    ("Your Myntra package containing 2 items is expected to be delivered by Thursday, 5 PM.", "ecommerce"),
    ("Uber: Your driver Harish is arriving in a White Swift Dzire (KA01AB1234). PIN is 4821.", "ride"),
    ("Ola: Your cab is arriving in 4 mins. Share OTP 7412 with your driver to start your ride.", "ride"),

    # Bank & Financial Updates (Normal Transactional, NO deceptive links)
    ("Your SBI Account XX4829 is debited by INR 650.00 on 04-Sep-26 at Grocery Store. Avl Bal: INR 18,420.00. Report fraud: 1800112211.", "bank_normal"),
    ("HDFC Bank Alert: Salary of INR 85,000.00 credited to Account ending 1204 on 01-Sep. Net available balance: INR 94,210.00.", "bank_normal"),
    ("ICICI Bank: INR 2,500.00 withdrawn from ATM at MG Road on 03-Sep. Available balance INR 32,100.00. If not done by you, SMS BLOCK to 92156.", "bank_normal"),
    ("Axis Bank: Statement for Credit Card ending 9012 for the period Aug 2026 is generated. Total due: INR 4,210. Due date: 20-Sep-26.", "bank_normal"),
    ("PhonePe: You paid ₹120 to Café Coffee Day. Transaction ID: T260904123456.", "payment_normal"),
    ("Google Pay: You received ₹500 from Rohit Sharma for 'Dinner bill split'.", "payment_normal"),

    # Standard OTPs (Safe, no deceptive link/threat)
    ("849201 is your secret OTP to login to Netflix. Do not share this OTP with anyone, including customer support.", "otp_normal"),
    ("291048 is your verification code for Swiggy account login. Valid for 10 minutes.", "otp_normal"),
    ("Your WhatsApp verification code is 492-184. You can also tap this link to verify your phone: v.whatsapp.com/492184", "otp_normal"),
    ("Do not share: 928310 is your OTP for transaction of INR 350.00 on Zepto with HDFC Bank Card ending 8219.", "otp_normal"),

    # Everyday Personal & Social Messages
    ("Hey, are we still meeting for lunch at 1 PM today near the office?", "chat"),
    ("Can you please pick up some bread and eggs on your way back home?", "chat"),
    ("Happy Birthday! Wishing you a fantastic year ahead filled with joy and success.", "chat"),
    ("I have sent you the project presentation via email. Please check and let me know your thoughts.", "chat"),
    ("Running about 10 minutes late due to traffic, see you soon!", "chat"),
    ("Mom called earlier, she asked if you can call her back when you get free.", "chat"),
    ("Team meeting rescheduled to tomorrow at 11 AM. Link is on Google Calendar.", "chat"),
    ("Did you get a chance to review the pull request for the new authentication module?", "chat"),
    ("Flight 6E-204 to Mumbai is on schedule. Boarding begins at Gate 14 at 16:45.", "travel"),
    ("IRCTC: PNR 2849102948 is Confirmed. Coach B2, Berth 35. Train 12952 departs at 17:00.", "travel"),
]

def generate_augmented_dataset(target_samples=1200):
    """
    Expands the benchmark base corpus using realistic lexical variations,
    amounts, banks, phone numbers, and URLs while strictly maintaining label semantics.
    """
    np.random.seed(42)
    
    banks = ["SBI", "HDFC", "ICICI", "Axis Bank", "PNB", "Kotak", "Bank of Baroda", "Canara Bank"]
    scam_tlds = [".xyz", ".top", ".click", ".site", ".info", ".cc", ".me", ".pw", ".online"]
    scam_domains = ["kyc-update", "secure-verify", "account-reactivate", "netbank-login", "reward-claim", "pan-link"]
    urgency_phrases = ["within 24 hours", "today immediately", "before 9 PM tonight", "to avoid permanent blocking", "or card will be deactivated"]
    amounts = ["₹4,999", "₹12,500", "₹25,000", "Rs 15,000", "Rs 50,000", "Rs 2,50,000", "₹25 Lakhs"]
    legit_merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Blinkit", "Zepto", "Myntra", "Uber", "Ola"]
    
    augmented_rows = []
    
    # 1. Base samples
    for text, cat in SCAM_MESSAGES:
        augmented_rows.append({"text": text, "label": 1, "category": cat})
        
    for text, cat in LEGITIMATE_MESSAGES:
        augmented_rows.append({"text": text, "label": 0, "category": cat})

    # 2. Augment Scam Samples
    while sum(1 for r in augmented_rows if r["label"] == 1) < (target_samples // 2):
        scam_type = np.random.choice(["bank", "utility", "job", "delivery", "lottery", "threat", "refund"])
        bank = np.random.choice(banks)
        tld = np.random.choice(scam_tlds)
        domain = np.random.choice(scam_domains)
        urgency = np.random.choice(urgency_phrases)
        amt = np.random.choice(amounts)
        phone = f"9{np.random.randint(100000000, 999999999)}"
        acct_num = np.random.randint(1000, 9999)
        
        if scam_type == "bank":
            msg = f"Alert from {bank}: Your account {acct_num} is restricted. Update your KYC {urgency} at http://{bank.lower().replace(' ', '')}-{domain}{tld}."
            augmented_rows.append({"text": msg, "label": 1, "category": "bank_kyc"})
        elif scam_type == "utility":
            hour = np.random.choice(["8:00 PM", "9:30 PM", "10:00 PM", "midnight"])
            msg = f"Dear consumer, power supply will be cut off tonight at {hour} for non-payment of electricity bill. Call electricity desk {phone} immediately."
            augmented_rows.append({"text": msg, "label": 1, "category": "utility"})
        elif scam_type == "job":
            daily_pay = np.random.choice(["₹2,500", "₹4,000", "₹6,000", "₹8,500"])
            msg = f"Work from home daily! Earn {daily_pay} by rating movies and products online. No fee. Contact manager on WhatsApp {phone}."
            augmented_rows.append({"text": msg, "label": 1, "category": "fake_job"})
        elif scam_type == "delivery":
            fee = np.random.choice(["Rs 19", "Rs 25", "Rs 35", "Rs 49", "₹10"])
            courier = np.random.choice(["India Post", "FedEx", "DHL", "BlueDart", "Delhivery"])
            msg = f"{courier}: Package delivery paused due to incomplete home address. Pay {fee} redelivery fee at http://{courier.lower().replace(' ', '')}-reschedule{tld}"
            augmented_rows.append({"text": msg, "label": 1, "category": "delivery"})
        elif scam_type == "lottery":
            prize = np.random.choice(["₹25,00,000", "₹50,00,000", "1 Crore", "Tata Harrier SUV"])
            msg = f"Congratulations! Your mobile number won {prize} in nationwide lucky draw! Call manager at {phone} to claim your prize."
            augmented_rows.append({"text": msg, "label": 1, "category": "lottery"})
        elif scam_type == "threat":
            dept = np.random.choice(["Cyber Cell", "Police Crime Branch", "CBI Investigation", "Telecom Authority"])
            msg = f"Urgent notice from {dept}: Legal case registered under your ID. Call investigation officer {phone} within 2 hours to avoid arrest."
            augmented_rows.append({"text": msg, "label": 1, "category": "police_threat"})
        elif scam_type == "refund":
            service = np.random.choice(["PhonePe", "Paytm", "Google Pay", "Amazon Pay"])
            msg = f"{service}: Pending refund of {amt} failed. Complete OTP verification at http://{service.lower().replace(' ', '')}-refund{tld} to credit money."
            augmented_rows.append({"text": msg, "label": 1, "category": "refund"})

    # 3. Augment Legitimate Samples
    while sum(1 for r in augmented_rows if r["label"] == 0) < target_samples:
        legit_type = np.random.choice(["bank_tx", "otp", "order", "chat", "travel"])
        merchant = np.random.choice(legit_merchants)
        bank = np.random.choice(banks)
        otp = np.random.randint(100000, 999999)
        acct_num = np.random.randint(1000, 9999)
        debit_amt = np.random.choice(["150.00", "420.00", "890.00", "1,250.00", "2,499.00", "45.00"])
        order_id = np.random.randint(100000, 999999)
        
        if legit_type == "bank_tx":
            bal = np.random.randint(5000, 85000)
            msg = f"Your {bank} Account XX{acct_num} is debited by INR {debit_amt} at {merchant}. Avl Bal: INR {bal:,.2f}. Report unauthorized: 1800112211."
            augmented_rows.append({"text": msg, "label": 0, "category": "bank_normal"})
        elif legit_type == "otp":
            service = np.random.choice(["Uber", "Swiggy", "Zomato", "IRCTC", "Myntra", "Amazon", "WhatsApp"])
            msg = f"{otp} is your secret one time password (OTP) for logging into {service}. Valid for 5 minutes. Do not share with anyone."
            augmented_rows.append({"text": msg, "label": 0, "category": "otp_normal"})
        elif legit_type == "order":
            msg = f"Your order #{order_id} from {merchant} has been dispatched. Track in your app or thank your delivery agent."
            augmented_rows.append({"text": msg, "label": 0, "category": "ecommerce"})
        elif legit_type == "chat":
            friend_msgs = [
                "Hey, let's catch up this weekend. Are you free on Saturday?",
                "Can you share the lecture notes from today's session?",
                "Thanks for the help yesterday, really appreciate it!",
                "Have you booked the movie tickets for tonight?",
                "See you in 15 minutes at the office cafeteria.",
                "Did you check out that new coffee shop down the street?",
                "Let me know once you reach home safely.",
                "Happy anniversary to you both! Have an amazing celebration."
            ]
            msg = np.random.choice(friend_msgs)
            augmented_rows.append({"text": msg, "label": 0, "category": "chat"})
        elif legit_type == "travel":
            pnr = np.random.randint(100000000, 999999999)
            coach = np.random.choice(["B1", "B2", "B3", "A1", "S4", "S5"])
            berth = np.random.randint(1, 72)
            msg = f"IRCTC: PNR {pnr} confirmed. Coach {coach}, Berth {berth}. Please carry a valid original photo ID during travel."
            augmented_rows.append({"text": msg, "label": 0, "category": "travel"})

    df = pd.DataFrame(augmented_rows)
    # Shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = generate_augmented_dataset(target_samples=1200)
    print(f"Generated dataset with {len(df)} samples.")
    print("Class distribution:\n", df["label"].value_counts())
    print("\nCategory distribution:\n", df["category"].value_counts())
    
    # Save to disk
    df.to_csv("ai/data/training_dataset.csv", index=False)
    print("Saved dataset to ai/data/training_dataset.csv")
