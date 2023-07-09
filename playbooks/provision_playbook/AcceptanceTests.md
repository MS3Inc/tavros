### Access

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

These are in order.

#### Keycloak

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin creds |  |  | Auth |
| Can create account and assign roles in prod |  |  | Auth |
| Can create account and assign roles in sandbox |  |  | Auth |

#### Gitea

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin creds |  |  | Auth |
| Can login with Keycloak creds |  |  | Auth |
| Platform repo is there |  |  |  |
| Can edit a file in Gitea and this causes an update to a component |  |  | Tests flux is working correctly |

#### Nexus

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin creds |  |  | Auth |
| Can login with Keycloak creds |  |  | Auth |
| Repos exist: container-registry, dockerhub-proxy, internal, maven-central, maven-public, maven-releases, maven-snapshots |  |  | API calls were successful |


#### Jenkins

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with Keycloak creds |  |  | Auth |
| Pipelines are there |  |  |  |
| Can deploy an API using quickstart |  |  |  |

#### Nexus Registry

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Image exists in internal repo |  |  |  |

#### Other

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Can create helm release in Gitea (if not created by quickstart)|  |  |  |
| Confirm image can be pulled by cluster, pod starts in specified namespace |  |  |  |
| Update helm release in Gitea to include an ingress, confirm API is accessible with ingress |  |  |  |
| Confirm API ingress is secure |  |  |  |

#### Prod Kong

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with keycloak prod creds and view routes/services/etc |  |  |  |
| Kong license is configured properly (if it wasn't, install would have failed) |  |  |  |

#### Sandbox Kong

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with keycloak sandbox creds and view routes/services/etc |  |  |  |
| Kong license is configured properly (if it wasn't, install would have failed) |  |  |  |

#### Kibana

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with admin creds from and view logs. All expected dashboards (including Tavros - Logs Dashboard) are there. |  |  |  |

#### Jaeger

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Is secure |  |  | Checks cert manager is working correctly |
| Can login with keycloak prod creds and view traces |  |  |  |

#### Service mesh (Kuma)

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| Can't curl from one prod to test |  |  |  |

#### Postgres

| Expected result | Actual result | PASS/FAIL | Purpose of test |
|---|---|---|---|
| If not configured properly, then Kong and ? wouldn't start, so maybe this is not necessary |  |  |  |