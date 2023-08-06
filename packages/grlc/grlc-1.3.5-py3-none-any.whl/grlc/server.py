#!/usr/bin/env python

# server.py: the grlc server

from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS

# grlc modules
import grlc.static as static
import grlc.utils as utils
import grlc.glogging as glogging

glogger = glogging.getGrlcLogger(__name__)

### The Flask app ###
app = Flask(__name__)
CORS(app)

### Helper functions ###
def relative_path():
    """Generate relative path for the current route. This is used to build relative paths when rendering templates."""
    path = request.path
    path = '.' + '/..' * (path.count('/') - 1)
    return path

def api_docs_template():
    """Generate Grlc API page."""
    return render_template('api-docs.html', relative_path=relative_path())

def swagger_spec(user, repo, subdir=None, spec_url=None, sha=None, content=None):
    """ Generate swagger specification """
    glogger.info("-----> Generating swagger spec for /{}/{}, subdir {}, params {}, on commit {}".format(user, repo, subdir, spec_url, sha))

    swag = utils.build_swagger_spec(user, repo, subdir, spec_url, sha, static.SERVER_NAME)

    resp_spec = make_response(jsonify(swag))
    resp_spec.headers['Content-Type'] = 'application/json'

    resp_spec.headers['Cache-Control'] = static.CACHE_CONTROL_POLICY  # Caching JSON specs for 15 minutes

    glogger.info("-----> API spec generation for /{}/{}, subdir {}, params {}, on commit {} complete".format(user, repo, subdir, spec_url, sha))
    return resp_spec

def query(user, repo, query_name, subdir=None, spec_url=None, sha=None, content=None):
    """Execute SPARQL query for a specific grlc-generated API endpoint"""
    glogger.info("-----> Executing call name at /{}/{}/{}/{} on commit {}".format(user, repo, subdir, query_name, sha))
    glogger.debug("Request accept header: " + request.headers["Accept"])

    requestArgs = request.args
    acceptHeader = request.headers['Accept']
    requestUrl = request.url
    formData = request.form

    query_response, status, headers = utils.dispatch_query(user, repo, query_name, subdir, spec_url,
                                                           sha=sha, content=content, requestArgs=requestArgs,
                                                           acceptHeader=acceptHeader,
                                                           requestUrl=requestUrl, formData=formData)
    if isinstance(query_response, list):
        query_response = jsonify(query_response)

    return make_response(query_response, status, headers)

### Server routes ###
@app.route('/')
def grlc():
    """Grlc landing page."""
    resp = make_response(render_template('index.html'))
    return resp

#############################
### Routes for local APIs ###
#############################

# Spec generation, front-end
@app.route('/api-local', methods=['GET'], strict_slashes=False)
@app.route('/api/local/local', methods=['GET'], strict_slashes=False)  # backward compatibility route
def api_docs_local():
    """Grlc API page for local routes."""
    return api_docs_template()

# Spec generation, JSON
@app.route('/api-local/swagger', methods=['GET'])
@app.route('/api/local/local/swagger', methods=['GET'], strict_slashes=False)  # backward compatibility route
@app.route('/api-local/spec', methods=['GET'])                              # backward compatibility route
@app.route('/api/local/local/spec', methods=['GET'], strict_slashes=False)  # backward compatibility route
def swagger_spec_local():
    """Swagger spec for local routes."""
    return swagger_spec(user=None, repo=None, sha=None, content=None)

# Callname execution
@app.route('/api-local/<query_name>', methods=['GET', 'POST'])
@app.route('/api/local/local/<query_name>', methods=['GET', 'POST'], strict_slashes=False)  # backward compatibility route
def query_local(query_name):
    """SPARQL query execution for local routes."""
    return query(user=None, repo=None, query_name=query_name)

################################
### Routes for URL HTTP APIs ###
################################

# Spec generation, front-end
@app.route('/api-url', methods=['POST', 'GET'], strict_slashes=False)
def api_docs_param():
    """Grlc API page for specifications loaded via http."""
    # Get queries provided by params
    spec_url = request.args['specUrl']
    glogger.info("Spec URL: {}".format(spec_url))
    return api_docs_template()

# Spec generation, JSON
@app.route('/api-url/swagger', methods=['GET'])
@app.route('/api-url/spec', methods=['GET'])      # backward compatibility route
def swagger_spec_param():
    """Swagger spec for specifications loaded via http."""
    spec_url = request.args['specUrl']
    glogger.info("Spec URL: {}".format(spec_url))
    return swagger_spec(user=None, repo=None, spec_url=spec_url)

# Callname execution
@app.route('/api-url/<query_name>', methods=['GET', 'POST'])
def query_param(query_name):
    """SPARQL query execution for specifications loaded via http."""
    spec_url = request.args['specUrl']
    glogger.debug("Spec URL: {}".format(spec_url))
    return query(user=None, repo=None, query_name=query_name, spec_url=spec_url)

##############################
### Routes for GitHub APIs ###
##############################

# Spec generation, front-end
@app.route('/api-git/<user>/<repo>', strict_slashes=False)
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>', strict_slashes=False)
@app.route('/api-git/<user>/<repo>/api-docs')
@app.route('/api-git/<user>/<repo>/commit/<sha>')
@app.route('/api-git/<user>/<repo>/commit/<sha>/api-docs')
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/commit/<sha>')
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/commit/<sha>/api-docs')
@app.route('/api/<user>/<repo>', strict_slashes=False)  # backward compatibility route
@app.route('/api/<user>/<repo>/<path:subdir>', strict_slashes=False)  # backward compatibility route
@app.route('/api/<user>/<repo>/api-docs')  # backward compatibility route
@app.route('/api/<user>/<repo>/commit/<sha>')  # backward compatibility route
@app.route('/api/<user>/<repo>/commit/<sha>/api-docs')  # backward compatibility route
@app.route('/api/<user>/<repo>/<path:subdir>/commit/<sha>')  # backward compatibility route
@app.route('/api/<user>/<repo>/<path:subdir>/commit/<sha>/api-docs')  # backward compatibility route
def api_docs_git(user, repo, subdir=None, sha=None):
    """Grlc API page for specifications loaded from a Github repo."""
    return api_docs_template()

# Spec generation, JSON
@app.route('/api-git/<user>/<repo>/swagger', methods=['GET'])
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/swagger', methods=['GET'])
@app.route('/api-git/<user>/<repo>/commit/<sha>/swagger')
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/commit/<sha>/swagger')
@app.route('/api-git/<user>/<repo>/<path:subdir>/commit/<sha>/swagger')
@app.route('/api/<user>/<repo>/swagger', methods=['GET'])  # backward compatibility route
@app.route('/api/<user>/<repo>/<subdir>/swagger', methods=['GET'])  # backward compatibility route
@app.route('/api/<user>/<repo>/commit/<sha>/swagger')  # backward compatibility route
@app.route('/api/<user>/<repo>/<subdir>/commit/<sha>/swagger')  # backward compatibility route
@app.route('/api-git/<user>/<repo>/spec', methods=['GET'])  # backward compatibility route
@app.route('/api-git/<user>/<repo>/swagger', methods=['GET'])  # backward compatibility route
@app.route('/api-git/<user>/<repo>/subdir/<subdir>/spec', methods=['GET'])  # backward compatibility route
@app.route('/api-git/<user>/<repo>/<path:subdir>/swagger', methods=['GET'])  # backward compatibility route
@app.route('/api-git/<user>/<repo>/commit/<sha>/spec')  # backward compatibility route
@app.route('/api-git/<user>/<repo>/subdir/<subdir>/commit/<sha>/spec')  # backward compatibility route
@app.route('/api-git/<user>/<repo>/<subdir>/commit/<sha>/spec')  # backward compatibility route
@app.route('/api-git/<user>/<repo>/<path:subdir>/commit/<sha>/swagger')  # backward compatibility route
@app.route('/api/<user>/<repo>/spec', methods=['GET'])  # backward compatibility route
@app.route('/api/<user>/<repo>/<subdir>/spec', methods=['GET'])  # backward compatibility route
@app.route('/api/<user>/<repo>/commit/<sha>/spec')  # backward compatibility route
@app.route('/api/<user>/<repo>/<subdir>/commit/<sha>/spec')  # backward compatibility route
def swagger_spec_git(user, repo, subdir=None, sha=None):
    """Swagger spec for specifications loaded from a Github repo."""
    return swagger_spec(user, repo, subdir=subdir, spec_url=None, sha=sha, content=None)

# Callname execution
@app.route('/api-git/<user>/<repo>/<query_name>', methods=['GET', 'POST'])
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/<query_name>', methods=['GET', 'POST'])
@app.route('/api-git/<user>/<repo>/<query_name>.<content>', methods=['GET', 'POST'])
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/<query_name>.<content>', methods=['GET', 'POST'])
@app.route('/api-git/<user>/<repo>/commit/<sha>/<query_name>', methods=['GET', 'POST'])
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/commit/<sha>/<query_name>', methods=['GET', 'POST'])
@app.route('/api-git/<user>/<repo>/commit/<sha>/<query_name>.<content>', methods=['GET', 'POST'])
@app.route('/api-git/<user>/<repo>/subdir/<path:subdir>/commit/<sha>/<query_name>.<content>', methods=['GET', 'POST'])
@app.route('/api/<user>/<repo>/<query_name>', methods=['GET', 'POST'])  # backward compatibility route
@app.route('/api/<user>/<repo>/<path:subdir>/<query_name>', methods=['GET', 'POST'])  # backward compatibility route
@app.route('/api/<user>/<repo>/<query_name>.<content>', methods=['GET', 'POST'])  # backward compatibility route
@app.route('/api/<user>/<repo>/<path:subdir>/<query_name>.<content>', methods=['GET', 'POST'])  # backward compatibility route
@app.route('/api/<user>/<repo>/commit/<sha>/<query_name>', methods=['GET', 'POST'])  # backward compatibility route
@app.route('/api/<user>/<repo>/<path:subdir>/commit/<sha>/<query_name>', methods=['GET', 'POST'])  # backward compatibility route
@app.route('/api/<user>/<repo>/commit/<sha>/<query_name>.<content>', methods=['GET', 'POST'])  # backward compatibility route
@app.route('/api/<user>/<repo>/<path:subdir>/commit/<sha>/<query_name>.<content>', methods=['GET', 'POST'])  # backward compatibility route
def query_git(user, repo, query_name, subdir=None, sha=None, content=None):
    """SPARQL query execution for specifications loaded from a Github repo."""
    return query(user, repo, query_name, subdir=subdir, sha=sha, content=content)


# Main thread
if __name__ == '__main__':
    app.run(host=static.DEFAULT_HOST, port=static.DEFAULT_PORT, debug=True)
