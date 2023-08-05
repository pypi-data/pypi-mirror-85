# backplane

A simple backplane for your containerized applications.

- [Traefik](https://doc.traefik.io/traefik/getting-started/quick-start/) reverse-proxy for your containers
- [Portainer](https://www.portainer.io/) management dashboard for Docker

## Get started

```bash
pip install backplane
backplane install
backplane start
```

You can now visit the dashboards of both services in your browser:

- [Traefik Dashboard](http://traefik.here.ns0.co)
- [Portainer Dashboard](http://portainer.here.ns0.co)

## Configure your containers

To expose one of your services through Traefik, your service needs to be part of the `backplane` Docker network and carry a few Traefik-relevant labels:

### docker

```bash
docker run \
--network backplane \
--label "traefik.enable=true" \
--label "traefik.http.routers.whoami.rule=Host(\`whoami.here.ns0.co\`)" \
--label "traefik.http.routers.whoami.entrypoints=http" \
--rm traefik/whoami
```

Visit http://whoami.here.ns0.co to verify it worked.

### docker-compose

```bash
version: "3.3"

services:
  whoami:
    image: "traefik/whoami"
    container_name: "simple-service"
    networks:
      - backplane
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.whoami.rule=Host(`whoami.here.ns0.co`)"
      - "traefik.http.routers.whoami.entrypoints=http"

networks:
  backplane:
    name: backplane
    external: true
```

Visit http://whoami.here.ns0.co to verify it worked.

## Development

### Dependencies

```bash
pip install poetry
poetry shell
poetry install
npm i -g standard-version
```

### Build

```bash
poetry build
```

### Publish

```bash
poetry publish
```