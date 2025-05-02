from diagrams import Cluster, Diagram
from diagrams.gcp.storage import GCS
from diagrams.generic.storage import Storage
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Mongodb
from diagrams.onprem.gitops import Argocd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.vcs import Github
from diagrams.programming.framework import Fastapi
from diagrams.saas.chat import Slack
from diagrams.saas.identity import Auth0

graph_attr = {
    "layout": "dot",
    "rankdir": "TB",
    "nodesep": "1",
    "ranksep": "1",
    "splines": "true",
    "ratio": "auto",
}

node_attr = {
    "fontcolor": "black",
    "fontsize": "16",
    "shape": "ellipse",
    "style": "transparent",
    "color": "black"
}

edge_attr = {
    "color": "black",
    "arrowhead": "normal",
    "fontcolor": "black"
}

with (Diagram("RECIPE", show = False, graph_attr = graph_attr, node_attr = node_attr, edge_attr = edge_attr)) as diag:
    with Cluster("API services", direction = "TB"):
        with Cluster("VCS"):
            vcs = Github("karned-rekipe/api-recipe")

            with Cluster("CD"):
                cd = Argocd("ArgoCD")

                with Cluster("Kubernetes"):
                    docker_api = Docker("API recipe")
                    docker_db = Docker("DB recipe")

            with Cluster("CI"):
                ci = Jenkins("Jenkins")
                hub = Storage("Docker Hub")

        with Cluster("API"):
            api = Fastapi("FastAPI")
            db = Mongodb("MongoDB")



    with Cluster("Services"):
        with Cluster("API gateway"):
            gateway = Nginx("API gateway")

        with Cluster("Storage"):
            storage = GCS("Bucket GCS")

        with Cluster("Auth"):
            auth = Auth0("Keycloak")

        with Cluster("Messaging"):
            message = Kafka("Kafka")

        with Cluster("Monitoring"):
            metrics = Prometheus("Prometheus")
            dashboard = Grafana("Grafana")

        with Cluster("Alert"):
            im = Slack("karned #api-recipe")

    vcs >> cd
    cd >> docker_api
    cd >> docker_db
    ci >> vcs
    vcs >> ci >> hub >> cd
    vcs >> im
    ci >> im
    docker_db >> db
    docker_api >> api

    api >> db >> api
    api >> auth >> api
    api >> gateway >> api
    api >> message >> api
    api >> storage
    api >> metrics
    db >> metrics

