За основу взят обучающий проект по этой ссылке:  
[Django Tutorial in Visual Studio Code](https://code.visualstudio.com/docs/python/tutorial-django)

pip install --upgrade pip           # to upgrade pip

pip install "psycopg[binary,pool]"  # to install package and dependencies


pip freeze > requirements.txt


python manage.py collectstatic


Откатиться до нужного коммита, чтобы почистить историю коммитов и объединить в боллее понятный коммит:  
git reset --soft 08880f507e35ac299a55e468a35897c658059d5f
git push origin main --force