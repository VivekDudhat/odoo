from odoo import http
from odoo.http import request

class AuthController(http.Controller):

    @http.route('/web/login/api', type='json', auth='public', methods=['GET'])
    def web_login_api(self, db, login, password):
        try:
            # Authentication for user 
            request.session.authenticate(db, login, password)
            user = request.env.user
            #if no user found
            if not user or user.id == 1:
                return {"error": "Invalid credentials"}
            
            # Return success message with user info
            return {
                "message": "Authentication successful",
                "user_id": user.id,
                "user_name": user.name,
                "session_id": request.session.session_token,
            }

        except Exception as e:
            return {"error": f"An error occurred during authentication: {str(e)}"}
