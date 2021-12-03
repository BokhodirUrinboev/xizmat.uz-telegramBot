# xizmat.uz-telegramBot
## usage
```
1. First create your virtual environment
			python3 -m venv yourvenv

2. then activate yourvenv
	On Windows, run:  	yourvenv\Scripts\activate.bat
	On Unix or MacOS, run: 	source yourvenv/bin/activate

4. then install needed packages
			pip install -r requirements.txt

5.  rename example.env as env

6. then setup token and database in env file

7. Use PostgradeSql
 
8. run the app.py file in order to run telegram bot
	python app.py
```

``` init
1. pybabel extract . -o locales/xizmat_uz.pot
2. pybabel init -i locales/xizmat_uz.pot -d locales -D xizmat_uz -l en
3. pybabel init -i locales/xizmat_uz.pot -d locales -D xizmat_uz -l ru
4. pybabel compile -d locales -D xizmat_uz
```

```update
1. pybabel extract . -o locales/xizmat_uz.pot
2. pybabel update -d locales -D xizmat_uz -i locales/xizmat_uz.pot
3. pybabel compile -d locales -D xizmat_uz

```