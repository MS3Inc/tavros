## Manual Backup and Restore Procedures

### Postgres

#### Backup Postgres

```
PASSWORD=$(kubectl get secrets/tavros-pg-creds -n postgresql --template='{{ index .data "postgres-password" | base64decode}}')

kubectl run pgtesting --image=docker.io/bitnami/postgresql:14.3.0-debian-10-r22 -n postgresql --env="ALLOW_EMPTY_PASSWORD=yes" --env="PGPASSWORD=$PASSWORD" --env="PGUSER=postgres"

kubectl exec -i pgtesting -n postgresql -- bash -c "pg_dumpall -U postgres -h tavros-postgresql.postgresql.svc.cluster.local -w --clean" > backup.sql
```

To test a database where tables have been removed, take DROP commands from backup.sql and copy them into file called drop.sql and run that file separately. You may need to scale down gitea and kong in order to run without errors.


```
kubectl scale statefulsets gitea -n gitea --replicas=0

kubectl -n postgresql cp drop.sql pgtesting:/tmp/drop.sql

kubectl exec -i pgtesting -n postgresql -- bash -c "psql -U postgres -h tavros-postgresql.postgresql.svc.cluster.local -w -f /tmp/drop.sql"

kubectl scale statefulsets gitea -n gitea --replicas=1
```


#### Restore Postgres

```
kubectl -n postgresql cp backup.sql pgtesting:/tmp/backup.sql

kubectl exec -i pgtesting -n postgresql -- bash -c "psql -U postgres -h tavros-postgresql.postgresql.svc.cluster.local -w -f /tmp/backup.sql"
```

### Nexus

#### Back up Nexus

Set up backup task following the instructions in the reference article. Recommended backup location should be /nexus-data/backups.

Once task completes run these commands:
```
NEXUS_POD=$(kubectl get pods -n nexus -o jsonpath="{.items[0].metadata.name}")
# copy blobs to local directory
kubectl -n nexus cp $NEXUS_POD:nexus-data/blobs nexus-data/blobs
# copy node ids to local directory
kubectl -n nexus cp $NEXUS_POD:nexus-data/keystores/node nexus-data/keystores/node
# copy files from db backup task to local directory
kubectl -n nexus cp $NEXUS_POD:nexus-data/backups nexus-data/backups
```

Reference: https://help.sonatype.com/repomanager3/planning-your-implementation/backup-and-restore/prepare-a-backup

#### Restore Nexus

Scale down nexus/stop nexus:
```
kubectl scale --replicas=0 deployment/tavros-nexus-repository-manager -n nexus
```

Start another pod that uses the volume mount:

```
vi temp-nexus.yaml

apiVersion: v1
kind: Pod
metadata:
  name: temp-nexus
  namespace: nexus
spec:
  containers:
  - name: bash
    image: redhat/ubi9:9.2-696
    command: [ "/bin/bash", "-c", "--" ]
    args: [ "while true; do sleep 30; done;" ]
    volumeMounts:
    - mountPath: /nexus-data
      name: nexus-repository-manager-data
  serviceAccount: tavros-nexus-repository-manager
  serviceAccountName: tavros-nexus-repository-manager
  volumes:
  - name: nexus-repository-manager-data
    persistentVolumeClaim:
      claimName: tavros-nexus-repository-manager-data

kubectl apply -f temp-nexus.yaml

```

Once pod starts:

```
kubectl exec -i temp-nexus -n nexus -- bash -c "cd nexus-data/db && rm -rf component && rm -rf config && rm -rf security"
kubectl exec -i temp-nexus -n nexus -- bash -c "rm -rf nexus-data/blobs"
kubectl exec -i temp-nexus -n nexus -- bash -c "rm -rf nexus-data/keystores/node"

NEXUS_POD=temp-nexus
# copy blobs back to pv
kubectl -n nexus cp nexus-data/blobs $NEXUS_POD:nexus-data
# copy node ids back to pv
kubectl -n nexus cp nexus-data/keystores/node $NEXUS_POD:nexus-data/keystores
# copy files from db backup task back to pv
kubectl -n nexus cp nexus-data/backups/. $NEXUS_POD:nexus-data/restore-from-backup
```

Delete temp-nexus pod.

Scale nexus pod back up:
`kubectl scale --replicas=1 deployment/tavros-nexus-repository-manager -n nexus`

Verify nexus is working properly.

Then, delete backup files.

```
NEXUS_POD=$(kubectl get pods -n nexus -o jsonpath="{.items[0].metadata.name}")
kubectl exec -i $NEXUS_POD -n nexus -- bash -c "rm /nexus-data/restore-from-backup/*.bak"
kubectl exec -i $NEXUS_POD -n nexus -- bash -c "rm -rf /nexus-data/backups"
```

Reference: https://help.sonatype.com/repomanager3/planning-your-implementation/backup-and-restore/restore-exported-databases