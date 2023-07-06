### Manual Backups

## Backup Postgres

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


## Restore Postgres

```
kubectl -n postgresql cp backup.sql pgtesting:/tmp/backup.sql

kubectl exec -i pgtesting -n postgresql -- bash -c "psql -U postgres -h tavros-postgresql.postgresql.svc.cluster.local -w -f /tmp/backup.sql"
```