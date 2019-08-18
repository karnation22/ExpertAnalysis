import os, os.path

import cherrypy
import simplejson

class WebRoot(object):
    @cherrypy.expose
    def index(self):
        pass

@cherrypy.expose
class AnalyticsRequestWebService(object):
    def POST(self):
        cont_len = cherrypy.request.headers['Content-Length']
        r_body = cherrypy.request.body.read(int(cont_len))
        main_body = simplejson.loads(r_body) # should be dictionary w/ four booleans + season_id
        for form_fillout in main_body:
            if(form_fillout=="expert_curation" and main_body[form_fillout]): pass #do expert curation
            elif(form_fillout=="pred_power" and main_body[form_fillout]): pass # do predictive power
            elif(form_fillout=="weight_matrix" and main_body[form_fillout]): pass # do weight matrix
            elif(form_fillout=="predict_q_power" and main_body[form_fillout]): pass # do predictive q power
            else: season_id = int(main_body[form_fillout])
        return


## if __name__=='__main__':