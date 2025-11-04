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

Остановился на том, что хотел реализовать логику поиска последовательностей стимулов для достижения результата
x1 - состояние наблюданиемое в датчиках vision, когда сработал датчик дофамина при насыщении
с1 - действие при котором сработал датчик дофамина при насыщении при состоянии x1
y1 - результат для достижения в виде датчика дофамина при насыщении

x2 - состояние наблюданиемое в датчиках vision, когда сработал датчик достижения x1 при действии с2
с2 - действи при котором состояние x2 перешло в x1
y2 - результат для достижения в виде получения x1 из x2

x3
c3
y3

и т.д.