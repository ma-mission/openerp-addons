

1 - Install Cx_Oracle
2 - Install Modules Home - APOGEE - Connecteur
3 - Install fonts in server
4 - nano addons/web/static/src/css/base.css 1432 background: url('/HOME/static/src/img/back.png');
5 - Change image in this location : /opt/openerp/v7/addons/web/static/src/img/logo2.png
6 - Modify top attribute in this css file /opt/openerp/v7/addons/web/static/src/css/base.css
	
	945 .openerp .oe_login .oe_login_logo {
  		position: absolute;
		top: -120px;
		...;
	}

7 - Modify background attribute in this css file /opt/openerp/v7/addons/web/static/src/css/base.css

	841 .openerp .oe_login {
		/*  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAYAAAAGCAYAAADgzO9IAAAAKUlEQVQIHWO8e/fufwYsgAU$
		  background-image: url(/HOME/static/src/img/back.png);
	}

8 - nano /opt/openerp/v7/addons/web_graph/static/lib/flotr2/js/Flotr.js, And modify this 142 line :

	defaultTrackFormatter: function(obj){
  		/**
	    	return '('+obj.x+', '+obj.y+')';
   		*/
		return '['+obj.series.label+' : '+Math.round(obj.y)+']';

  	},
