from flask import Flask, jsonify, session
from multiprocessing import Process
from flask_sockets import Sockets
from concurrent.futures import Future

import json
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# socketio = SocketIO(app, cors_allowed_origins='*')
sockets = Sockets(app)

# mock events table
MAPPING = {
    "mcm_events_mock": {
        "mcmEventsPath": "maprfs://mapr5/sas/pca/experiments-lci/nd-ap-app-nm-1342/7a283c96b3232c0f2e5c7cfca14204fe0bdf63df38139af0de4252b1f108250e/events",
        "mcmEventsCount": None,
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-2505"
    },
    "impressions-nm_mock": {
        "path": "maprfs://mapr5/sas/pca/experiments-lci/impressions_81af6c9b-f91b-4e7e-bdd3-7315ce9247fe",
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-2860"
    },
    "repartition_mock": {
        "mcmEventsPath": "maprfs://mapr5/sas/pca/experiments-lci/nd-ap-app-nm-1342/7a283c96b3232c0f2e5c7cfca14204fe0bdf63df38139af0de4252b1f108250e/events",
        "mcmEventsCount": None,
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-2505"
    },
    "ctrl-events_mock": {
        "eventsPath": "maprfs://mapr5/sas/pca/experiments-lci/events_with_fixed_control_a7f71af8-f0d9-4ab0-911a-6d381f32bb2f",
        "eventsCount": 354381,
        "eventLogPath": "maprfs://mapr5/opt/spark-history/56af211a-ea18-4e97-8491-a8a5d2542acc-24648"
    },
    "lci_2_1_collect_metrics_mock": {
        "name": "Metrics",
        "columns": [
            "stage_name",
            "name",
            "value"
        ]
    },
    "xdv_mock": {
        "otherLocationsEventsExposedPath": None,
        "impressionsPath": "maprfs://mapr5/sas/pca/experiments-lci/xdv_impressions_d0136c23-242f-487e-9a5f-3cf9378c24c7",
        "controlPath": None,
        "otherLocationsEventsVisitedPath": None,
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-2983",
        "eventsPath": "maprfs://mapr5/sas/pca/experiments-lci/xdv_events_0aaeba96-26ec-4a39-b569-c9afba4e9634"
    },
    "matching_mock": {
        "controlPath": "maprfs://mapr5/sas/pca/experiments-lci/matching_control_b41fbf09-840e-4af6-b25e-4dbbc3284bab",
        "exposedPath": "maprfs://mapr5/sas/pca/experiments-lci/matching_exposed_9f4e8c5c-fa00-4523-8a4c-a423be309c47",
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-3028"
    },
    "cleanup-path_mock": True,
    "profile-preparer_mock": {
        "profilesPath": "maprfs://mapr5/sas/pca/experiments-lci/profile_106c1f55-9830-45ad-9ed5-2597b3855c02",
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-2997"
    },
    "groups-filter_mock": {
        "filteredImpressions": "maprfs://mapr5/sas/pca/experiments-lci/impressions_custom_group_110bf769-7c78-424d"
                               "-a716-da6c0975de7c",
        "customGroupsToKeep": ["xax_creative_logo", "xax_creative_shoppingmaxximizingbeauty",
                               "xax_creative_shoppingmaxximizingdining"]
    },
    "new-metric_mock": [{
        "name": "Unique Overalls",
        "columns": [
            "inventory_type",
            "users",
            "devices"
        ],
        "rows": [
            [
                "mapp",
                473836,
                489343
            ]
        ]
    }],
    "mcm-locations_mock": {
        "locationsPath": "maprfs://mapr5/sas/pca/experiments-lci"
                         "/ec886a686f1b18a0d09fbc8726d3175c9dfb4194eceeeac39baef290fc3f2984/locations_ccfa321d-0486"
                         "-4d24-a370-e66d242c78f6",
        "locationsCount": 11,
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-2075"
    },
    "reduce-events": {
        "mcmEventsPath": "maprfs://mapr5/sas/pca/experiments-lci"
                         "/ec886a686f1b18a0d09fbc8726d3175c9dfb4194eceeeac39baef290fc3f2984/events_130b5113-5c61-4333"
                         "-aa33-2314ed72ff5f",
        "mcmEventsCount": 0,
        "eventLogPath": "maprfs://mapr5/opt/spark-history/e418ef3d-cd73-4e6e-aec9-4f9fb3e66291-2182"
    }
}


def get_event_ret(function_id):
    return {
        "event": "finished",
        "result": MAPPING[function_id]
    }


@app.route("/v2/api/functions/<function_id>/jobs", methods=["POST"])
def run_job_mock(function_id):
    return {"id": function_id + "_mock"}


@sockets.route('/v2/api/ws/jobs/<function_id>')
def hello(ws, function_id):
    while not ws.closed:
        print "function ID is " + str(function_id)
        ret = get_event_ret(function_id)
        ws.send(json.dumps(ret))
        ws.close()



if __name__ == "__main__":
    # app.run(debug=True, port=1999)
    # socketio.run(app, debug=True, host="localhost", port=1999)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('localhost', 1999), app, handler_class=WebSocketHandler)
    s = Process(target=server.serve_forever, kwargs=dict(stop_timeout=1))
    s.start()
