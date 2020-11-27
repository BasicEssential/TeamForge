from config import conf
from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__,
            template_folder=conf.TEMPLATES_PATH,
            static_folder=conf.STATIC_FILES_PATH)


@app.route('/')
def index():
    menuList = [("DashBoard", ["s1", "s1"]),
                ("Команда", ["s1", "s1"]),
                ("Персона", ["s1", "s1"]),
                ("Траектории", ["s1", "s1"]),
                ("Методология", ["s1", "s1"]),
                ("Расписание", ["s1", "s1"])
                ]

    appName = conf.APPNAME
    menuList = menuList
    menupage = "TeamDash"
    crums = ["Dashboard", menupage]

    return render_template(['index.html', 'top_menu.html', 'bcrums.html'],
                           appName = appName,
                           menuList = menuList,
                           menupage = menupage,
                           crums = crums
                           )

@app.route('/team-<teamname>/members')
def users(teamname):
    return f'SHOW YOUR TEAMMATE IN TEAM {teamname}'


def some_func(var, l = [], a = 1):
    return var

if __name__ == "__main__":
    app.run(host=conf.HOST, port=conf.PORT, debug=True)
