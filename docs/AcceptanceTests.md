### Access

Use the outputted `vars.yaml` to find credentials to access the various components.

| Keycloak     | URL                     | Uses Keycloak | Admin/other access                                                                  |
|--------------|-------------------------|---------------|-------------------------------------------------------------------------------------|
| Keycloak     | auth.fdqn               | F             | credential-tavros secret                                                            |
| Gitea        | code.fdqn               | T - Prod      | all.vars.gitea.admin_password                                                       |
| Nexus        | artifacts.fdqn          | T - Prod      | all.vars.nexus.generated.admin_password                                             |
| Jenkins      | ci.fdqn                 | T - Prod      | N/A                                                                                 |
| Prod Kong    | admin.prod-kong.fdqn    | T - Prod      | N/A                                                                                 |
| Sandbox Kong | admin.sandbox-kong.fdqn | T - Sandbox   | N/A                                                                                 |
| Kibana       | kibana.fdqn             | F             | username as elastic, password as all.vars.elastic_cloud.generated.elastic_password  |
| Jaeger       | jaeger.fdqn             | T - Prod      | N/A  

Keycloak: all.vars.keycloak.admin_password

Run `kubectl get ingresses -A` to find the specific ingresses in your cluster.

### Out of the Box Acceptance Tests

These are in order. Refer to the above access chart for how to login to each component.

#### Keycloak

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin creds |  | | Auth |
| Can create new user and assign roles in prod (nexus: developer, jaeger: user) |  |  | Auth |

#### Gitea

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| 'Sign in with openid connect' is showing on login screen |  |  | Checks keycloak is set up correctly |
| Can login with admin creds |  |  | Auth |
| Can login with Keycloak creds (occasionally Keycloak needs to be re-enabled in gitea settings) |  |  | Auth |
| Platform repo is there |  |  |  |
| Can pull/push to repo |  |  |  |
| Can edit a file in Gitea and this causes an update to a component |  |  | Tests flux is working correctly |

#### Nexus

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin creds |  | N/A (not possible through UI?) | Auth |
| Can login with Keycloak creds |  |  | Auth |
| Repos exist: container-registry, dockerhub-proxy, internal, maven-central, maven-public, maven-releases, maven-snapshots |  |  | API calls to add repos were successful |
| Can login with jenkins-ci Keycloak creds (keycloak-basic-auth -n jenkins secret), has limited access (developer role) |  |  | Auth |
| Can login with created prod user and see repos |  |  | Auth |


#### Jenkins

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with Keycloak creds |  |  | Auth |
| Pipelines are there |  |  |  |
| Configuration as code is setup properly |  |  |  |
| Can create spec repo using Quickstart − OpenAPI Project |  |  |  |
| Can create API repo using Quickstart − Camel Web Service Project and previously created spec repo |  |  |  |
| Can scan Gitea Tavros org and API repo builds properly and updates helm release |  |  |  |

#### Nexus Registry

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Image exists in internal repo |  |  |  |

#### Other

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Can create helm release in Gitea in prod |  |  |  |
| Confirm image can be pulled by cluster, pod starts in prod |  |  |  |
| Update helm release in Gitea to include an ingress, confirm API is accessible with prod kong ingress (https://apps.<FQDN>/<path>/api/pet/123)  |  |  |  |
| Can create helm release in Gitea in dev (if not created by quickstart) |  |  |  |
| Confirm image can be pulled by cluster, pod starts in dev/test |  |  |  |
| Update helm release in Gitea to include an ingress, confirm API is accessible with sandbox kong ingress (https://apps.sandbox.<FQDN>/<path>/api/pet/123) |  |  |  |

#### Prod Kong

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin/keycloak prod creds (Kong Enterprise/Manager screen -> Keycloak screen) and view routes/services/etc |  |  |  |
| Kong license is configured properly (if it wasn't, install would have failed) |  |  |  |

#### Sandbox Kong

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with keycloak sandbox creds (Kong Enterprise/Manager screen -> Keycloak screen) and view routes/services/etc |  |  |  |
| Kong license is configured properly (if it wasn't, install would have failed) |  |  |  |

#### Kibana

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Assets are correctly installed |  |  |  |
| Can login with admin creds from and view logs. All expected dashboards (including 'Dashboard' -> 'Tavros - Logs Dashboard') are there. |  |  |  |
| Observability -> Uptime shows UP for prod, dev, and test pod  |  |  |  |

#### Jaeger

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin/keycloak prod creds and view traces |  |  |  |
| Can login with created prod user and view traces |  |  | Auth |

#### Service mesh (Kuma)

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| From PROD shell `curl 'http://api-repo.prod.svc.cluster.local:8080/actuator/health/liveness'` returns {"status":"UP"} |  |  |  |
| From PROD shell `curl 'http://api-repo.dev.svc.cluster.local:8080/actuator/health/liveness'` & `curl 'http://api-repo.test.svc.cluster.local:8080/actuator/health/liveness'` returns Empty reply from server |  |  |
| From DEV shell `curl 'http://api-repo.prod.svc.cluster.local:8080/actuator/health/liveness'` returns Empty reply from server |  |  |  |
| From DEV shell `curl 'http://api-repo.dev.svc.cluster.local:8080/actuator/health/liveness'` & `curl 'http://api-repo.test.svc.cluster.local:8080/actuator/health/liveness'` returns {"status":"UP"} |  |  |  |
| From TEST shell `curl 'http://api-repo.prod.svc.cluster.local:8080/actuator/health/liveness'` returns Empty reply from server |  |  |  |
| From TEST shell `curl 'http://api-repo.dev.svc.cluster.local:8080/actuator/health/liveness'` & `curl 'http://api-repo.test.svc.cluster.local:8080/actuator/health/liveness'` returns {"status":"UP"} |  |  |  |

#### Postgres

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Configured properly (If not configured properly, then Kong, Keycloak wouldn't start, so maybe this is not necessary) |  |  |  |