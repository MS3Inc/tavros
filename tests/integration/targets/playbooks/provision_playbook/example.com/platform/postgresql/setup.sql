CREATE DATABASE "gitea";
CREATE USER "gitea" WITH ENCRYPTED PASSWORD 'placeholder8';
GRANT ALL PRIVILEGES ON DATABASE "gitea" TO "gitea";

CREATE DATABASE "keycloak";
CREATE USER "keycloak" WITH ENCRYPTED PASSWORD 'placeholder3';
GRANT ALL PRIVILEGES ON DATABASE "keycloak" TO "keycloak";

CREATE DATABASE "sandbox-kong";
CREATE USER "sandbox-kong" WITH ENCRYPTED PASSWORD 'placeholder1';
GRANT ALL PRIVILEGES ON DATABASE "sandbox-kong" TO "sandbox-kong";

CREATE DATABASE "prod-kong";
CREATE USER "prod-kong" WITH ENCRYPTED PASSWORD 'placeholder2';
GRANT ALL PRIVILEGES ON DATABASE "prod-kong" TO "prod-kong";

