from tools.apis.pmaw_api import make_pmaw_instance
from tools.apis.praw_api import login_ro as make_praw_ro_instance


praw_api = make_praw_ro_instance()
pmaw_api = make_pmaw_instance()
