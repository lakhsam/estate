from urllib.parse import parse_qs

from odoo import http
from odoo.tools import json


class PropertyApi(http.Controller):

    @http.route("/v1/api/properties", type="http", methods=["GET"], auth="public", csrf=False)
    def get_property_ids(self):
        try:
            params = parse_qs(http.request.httprequest.query_string.decode("utf-8"))
            property_domain = []
            if params.get('state'):
                property_domain.append(('state', '=', params.get('state')))
            property_ids = http.request.env['property'].sudo().search(property_domain)
            if not property_ids:
                return http.request.make_json_response({
                    'message': "There is no properties",
                }, status=400)

            return http.request.make_json_response([{
                'id': property_id.id,
                'name': property_id.id,
                'ref': property_id.id,
                'description': property_id.description,
                'bedrooms': property_id.bedrooms,
                'garden_orientation': property_id.garden_orientation,
            } for property_id in property_ids], status=200)

        except Exception as e:
            return http.request.make_json_response({
                'message': e,
            }, status=400)

    @http.route("/v1/api/properties", type="http", methods=["POST"], auth="none", csrf=False)
    def post_property(self):
        args = http.request.httprequest.data.decode()
        vals = json.loads(args)

        if not vals.get('name'):
            return http.request.make_json_response({
                'message': "Name is required",
            }, status=400)

        try:
            res = http.request.env['property'].sudo().create(vals)
            if res:
                return http.request.make_json_response({
                    'id': res.id,
                }, status=201)
        except Exception as e:
            return http.request.make_json_response({
                'message': e,
            }, status=400)

    @http.route("/v1/api/properties/<int:property_id>", type="http", methods=["PUT"], auth="none", csrf=False)
    def update_property(self, property_id):
        property_id = http.request.env['property'].sudo().search([('id','=',property_id)])
        args = http.request.httprequest.data.decode()
        vals = json.loads(args)
        property_id.write(vals)
        return http.request.make_json_response({
                    'id': property_id.id,
                }, status=201)

    @http.route("/v1/api/properties/<int:property_id>", type="http", methods=["GET"], auth="none", csrf=False)
    def get_property_by_id(self, property_id):
        try:
            property_id = http.request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return http.request.make_json_response({
                    'message': "There is no property with this id",
                }, status=400)

            return http.request.make_json_response({
                'id': property_id.id,
                'name': property_id.id,
                'ref': property_id.id,
                'description': property_id.description,
                'bedrooms': property_id.bedrooms,
                'garden_orientation': property_id.garden_orientation,
            })

        except Exception as e:
            return http.request.make_json_response({
                'message': e,
            }, status=400)

    @http.route("/v1/api/properties/<int:property_id>", type="http", methods=["DELETE"], auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = http.request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return http.request.make_json_response({
                    'message': "There is no property with this id",
                }, status=400)

            property_id.unlink()

            return http.request.make_json_response({
                'message': "Property has been deleted",
            }, status=400)

        except Exception as e:
            return http.request.make_json_response({
                'message': e,
            }, status=400)
