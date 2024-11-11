from quart import Blueprint, make_response, jsonify, send_from_directory, current_app
from .controller import MainController


main_bp = Blueprint('main', __name__)
main_controller = MainController()

swagger_ui = Blueprint("swagger_ui", __name__, static_folder='swaggerui')

@swagger_ui.route('swaggerui')
@swagger_ui.route('swaggerui/<path:path>')
async def show(path=None):
    if path is None:
        return await send_from_directory(swagger_ui.static_folder, 'index.html')
    return await send_from_directory(swagger_ui.static_folder, path)

@main_bp.route('/', methods=['GET'])
def index():
  """ Example endpoint with simple greeting.
  ---
  tags:
    - Example API
  responses:
    200:
      description: A simple greeting
      schema:
        type: object
        properties:
          data:
            type: object
            properties:
              message:
                type: string
                example: "Hello World!"
  """
  result = main_controller.index()
  return make_response(jsonify(data=result))

@main_bp.route('/test', methods=['GET'])
def test():
    """ Test endpoint to check if the API works.
    ---
    tags:
      - Test API
    responses:
      200:
        description: API is working
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "API is working!"
    """
    return make_response(jsonify(data={"message": "API is working!"}))
