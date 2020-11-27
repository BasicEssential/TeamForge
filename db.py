from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# Global Variables
SQLITE = 'sqlite'
DB = "tmp_db/all_db.db"

# Table Names
STAFF = 'staff'
SKILLS = 'skills'

# Message
DB_QUERY = {
"SELECT": "SELECT {COLS} FROM {TABLE} WHERE 1=1 {CONDS}",
"GRP_SELECT": """SELECT {GRP_COLS_V}, {AGGR_COLS}
              FROM {TABLE} WHERE 1=1 {CONDS} 
              GROUP BY {GRP_COLS}""",
"GRP_HAV_SELECT": """SELECT {GRP_COLS_V}, {AGGR_COLS}
                  FROM {TABLE} WHERE 1=1 {CONDS} 
                  GROUP BY {GRP_COLS} HAVING {HCOND}""",
"DIST_SELECT": "SELECT DISTINCT {COLS} FROM {TABLE} WHERE 1=1 {CONDS}",
"LIM_SELECT": "SELECT {COLS} FROM {TABLE} WHERE 1=1 {CONDS} LIMIT {LIM}",
"INSERT": "INSERT INTO {TABLE}(COLS) VALUE ({VALUES})",
"DROP": "DROP TABLE {TABLE}"
}


class SqlLiteDatabase:

    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None

    def __init__(self, dbtype, dbname='', username='', password=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        """
        Create basic(MAIN) data base structure in DB

        :return:
        """
        metadata = MetaData()
        staff = Table(STAFF,
                      metadata,
                      Column('id', Integer, primary_key=True),
                      Column('first_name', String),
                      Column('last_name', String),
                      Column('personal_type', String),
                      Column('skill_id', None, ForeignKey('skills.id')))

        skills = Table(SKILLS,
                       metadata,
                       Column('id', Integer, primary_key=True),
                       Column('skill', String, nullable=False),
                       Column('description', String))
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '':
            return

        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)  # print(row[0], row[1], row[2])
                result.close()
        print("\n")
        

if "__main__" == __name__:
    SqlLiteDatabase(SQLITE, DB).execute_query("drop table staff")
    SqlLiteDatabase(SQLITE, DB).execute_query("drop table skills")
    SqlLiteDatabase(SQLITE, DB).create_db_tables()
    SqlLiteDatabase(SQLITE, DB).execute_query("insert into \
                                              staff(id, first_name, last_name, personal_type, skill_id)\
                                              values (1, 'Artem', 'Seleznev', 'Lead', 1)")
    SqlLiteDatabase(SQLITE, DB).execute_query("insert into \
                                              staff(id, first_name, last_name, personal_type, skill_id) \
                                              values (2, 'Sen', 'Seniorkin', 'Senior Pomidor', 2)")
    SqlLiteDatabase(SQLITE, DB).print_all_data("staff")
    