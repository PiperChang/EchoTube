from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/' )

@bp.route('/') # url 생성해주는 것. route
def hello():
    return 'h'
  
if __name__=="__main__" :
    app.run()