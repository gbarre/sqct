import os
import connexion

basedir = os.path.abspath(os.path.dirname(__file__))

app =  connexion.App(__name__, specification_dir=os.path.join(basedir, 'spec'))
app.add_api('openapi.yml', strict_validation=True,validate_responses=True)
app.run(port=5000)