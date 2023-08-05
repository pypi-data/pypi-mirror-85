# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backplane']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'anyconfig>=0.9.11,<0.10.0',
 'docker-compose>=1.27.4,<2.0.0',
 'docker>=4.3.1,<5.0.0',
 'packaging>=20.4,<21.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['backplane = backplane.main:app']}

setup_kwargs = {
    'name': 'backplane',
    'version': '0.1.11',
    'description': 'a dead-simple backplane for Dockerized applications',
    'long_description': '# backplane\n\nA simple backplane for your containerized applications.\n\n- [Traefik](https://doc.traefik.io/traefik/getting-started/quick-start/) reverse-proxy for your containers\n- [Portainer](https://www.portainer.io/) management dashboard for Docker\n\n## Get started\n\n```bash\ngit clone https://gitlab.com/p3r.one/backplane $HOME/.backplane\ncd $HOME/.backplane\ndocker-compose --project-name backplane up -d\n```\n\nYou can now visit the dashboards of both services in your browser:\n\n- [Traefik Dashboard](http://traefik.here.ns0.co)\n- [Portainer Dashboard](http://portainer.here.ns0.co)\n\nTo expose one of your services through Traefik, your service needs to be part of the `backplane` Docker network and carry a few Traefik-relevant labels:\n\n```bash\nportainer:\n  image: portainer/portainer-ce:2.0.0\n  container_name: portainer\n  command: -H unix:///var/run/docker.sock\n  restart: unless-stopped\n  security_opt:\n    - no-new-privileges:true\n  networks:\n    - backplane\n  volumes:\n    - "/var/run/docker.sock:/var/run/docker.sock:ro"\n    - "portainer-data:/data"\n  labels:\n    - "traefik.enable=true"\n    - "traefik.http.routers.portainer.entrypoints=http"\n    - "traefik.http.routers.portainer.rule=Host(`portainer.${BACKPLANE_DOMAIN}`)"\n    - "traefik.http.routers.traefik.middlewares=compress@file"\n    - "traefik.http.routers.portainer.service=portainer"\n    - "traefik.http.services.portainer.loadbalancer.server.port=9000"\n    - "traefik.docker.network=backplane"\n```\n\n## Development\n\n### Dependencies\n\n```bash\npip install poetry\npoetry shell\npoetry install\nnpm i -g standard-version\n```\n\n### Build\n\n```bash\npoetry build\n```\n\n### Publish\n\n```bash\npoetry publish\n```',
    'author': 'Fabian Peter',
    'author_email': 'fabian@p3r.link',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
