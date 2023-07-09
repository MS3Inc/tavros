HIGH PRIORITY
- [ ] Test service mesh working (need services on pod if not using helm release)
- [ ] Fix flux/helm issue, can't deploy apps with normal helm release (error is: "HelmChart 'flux-system/prod-test-proj' is not ready")
- [ ] Fix ErrImagePull from nexus?
- [ ] Fix prod and sandbox Kong keycloak issues

MED PRIORITY
- [ ] Figure out Elasticsearch backup
- [ ] Fix Jenkins, issue with keycloak, issue with setup
- [ ] Fix issue with nexus and keycloak

LOW PRIORITY
- [ ] Fix Jaeger

------------------------------------
COMPLETE
- [x] Figure out backups of  postgres
- [x] Figure out backups of nexus
- [x] Update Keycloak operator to 18.0.0+ (not totally working though)
- [x] Update Jenkins operator to v0.7.0+
- [x] Update ECK to 2.5 +
- [x] Update Kong to 2.15.0/3.0.0.0
- [x] Update miscellaneous apiVersion stuff
- [x] Figure out normal sequence of logging into Kong
- [x] Figure out previous expected roles/account settings in keycloak

NOT DOING
- [ ] Figure out backups of etcd