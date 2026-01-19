from flask import Flask, render_template, request
import urllib.parse
import yaml

app = Flask(__name__)

# Filtre Jinja pour encoder une chaîne en URL safe
@app.template_filter('url_encode')
def url_encode_filter(s):
    return urllib.parse.quote_plus(s)

# chargement des schemas dorks depuis de schema yaml
def load_patterns(patterns_file):
    try:
        with open(patterns_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"le fichier {patterns_file} n'a pas été trouvé")
        return {}
    except yaml.YAMLError as e:
        print(f"le fichier {patterns_file} n'est pas un fichier YAML valide: {e}")
        return {}
    

def generate_dorks(domain_name, patterns_file='patterns.yml'):
    raw_patterns = load_patterns(patterns_file)
    if not raw_patterns:
        return {}
    
    site_filter = f"site:{domain_name}"
    dork_categories = {}

    # itération sur les catégories et les patterns
    for category, patterns in raw_patterns.items():
        dork_categories[category] = []
        for dork_pattern in patterns:
            dork_categories[category].append(f"{site_filter} {dork_pattern}")
    return dork_categories

@app.route('/', methods=['GET', 'POST'])
def index():
    dork_categories = None
    search_term = ""

    if request.method == 'POST':
        search_term = request.form.get('search', '').strip()
        if search_term:
            dork_categories = generate_dorks(search_term, 'patterns.yml')

    return render_template(
        'index.html',
        dork_categories=dork_categories,
        search_term=search_term
    )

if __name__ == '__main__':
    app.run(debug=True)

