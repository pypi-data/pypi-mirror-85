import dash
import flask
import pkgutil
import mimetypes
import dash_core_components as dcc

from dash._utils import stringify_id


class OAPDash(dash.Dash):
    static_files = {
        'css': [
            'bootstrap.css'
        ],
        'js': [ ]
    }

    def __init__(self, **kwargs):
        self.route = kwargs.pop('route')
        route_prefix = '/'+self.route if self.route else ''
        # assume this is not set by user
        kwargs['requests_pathname_prefix'] = route_prefix + '/'

        # add custom static files
        external_scripts = kwargs.get('external_scripts', [])
        for js in self.static_files['js']:
            external_scripts = external_scripts + [f'{route_prefix}/oap_dash/assets/{js}']
        kwargs['external_scripts'] = external_scripts

        external_stylesheets = kwargs.get('external_stylesheets', [])
        for css in self.static_files['css']:
            external_stylesheets = external_stylesheets + [f'{route_prefix}/oap_dash/assets/{css}']
        kwargs['external_stylesheets'] = external_stylesheets

        super(OAPDash, self).__init__(**kwargs)

    def init_app(self, app=None):
        """
        serve custom static files
        """
        super(OAPDash, self).init_app(app)
        self._add_url(
            "oap_dash/assets/<path:resource_path>",
            self.serve_oap_resources,
        )

    def serve_oap_resources(self, resource_path):
        """
        serve custom static files
        """
        extension = "." + resource_path.split(".")[-1]
        mimetype = mimetypes.types_map.get(extension)

        response = flask.Response(
            pkgutil.get_data("oap_dash", "assets/"+resource_path), mimetype=mimetype
        )
        return response

    def get_component_ids(self, layout):
        component_ids = []
        for component in layout._traverse():
            component_id = stringify_id(getattr(component, "id", None))
            component_ids.append(component_id)

        return component_ids

    def _layout_value(self):
        """
        add custom stores
        """
        _layout = self._layout() if self._layout_is_function else self._layout                        

        component_ids = self.get_component_ids(_layout)
        in_store_id = "_oap_data_in_" + self.route
        out_store_id = "_oap_data_out_" + self.route
        
        if in_store_id not in component_ids:
            _layout.children.append(dcc.Store(id="dummy-store"))
            _layout.children.append(dcc.Store(id=out_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id=in_store_id, storage_type="local"))

        return _layout
