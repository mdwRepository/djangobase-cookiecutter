# this files contains basic metadata about the project. This data will be used
# (by default) in the base.html and index.html

PROJECT_METADATA = {
    'title': '{{cookiecutter.project_title}}',
    'author': 'Peter Andorfer, Stefan Szepe',
    'subtitle': 'A django project to bootstrap further web-app developments',
    'description': '{{cookiecutter.project_short_description}}',
    'github': '{{cookiecutter.github_url}}',
    'purpose_de': 'der Schaffung einer einheitlichen\
    und generischen Grundlage für Web Applikationen.',
    'purpose_en': 'to bootstrap web development.',
    'version': '{{cookiecutter.version}}',
    'matomo_id': 'provide some',
    'matomo_url': '//mdw.ac.at/piwik/',
    'imprint': '/imprint',
    'social_media': [
        ('fab fa-twitter fa-2x', 'https://twitter.com/mdwwien'),
        ('fab fa-youtube fa-2x', 'https://www.youtube.com/user/mdwvienna'),
    ],
    'app_type': 'database',  # database|website|service|tool|digital-edition
}
