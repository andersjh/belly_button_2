
databaase = "sqlite"
# database = "mssql"
# database = "mongo"
# database = "postgres"

connect_string = ""

if database == "sqlite":
    connect_string = "sqlite:///belly_button.db"
elif database == "mssql":    
    connect_string = "mssql+pymssql://admin:adminpass@database-2.cevkalwufrrx.us-east-1.rds.amazonaws.com:1433/bellybutton"
elif database == "postgres":
    connect_string = "postgresql+psycopg2://postgres:adminpass@postgres-3.cevkalwufrrx.us-east-1.rds.amazonaws.com/bellybutton"
elif database == "mongo":        
    connect_string = "mongodb+srv://andersjh1120:PattersonJudson@clustertutorials-kgmhg.mongodb.net/?retryWrites=true&w=majority"
