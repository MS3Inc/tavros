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

Run `kubectl get ingresses -A` to find the specific ingresses in your cluster.                                                                               |

### Initial Setup Acceptance Tests

These are in order. Refer to the above access chart for how to login to each component.

#### Keycloak

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with admin creds |  | PASS | Auth |
| Can create account and assign roles in prod |  | UNKNOWN, need to define roles | Auth |
| Can create account and assign roles in sandbox |  | UNKNOWN | Auth |

#### Gitea

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with admin creds |  | PASS | Auth |
| Can login with Keycloak creds |  | PASS | Auth |
| Platform repo is there |  | PASS |  |
| Can edit a file in Gitea and this causes an update to a component |  | PASS | Tests flux is working correctly |

#### Nexus

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with admin creds |  | PASS | Auth |
| Can login with Keycloak creds | no keycloak prompt | FAIL | Auth |
| Repos exist: container-registry, dockerhub-proxy, internal, maven-central, maven-public, maven-releases, maven-snapshots |  | PASS | API calls were successful |


#### Jenkins

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with Keycloak creds |  | FAIL | Auth |
| Pipelines are there |  | FAIL |  |
| Can deploy an API using quickstart |  | FAIL |  |

#### Nexus Registry

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Image exists in internal repo |  | PASS |  |

#### Other

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Can create helm release in Gitea (if not created by quickstart)|  | PASS |  |
| Confirm image can be pulled by cluster, pod starts in specified namespace |  | PASS |  |
| Update helm release in Gitea to include an ingress, confirm API is accessible with ingress |  | PASS |  |

#### Prod Kong

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with keycloak prod creds (Kong Enterprise/Manager screen -> Keycloak screen) and view routes/services/etc | Is showing Kong Manager instead | FAIL |  |
| Kong license is configured properly (if it wasn't, install would have failed) | why is it Kong Manager instead of Enterprise? | FAIL? |  |

#### Sandbox Kong

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with keycloak sandbox creds (Kong Enterprise/Manager screen -> Keycloak screen) and view routes/services/etc | FAIL | Is showing Kong Manager instead |  |
| Kong license is configured properly (if it wasn't, install would have failed) |  | FAIL? |  |

#### Kibana

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with admin creds from and view logs. All expected dashboards (including Tavros - Logs Dashboard) are there. |  | PASS |  |

#### Jaeger

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  | PASS | Checks cert manager is working correctly |
| Can login with keycloak prod creds and view traces | Getting {"message":"Forbidden"} | FAIL |  |

#### Service mesh (Kuma)

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Can't curl from one prod to test |  | PASS |  |

#### Postgres

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| If not configured properly, then Kong and ? wouldn't start, so maybe this is not necessary |  | PASS? |  |

### Keycloak Roles

Realm roles: offline access, uma_authorization

Client roles:
Account: manage account, view profile
Account console: none
Admin cli: none
Broker: none
Gitea: none?
Jaeger: user
Jenkins: none
Nexus: admin or developer
Prod-kong: super-admin (or is this added in Kong itself?)
Realm management: none
Security admin console: none