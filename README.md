За основу взят обучающий проект по этой ссылке:  
[Django Tutorial in Visual Studio Code](https://code.visualstudio.com/docs/python/tutorial-django)

pip install --upgrade pip           # to upgrade pip

pip install "psycopg[binary,pool]"  # to install package and dependencies


pip freeze > requirements.txt


python manage.py collectstatic


Миграция:  
python manage.py dumpdata > datadump.json  
python manage.py makemigrations  
python manage.py migrate  
python manage.py loaddata datadump.json  

Откатиться до нужного коммита, чтобы почистить историю коммитов и объединить в боллее понятный коммит:  
git reset --soft 08880f507e35ac299a55e468a35897c658059d5f  
git push origin main --force

https://channels.readthedocs.io/en/stable/installation.html
python -m pip install -U 'channels[daphne]'
python3 -c 'import channels; import daphne; print(channels.__version__, daphne.__version__)'


$ git clone git@github.com:django/channels.git
$ cd channels
$ <activate your project’s virtual environment>
(environment) $ pip install -e .  # the dot specifies the current repo