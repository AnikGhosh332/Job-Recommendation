import kagglehub
import os
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("arbazkhan971/allskillandnonskill")

print("Path to dataset files:", path)


files = os.listdir(path)
print("Files in dataset:", files)

skillset_df = []

# If it contains CSVs, you can load them
for f in files:
    if f.endswith(".csv"):
        file_path = os.path.join(path, f)
        print(f"\nPreview of {f}:")
        skillset_df = pd.read_csv(file_path)

print(skillset_df)      


domains = {
    "Cloud": [
        # Cloud providers
        "AWS", "Azure", "GCP", "IBM Cloud", "Oracle Cloud", 
        # DevOps / cloud infra
        "Terraform", "CloudFormation", 
        "Serverless", "CI/CD", "Jenkins", "GitHub Actions",
        "Monitoring", "Prometheus", "Grafana", "CloudWatch"
    ],

    "Machine Learning": [
        # Core ML
         "Reinforcement Learning", "Supervised Learning", "Unsupervised Learning", 
        # Frameworks / libraries
        "TensorFlow", "PyTorch", "scikit-learn", "Keras", "XGBoost", "LightGBM", "CatBoost",
        # NLP / computer vision
        "Transformers", "HuggingFace", "BERT", "GPT", "CNN", "RNN", "YOLO", "OpenCV",
        # MLOps / pipelines
        "MLflow", "DVC", "Kubeflow", "MLOps", "Model Deployment", "Docker", "APIs", "Monitoring", 
        "Hyperparameter Tuning", "Cloud ML Services", "SageMaker", "Vertex AI", "Azure ML"
    ],

    "Data Engineering": [
        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "MS SQL", "Redis", "Elasticsearch", "Cassandra", 
        # ETL / pipelines
        "ETL", "Data Pipeline", "Airflow", "Luigi", "Prefect", "Dagster", 
        # Big data
        "Hadoop", "Spark", "Flink", "Kafka", "Hive", "Pig", 
        # Storage / warehousing
        "Redshift", "BigQuery", "Snowflake", "Delta Lake", 
        # Tools / others
        "Python", "SQL", "Pandas", "NumPy", "DVC", "Data Modeling", "Data Cleaning", "Data Transformation"
    ],

    "Web Development": [
        # Backend frameworks
        "Django", "Flask", "FastAPI", "Spring Boot", "Node.js", "Express.js", "ASP.NET",
        # Frontend frameworks
        "React", "Angular", "Vue.js", "Svelte", "HTML", "CSS", "JavaScript", "TypeScript", "Tailwind", "Bootstrap", "Material UI",
        # Web APIs / services
        "REST API", "GraphQL", "WebSockets", "JSON", "AJAX", "HTTP", 
        # DevOps / deployment
        "Docker", "CI/CD", "AWS EC2", "Heroku", "Netlify", "Vercel", "Nginx", "Apache",
        # Testing / tools
        "Selenium", "Cypress", "Jest", "Mocha", "Unit Testing", "Integration Testing"
    ],

    "Cybersecurity": [
        "Network Security", "Penetration Testing", "OWASP", "Cryptography", "Firewalls", "IDS/IPS", 
        "Vulnerability Assessment", "SIEM", "Malware Analysis", "Authentication", "OAuth", "JWT"
    ],

    "DevOps / SRE": [
        "CI/CD", "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitHub Actions", 
        "Monitoring", "Prometheus", "Grafana", "Load Balancing", "High Availability", "Scaling", 
        "AWS", "GCP", "Azure"
    ],
    
    # New domains for hospitality/bar industry
    "Bartending": [
        "Mixology", "Cocktail Recipes", "Classic Cocktails", "Signature Drinks", 
        "Speed Pouring", "Customer Service", "Drink Presentation", "Event Hosting", 
        "Inventory Management", "Liquor Knowledge", "Wine & Spirits Pairing"
    ],

    "Bar Backing": [
        "Stocking Supplies", "Glassware Cleaning", "Bar Organization", 
        "Assisting Bartenders", "Ice Management", "Keg Handling", "Trash Removal"
    ],

    "Serving": [
        "Order Taking", "Table Service", "Customer Interaction", "Food & Beverage Knowledge",
        "POS Systems", "Upselling Techniques", "Team Coordination", "Complaint Handling"
    ]
} 