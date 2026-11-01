"""Builds a clearly-labelled SYNTHETIC test dataset (no real people, no scraping)."""
import json, random
random.seed(7)
F="Aarav Ananya Rohit Meera Sanjay Kavita Vikram Neha Arjun Priya Rahul Sunita Imran Farah Deepak Shalini Manish Pooja Karan Anjali Suresh Lata Nitin Ritu Amit Divya Harish Geeta Naveen Smita".split()
LN="Sharma Verma Iyer Nair Kapoor Mehta Rao Banerjee Gupta Singh Joshi Menon Khan Reddy Chatterjee Bhatt Das Malhotra Pillai Saxena Tripathi Mishra Agarwal Kulkarni".split()
CITY=["Lucknow, India","Delhi NCR, India","Mumbai, India","Bengaluru, India","Pune, India","Jaipur, India","Hyderabad, India","Kolkata, India","Chennai, India","Dubai, UAE"]
A={ # key: (label, roles, orgs, summaries, experience)
"consultant":(1,["Education Consultant","School Improvement Advisor","Independent Academic Advisor","School Accreditation Consultant","Curriculum Consultant"],
 ["{L} Education Advisory","Independent","Pragya Learning Partners","Shikshak Consulting"],
 ["Works with {n}+ K-12 schools on academic quality, teacher training and affiliation readiness. Trusted by school owners and principals across states.",
  "Advisor to school management teams on curriculum, accreditation and school audits. {y} years in school education.",
  "Helps trustees and promoters set up academic systems, with engagements across {n} schools in CBSE, ICSE and IGCSE boards."],
 ["Led academic audits for {n} schools","Former Vice Principal, CBSE school","Mentored first-time principals and school directors"]),
"ex_leader":(1,["Former Principal","Retired School Director","Former Headmaster","Ex-Head of School","Principal Emeritus & Education Mentor"],
 ["Independent","Advisory board member, school trust","Retired","{L} Education Society"],
 ["Served {y} years as principal of leading CBSE schools; now sits on school boards and advises management on leadership hiring.",
  "Former school director who built academic teams at {n} schools. Mentors principals and trustees.",
  "Retired headmaster, {y} years in K-12. Advisor to school trusts and owners on governance and school improvement."],
 ["Principal, CBSE school, {y} years","Board member, school education trust","Guest speaker at principals conferences"]),
"entrepreneur":(1,["Founder & Chairman","Co-founder, Schools","Managing Trustee","School Owner & Director","Founder, School Chain"],
 ["{L} Group of Schools","{L} Education Trust","Little Scholars Network","Vidyalaya Ventures"],
 ["Founded a group of {n} schools across tier-2 cities. Works closely with trustees, principals and other school owners.",
  "Education entrepreneur; launched and scaled {n} K-12 schools and an association of independent school owners.",
  "Managing trustee of a school trust running {n} schools; advises first-time school founders."],
 ["Founded {n} schools","Chair, association of private school owners","Raised funding to expand school network"]),
"network":(1,["Regional Director, School Network","Head of Academics, School Group","COO, Schools","Cluster Head, Schools"],
 ["Bharat Schools Network","Vidya Group of Schools","Orchid Learning Schools","Gyan Education Group"],
 ["Oversees a network of {n} schools, coordinating principals, academics and operations across regions.",
  "Leads academics for a school group with {n} campuses; works with owners, trustees and principals on rollout.",
  "{y} years managing multi-campus school operations and principal development."],
 ["Managed {n} school campuses","Principal development programme lead","Reported to group trustees"]),
"connector":(1,["Business Development Manager, Schools","Education Partnerships Lead","Head of School Relations","Regional Manager, School Sales"],
 ["LearnSphere (EdTech)","Praxis Books","Gurukul Tech","Scholar Publishing"],
 ["Works with principals, owners and management of {n}+ schools on curriculum and technology adoption; strong relationships with school decision-makers.",
  "Builds partnerships with school groups and trustees; {y} years selling to K-12 school leadership.",
  "Regional lead covering {n} schools; trusted contact for principals and school promoters."],
 ["Onboarded {n} schools","Organised principal roundtables","Key accounts: school groups"]),
"software":(0,["Software Engineer","Backend Developer","Data Scientist","DevOps Engineer"],["TechNova","CloudKart","Infrabyte"],
 ["Builds scalable APIs and data pipelines in Python and Go. {y} years in fintech and e-commerce.","Machine learning engineer working on recommendation systems."],["Led migration to microservices","Mentored junior engineers"]),
"retail":(0,["Retail Store Manager","Regional Sales Head","Operations Manager"],["MegaMart","FreshBasket","StyleHub"],
 ["Manages {n} retail stores, focused on sales targets, inventory and customer experience.","{y} years in FMCG distribution and retail operations."],["Opened {n} new stores","Reduced shrinkage by 12%"]),
"marketing":(0,["Digital Marketing Manager","Brand Strategist","Growth Marketer"],["AdWave","BrandCraft"],
 ["Performance marketing and brand campaigns for consumer apps. {y} years in digital.","Runs paid acquisition and SEO for D2C brands."],["Scaled paid channels","Launched brand campaign"]),
"recruiter":(0,["HR Business Partner","Talent Acquisition Lead","Technical Recruiter"],["PeopleFirst","TalentBridge"],
 ["Hires engineers and managers for IT companies; {y} years in talent acquisition.","HR partner for manufacturing, handling payroll and policy."],["Hired {n} engineers","Built employer brand"]),
"corp_trainer":(0,["Corporate Trainer","L&D Manager","Leadership Coach, Corporate"],["Skillset Corporate","LeadWell"],
 ["Soft-skills and leadership workshops for corporate managers; management and sales training.","{y} years in corporate learning and development at IT firms."],["Trained {n} corporate managers","Designed onboarding programme"]),
"professor":(0,["Professor, Business School","Lecturer, Law School","Research Scholar, Engineering"],["{L} Business School","National Law School","Institute of Technology"],
 ["Teaches finance and strategy at a business school; research on capital markets.","Academic in law school focused on constitutional research and publications."],["Published {n} papers","PhD supervisor"]),
"teacher":(0,["Classroom Teacher","Mathematics Teacher","English Teacher","Primary Teacher"],["Government school","City Public School"],
 ["Teaches grade 8 mathematics at a school; enjoys classroom activities and student projects.","{y} years teaching English to primary school students."],["Class teacher","Organised school annual day"]),
}
COUNT={k:(8 if v[0] else 5) for k,v in A.items()}
combos=[(f,l) for f in F for l in LN]; random.shuffle(combos); ci=0
def make(key, pid):
    global ci
    lab,roles,orgs,sums,exp=A[key]; f,l=combos[ci]; ci+=1
    d=dict(n=random.choice([4,6,8,12,15,20,25,30]),y=random.randint(8,28),L=l)
    role=random.choice(roles); org=random.choice(orgs).format(**d); s=random.choice(sums).format(**d)
    return dict(id=pid,name=f"{f} {l}",url=f"https://example.org/synthetic-test-profile/{f.lower()}-{l.lower()}",
      headline=f"{role} | {org}",role=role,org=org,location=random.choice(CITY),summary=s,
      experience=[e.format(**d) for e in random.sample(exp,2)],archetype=key,gt=lab)
ref=make("consultant","REF"); ref.update(name="Test Reference (synthetic)",role="Education Consultant & Former Principal",
 org="Independent",headline="Education Consultant | Former Principal | Advisor to 30+ schools",
 summary="Former principal with 22 years in K-12 school education. Now advises 30+ schools on academic quality, accreditation and school improvement; mentors principals, trustees and school owners across several states.",
 experience=["Principal, CBSE school, 12 years","Led academic audits for 30 schools","Board member, school education trust"])
profs=[make(k,"x") for k in A for _ in range(COUNT[k])]
random.shuffle(profs)
for i,p in enumerate(profs): p["id"]=f"P{i:03d}"
json.dump(dict(note="SYNTHETIC TEST DATASET - fictional people, not LinkedIn data.",reference=ref,profiles=profs),open("data/profiles.json","w"),indent=1)
print(len(profs),"profiles")
