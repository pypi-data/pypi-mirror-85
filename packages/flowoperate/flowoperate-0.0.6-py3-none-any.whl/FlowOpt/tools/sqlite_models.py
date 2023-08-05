from sqlitemodel import Model, Database, SQL

# IMPORTANT

Database.DB_FILE = 'sqlite3.db'


class User(Model):
    def __init__(self, id=None):
        Model.__init__(self, id, dbfile=None, foreign_keys=False, parse_decltypes=False)

        self.firstname = ''
        self.lastname = ''
        self.age = ''

        # Tries to fetch the object by its rowid from the database
        self.getModel()

    # Tells the database class the name of the database table
    def tablename(self):
        return 'users'

    # Tells the database class more about the table columns in the database
    def columns(self):
        return [
            {
                'name': 'firstname',
                'type': 'TEXT'
            },
            {
                'name': 'lastname',
                'type': 'TEXT'
            },
            {
                'name': 'age',
                'type': 'INTEGER'
            }
        ]


class Missions(Model):
    def __init__(self, id=None, table_name=None):
        Model.__init__(self, id, dbfile=None, foreign_keys=False, parse_decltypes=False)
        self.table_name = table_name
        self.name = ''
        self.step = ''
        self.method = ''
        self.params = ''
        self.create_time = ''

        # Tries to fetch the object by its rowid from the database
        self.getModel()

    # Tells the database class the name of the database table
    def tablename(self):
        return self.table_name

    # Tells the database class more about the table columns in the database
    def columns(self):
        return [
            {
                'name': 'name',
                'type': 'LONGTEXT'
            },
            {
                'name': 'step',
                'type': 'INTEGER'
            },
            {
                'name': 'method',
                'type': 'TEXT'
            },
            {
                'name': 'params',
                'type': 'LONGTEXT'
            },
            {
                'name': 'create_time',
                'type': 'TEXT'
            },
        ]


if __name__ == '__main__':
    # # create a new user
    user = User()
    #
    # # creating the table inside the database
    user.createTable()
    #
    # # add infos about the user
    # user.firstname = 'Rene'
    # user.lastname = 'Tanczos'
    # user.age = 25
    #
    # # save the user into the database
    # user.save()

    # get it by id
    # user = User(1)

    # get the user by his firstname and lastname
    users = User().selectOne(SQL())
    # user = User().selectOne(SQL().WHERE('firstname', '=', 'Rene').AND().WHERE('lastname', '=', 'Tanczos'))

    # Or get more the one user
    # this method will return an array of matching users
    # users = User().select(SQL().WHERE('age', '=', 25))
    print(users.firstname)
