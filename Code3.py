import random
import os
import fitz  # PyMuPDF
import csv

# Sous-catégories pour les Universités
UNIVERSITES_SOUS_CATEGORIES =TOP_100_UNIS = [
    # Liste des universités
    "harvard", "mit", "stanford", "oxford", "cambridge", "caltech", "university of chicago", "princeton",
    "columbia", "yale", "uc berkeley", "penn", "imperial college london", "university of california los angeles",
    "university of toronto", "university of california san diego", "eth zurich", "university of michigan",
    "university of california berkeley", "university of london", "cornell", "duke", "northwestern",
    "university of edinburgh", "university of melbourne", "university of hong kong", "university of manchester",
    "university of sydney", "university of oxford", "university of cambridge", "university of california santa barbara",
    "university of washington", "university of california san francisco", "university of illinois urbana champaign",
    "university of california davis", "university of california irvine", "university of north carolina", 
    "university of wisconsin madison", "university of california riverside", "university of florida", 
    "georgia tech", "brown", "university of bristol", "university of copenhagen", "university of amsterdam", 
    "university of zurich", "university of new york", "university of edinburgh", "swiss federal institute of technology",
    "university of tokyo", "university of melbourne", "university of cape town", "university of paris",
    "university of singapore", "university of munich", "tshwane university of technology", "university of cape town", 
    "the australian national university", "sofia university", "nanjing university", "shanghai jiao tong university",
    "hanyang university", "the university of sheffield", "nanyang technological university", "university of manchester",
    "university of copenhagen", "new york university", "university of pretoria", "university of osnabrück"
]

# Sous-catégories pour STEM
STEM_SOUS_CATEGORIES = [
    "hard sciences", "applied sciences", "computer engineering", "life sciences", 
    "pure sciences", "quantitative sciences", "data engineering", "advanced computing", 
    "biotechnology", "pharmaceutical sciences", "environmental engineering", "medical sciences"
]

# Sous-catégories pour les Nouvelles Catégories (EXTRA_CATEGORIES)
EXTRA_CATEGORIES_SOUS_CATEGORIES = {
    "communication": ["corporate communication", "digital communication", "public relations", "media relations"],
    "marketing": ["digital marketing", "content marketing", "brand management", "market research", "social media marketing"],
    "digital": ["web development", "digital transformation", "IT management", "cloud computing"],
    "human resources": ["recruitment", "employee relations", "talent management", "HR management", "organizational development"],
    "finance": ["corporate finance", "investment banking", "financial analysis", "wealth management", "accounting", "financial modeling"],
    "arts": ["visual arts", "performing arts", "fine arts", "arts administration"],
    "literature": ["creative writing", "poetry", "fiction", "non-fiction", "literary criticism", "comparative literature"],
    "political science": ["international relations", "political theory", "public policy", "governance", "political analysis"],
    "architecture": ["urban planning", "landscape architecture", "sustainable design", "building design", "structural engineering"],
    "history": ["ancient history", "modern history", "historical research", "cultural history", "political history"],
    "philosophy": ["ethics", "metaphysics", "logic", "epistemology", "political philosophy"],
    "linguistics": ["phonetics", "syntax", "semantics", "sociolinguistics", "language acquisition"],
    "law": ["corporate law", "international law", "criminal law", "civil law", "legal research", "law enforcement"],
    "management": ["strategic management", "operations management", "project management", "change management"],
    "public relations": ["crisis communication", "media relations", "branding", "public image management"],
    "education": ["education management", "curriculum development", "special education", "educational psychology"],
    "design": ["graphic design", "industrial design", "fashion design", "product design", "UI/UX design"],
    "journalism": ["news reporting", "investigative journalism", "broadcast journalism", "print journalism", "digital journalism"],
    "consulting": ["management consulting", "strategy consulting", "financial consulting", "business consulting"],
    "hospitality": ["hotel management", "tourism management", "event planning", "restaurant management"],
    "social sciences": ["sociology", "psychology", "anthropology", "economics", "political science"],
    "environmental management": ["environmental policy", "sustainability", "climate change", "conservation biology"],
    "international relations": ["global politics", "foreign policy", "international organizations", "diplomacy"],
    "public health": ["epidemiology", "health policy", "global health", "health systems management"],
    "urban planning": ["urban design", "city planning", "transportation planning", "land use planning"],
    "fashion": ["fashion design", "fashion marketing", "textiles", "fashion history"],
    "public policy": ["policy analysis", "public administration", "political strategy", "social policy"],
    "real estate": ["real estate management", "property development", "real estate investment", "urban development"],
    "sports management": ["sports marketing", "sports management", "event management", "athletic coaching"],
    "media": ["media studies", "media production", "broadcasting", "journalism"],
    "economics": ["microeconomics", "macroeconomics", "econometric analysis", "financial economics"],
    "museum studies": ["museum curation", "cultural heritage", "exhibition design", "archaeology", "museum management"],
    "graphic design": ["branding", "visual communication", "digital design", "web design", "typography"],
    "video production": ["filmmaking", "cinematography", "video editing", "sound design", "directing"],
    "music production": ["audio engineering", "music composition", "sound mixing", "musical performance"],
    "web design": ["HTML/CSS", "UX/UI design", "web development", "responsive design", "JavaScript"],
    "business development": ["sales strategy", "market analysis", "business partnerships", "client relations"],
    "product management": ["product strategy", "product lifecycle", "user research", "agile methodology"]
}

# Sous-catégories pour les Langues
LANGUAGES_SOUS_CATEGORIES = {
    "french": ["native", "fluent", "intermediate", "basic"],
    "italian": ["native", "fluent", "intermediate", "basic"],
    "spanish": ["native", "fluent", "intermediate", "basic"],
    "english": ["native", "fluent", "intermediate", "basic"]
}

# Sous-catégories pour l'Expérience
EXPERIENCE_SOUS_CATEGORIES = {
    "intern": ["summer intern", "research intern", "industry intern", "non-profit intern"],
    "internship": ["summer internship", "research internship", "management internship"],
    "research assistant": ["lab assistant", "research fellow", "project assistant"],
    "industry": ["engineering industry", "finance industry", "healthcare industry", "IT industry", "consulting industry"],
    "freelance": ["freelance designer", "freelance developer", "freelance writer", "freelance photographer"],
    "consultant": ["business consultant", "IT consultant", "management consultant", "financial consultant"],
    "part-time job": ["part-time teacher", "part-time receptionist", "part-time cashier", "part-time data entry"],
    "summer job": ["summer camp counselor", "summer retail assistant", "summer internship"],
    "consultant": ["management consultant", "technical consultant", "financial consultant"],
    "team leader": ["project manager", "group coordinator", "team supervisor"],
    "entrepreneur": ["startup founder", "business owner", "founder & CEO"],
    "founder": ["startup founder", "entrepreneur", "founder of a company"],
    "business development": ["sales strategy", "business growth", "market research"],
    "data analyst": ["data scientist", "business analyst", "data engineer", "data consultant"],
    "software engineer": ["backend developer", "frontend developer", "full-stack developer", "software architect"],
    "research scientist": ["biotech researcher", "clinical researcher", "research associate"],
    "laboratory technician": ["lab assistant", "research assistant", "clinical technician"],
    "customer service": ["call center agent", "customer support specialist", "client relations"],
    "sales associate": ["retail associate", "sales representative", "customer service agent"],
    "volunteer": ["community volunteer", "non-profit volunteer", "volunteer coordinator"],
    "project manager": ["project lead", "project coordinator", "program manager"],
    "scientific advisor": ["research advisor", "scientific consultant", "technical advisor"]
}

# Sous-catégories pour les niveaux d'éducation
LEVELS_SOUS_CATEGORIES = {
    "undergraduate": ["bachelor's", "undergrad", "associate's degree", "college student"],
    "graduate": ["master's", "graduate student", "graduate diploma", "postgraduate studies"],
    "phd": ["PhD", "doctoral student", "doctoral research", "postdoctoral research"],
    "postdoc": ["postdoctoral fellow", "postdoctoral research", "research associate"],
    "professional": ["MBA", "executive education", "professional certification", "specialized diploma"],
    "high_school": ["high school diploma", "secondary school", "high school graduate"]
}


# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = " ".join(page.get_text() for page in doc).lower()  # Extraire tout le texte et le mettre en minuscules
    return text


# Calculer le score de profondeur
def calculate_depth_score(cv_text, depth_category, depth_keywords, penalty=None):
    score = 0
    for keyword in depth_keywords:
        if keyword.lower() in cv_text.lower():
            score += 1  # Ajouter un point pour chaque mot-clé trouvé
    if penalty:
        score += penalty  # Appliquer la pénalité si elle existe
    return score


# Fonction principale pour classer les CVs
def algii(cvs, k, cvs_names, max_depth=40):
    scores = {i: [] for i in range(len(cvs))}  # Dictionnaire pour stocker les scores à chaque profondeur
    rankings = {i: [] for i in range(len(cvs))}  # Dictionnaire pour stocker les classements à chaque profondeur

    # Appliquer l'algorithme à chaque profondeur
    for depth in range(max_depth):
        # Définir les mots-clés pour chaque profondeur
        if depth == 0:
            depth_category = "university"
            depth_keywords = TOP_100_UNIS
        elif depth == 1:
            depth_category = "sector"
            depth_keywords = STEM_SOUS_CATEGORIES + EXTRA_CATEGORIES_SOUS_CATEGORIES  # Ajouter les nouvelles catégories
        elif depth == 2:
            depth_category = "languages"
            depth_keywords = LANGUAGES_SOUS_CATEGORIES
        elif depth == 3:
            depth_category = "experience"
            depth_keywords = EXPERIENCE_SOUS_CATEGORIES
        elif depth == 4:
            depth_category = "education"
            depth_keywords = LEVELS_SOUS_CATEGORIES["undergraduate"] + LEVELS_SOUS_CATEGORIES["graduate"] + LEVELS_SOUS_CATEGORIES["phd"] + LEVELS_SOUS_CATEGORIES["postdoc"]
        else:
            depth_category = f"extra_depth_{depth}"  # Nouvelles catégories à partir de la profondeur 5
            depth_keywords = EXTRA_CATEGORIES_SOUS_CATEGORIES  # Appliquer des mots-clés supplémentaires

        # Calculer les scores pour chaque CV à cette profondeur
        for cv_index, cv_text in enumerate(cvs):
            score = calculate_depth_score(cv_text, depth_category, depth_keywords)
            scores[cv_index].append(score)  # Ajouter le score pour cette profondeur

        # Classer les CV à cette profondeur
        sorted_cv_indices = sorted(scores.keys(), key=lambda x: scores[x][-1], reverse=True)
        
        # Sauvegarder le classement à cette profondeur
        for rank, cv_index in enumerate(sorted_cv_indices[:k]):  # Limite à k CVs
            rankings[cv_index].append(rank + 1)  # Stocke le rang dans le dictionnaire de rankings

    # Retourner les CVs avec les scores accumulés et leurs classements
    return rankings, scores, cvs_names


# Fonction pour extraire tous les CV d'un dossier
def extract_texts_from_folder(folder_path):
    cvs = []
    cvs_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            cvs.append(text)
            cvs_names.append(filename)  # Sauvegarder le nom du fichier CV
    return cvs, cvs_names


# Chemin vers le dossier contenant les CVs
folder_path = "./CV_test"

# Extraire les CVs du dossier
cvs, cvs_names = extract_texts_from_folder(folder_path)

# Nombre de CV à sélectionner à chaque profondeur
k = len(cvs)  # Vous pouvez ajuster la valeur ici en fonction de vos besoins

# Appliquer l'algorithme ALGII
rankings, scores, cvs_names = algii(cvs, k, cvs_names, max_depth=40)

# Sauvegarder les résultats dans un fichier CSV
with open('ranking_with_depths_test2.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    header = ["CV Name"]
    # Ajouter les en-têtes pour chaque profondeur (depth)
    for depth in range(len(rankings[0])):  # Le nombre de profondeurs
        header.append(f"Ranking depth{depth + 1}")
    
    writer.writerow(header)  # Entêtes du fichier CSV
    
    # Écrire les données pour chaque CV
    for i, cv_name in enumerate(cvs_names):
        row = [cv_name]
        row.extend(rankings[i])  # Ajouter les classements à chaque profondeur
        writer.writerow(row)

print("Le classement a été sauvegardé dans 'ranking_with_depths_test2.csv'.")