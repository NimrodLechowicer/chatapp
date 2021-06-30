PGHOST = 'ec2-34-195-143-54.compute-1.amazonaws.com'
PGDATABASE = 'd10v7k0t9ktpcq'
PGPORT = '5432'
PGUSER = 'zntaarwccxeuej'
PGPASSWORD = '53199ca83ed26655c802e4579187eaf4b490b259e668f6307f14525465ffd649'

conn_string = "host=" + PGHOST + " port=" + "5432" + " dbname=" + PGDATABASE + " user=" + PGUSER \
              + " password=" + PGPASSWORD


def app_init(app):
    app.config['SECRET_KEY'] = 'super-secret'
    return app

