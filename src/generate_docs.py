import os

# 1. data/ugc_docs directory එක නැත්නම් සාදාගැනීම
output_dir = "data/ugc_docs"
os.makedirs(output_dir, exist_ok=True)

# 2. UGC Sample Documents 15 (University Admission & Cut-off Data)
ugc_data = {
    "doc_1_colombo_cs.txt": """
    University of Colombo School of Computing (UCSC) - Computer Science (CS)
    Stream: Physical Science / Direct Intake
    Minimum Z-score (Colombo District): 1.8502
    Minimum Z-score (Gampaha District): 1.8410
    Minimum Z-score (Kandy District): 1.8211
    Duration: 3 Years (BSc) / 4 Years (BSc Hons)
    Key Modules: Data Structures, Algorithms, Artificial Intelligence, Database Systems.
    """,
    
    "doc_2_kelaniya_se.txt": """
    University of Kelaniya - Software Engineering (SE)
    Stream: Physical Science
    Minimum Z-score (Colombo District): 1.7210
    Minimum Z-score (Gampaha District): 1.7105
    Duration: 4 Years (BSc Hons)
    Key Modules: Software Architecture, Web Engineering, Mobile Dev, DevOps, Cloud Computing.
    Career Paths: Software Engineer, DevOps Engineer, Systems Architect.
    """,

    "doc_3_moratuwa_cse.txt": """
    University of Moratuwa - Computer Science & Engineering (CSE)
    Stream: Physical Science
    Minimum Z-score (Colombo District): 2.1500
    Minimum Z-score (Gampaha District): 2.1200
    Duration: 4 Years (BSc Eng Hons)
    Key Modules: Computer Systems, Embedded Systems, Machine Learning, Cyber Security.
    """,

    "doc_4_peradeniya_eng.txt": """
    University of Peradeniya - Faculty of Engineering
    Stream: Physical Science
    Minimum Z-score (Kandy District): 1.9120
    Minimum Z-score (Kurunegala District): 1.8900
    Specializations: Civil, Mechanical, Electrical & Electronic, Computer Engineering.
    """,

    "doc_5_japura_applied_math.txt": """
    University of Sri Jayewardenepura - Applied Sciences
    Stream: Physical Science / Mathematics
    Minimum Z-score (Colombo District): 1.4500
    Minimum Z-score (Kalutara District): 1.4200
    Key Subjects: Physics, Chemistry, Mathematics, Statistics, Financial Mathematics.
    """,

    "doc_6_colombo_medicine.txt": """
    University of Colombo - Faculty of Medicine (MBBS)
    Stream: Biological Science
    Minimum Z-score (Colombo District): 2.2100
    Minimum Z-score (Gampaha District): 2.1950
    Duration: 5 Years
    Requirements: A/L Biology, Chemistry, Physics with minimum C grades.
    """,

    "doc_7_japura_management.txt": """
    University of Sri Jayewardenepura - Management Studies & Commerce
    Stream: Commerce
    Minimum Z-score (Colombo District): 1.6800
    Minimum Z-score (Gampaha District): 1.6500
    Specializations: Accounting, Finance, Marketing, Business Administration, HR.
    """,

    "doc_8_kelaniya_translation.txt": """
    University of Kelaniya - Translation Studies
    Stream: Arts / Any Stream
    Minimum Z-score: 1.2000
    Special Requirement: Must pass the Practical / Aptitude Test conducted by Kelaniya University.
    Languages: Sinhala, English, Tamil.
    """,

    "doc_9_moratuwa_architecture.txt": """
    University of Moratuwa - Bachelor of Architecture (B.Arch)
    Stream: Any Stream (Arts / Commerce / Science) with Mathematics
    Minimum Z-score: District Based Cut-offs apply.
    Special Requirement: Mandatory pass in the Architecture Aptitude Test (Moratuwa Test).
    """,

    "doc_10_ruhuna_agri.txt": """
    University of Ruhuna - Faculty of Agriculture
    Stream: Biological Science
    Minimum Z-score (Galle District): 1.1500
    Minimum Z-score (Matara District): 1.1200
    Key Modules: Crop Science, Agri Economics, Food Technology, Animal Science.
    """,

    "doc_11_uva_wellassa_cst.txt": """
    Uva Wellassa University - Computer Science & Technology (CST)
    Stream: Physical Science
    Minimum Z-score (Badulla District): 1.2500
    Minimum Z-score (Colombo District): 1.4100
    Focus: Industry-oriented practical degree with entrepreneurship.
    """,

    "doc_12_wayamba_food_tech.txt": """
    Wayamba University of Sri Lanka - Food Science & Nutrition
    Stream: Biological Science
    Minimum Z-score (Kurunegala District): 1.3100
    Minimum Z-score (Puttalam District): 1.2800
    Career Paths: Food Technologist, Quality Assurance Manager, Nutritionist.
    """,

    "doc_13_rajarata_ict.txt": """
    Rajarata University of Sri Lanka - Information & Communication Technology (BICT)
    Stream: Technology Stream (ET/BST/ICT) or Physical Science
    Minimum Z-score (Anuradhapura District): 1.1800
    Duration: 4 Years Hons Degree.
    """,

    "doc_14_ugc_general_rules.txt": """
    University Grants Commission (UGC) Sri Lanka - General Admission Rules
    Rule 1: Candidates must obtain a minimum of 'C' grades or above in 3 main subjects.
    Rule 2: A minimum score of 30% for Common General Test is mandatory.
    Rule 3: English Language mark is evaluated for specific degree courses.
    """,

    "doc_15_aptitude_test_guidelines.txt": """
    UGC Aptitude Test Guidelines for State Universities
    Courses requiring Aptitude Tests: Architecture, Design, Fashion Design, Information Systems (UCSC), Translation Studies, Sports Science.
    Application Deadline: Usually within 2 weeks of A/L results publication.
    """
}

# 3. Files ලියීම (Writing files)
for file_name, content in ugc_data.items():
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print(f"Successfully created {len(ugc_data)} documents in '{output_dir}' folder!")