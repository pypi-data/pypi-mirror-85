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
    'version': '0.1.22',
    'description': 'a dead-simple backplane for Dockerized applications',
    'long_description': '# backplane\n\nA dead-simple backplane for your Docker containers.\n\n- [Traefik](https://doc.traefik.io/traefik/getting-started/quick-start/) reverse-proxy for your containers\n- [Portainer](https://www.portainer.io/) management dashboard for Docker\n\n## Get started\n\n```bash\npip install backplane\nbackplane install\nbackplane start\n```\n\nYou can now visit the dashboards of both services in your browser:\n\n- [Traefik Dashboard](http://traefik.here.ns0.co)\n- [Portainer Dashboard](http://portainer.here.ns0.co)\n\n## Configure your containers\n\nTo expose one of your services through Traefik, your service needs to be part of the `backplane` Docker network and carry a few Traefik-relevant labels:\n\n### docker\n\n```bash\ndocker run \\\n--network backplane \\\n--label "traefik.enable=true" \\\n--label "traefik.http.routers.whoami.rule=Host(\\`whoami.here.ns0.co\\`)" \\\n--label "traefik.http.routers.whoami.entrypoints=http" \\\n--rm traefik/whoami\n```\n\nVisit http://whoami.here.ns0.co to verify it worked.\n\n### docker-compose\n\n```bash\nversion: "3.3"\n\nservices:\n  whoami:\n    image: "traefik/whoami"\n    container_name: "simple-service"\n    networks:\n      - backplane\n    labels:\n      - "traefik.enable=true"\n      - "traefik.http.routers.whoami.rule=Host(`whoami.here.ns0.co`)"\n      - "traefik.http.routers.whoami.entrypoints=http"\n      - "traefik.docker.network=backplane"\n\nnetworks:\n  backplane:\n    name: backplane\n    external: true\n```\n\nVisit http://whoami.here.ns0.co to verify it worked.\n\n## Use in production\n\n**backplane** can be used on public cloud hosts, too:\n\n```bash\nbackplane install --environment production --domain mydomain.com --mail letsencrypt@mydomain.com\nbackplane start\n```\n\nThis enables the following additional features:\n\n- access your backplane services through `mydomain.com` (NOTE: if you do not specify a domain, **backplane** will use a wildcard domain based on the IP of your server, like 127-0-0-1.nip.io)\n- automatic SSL for your containers through LetsEncrypt\n- configurable HTTP to HTTPS redirect\n- sane security defaults\n\n### docker\n\n```bash\ndocker run \\\n--network backplane \\\n--label "traefik.enable=true" \\\n--label "traefik.http.routers.whoami.rule=Host(\\`whoami.here.ns0.co\\`)" \\\n--label "traefik.http.routers.whoami.entrypoints=http" \\\n--label "traefik.http.routers.whoami.middlewares=compress@docker" \\\n--label "traefik.http.routers.whoami.middlewares=https-redirect@docker" \\\n--label "traefik.http.routers.whoami-secure.entrypoints=https" \\\n--label "traefik.http.routers.whoami-secure.rule=Host(\\`whoami.mydomain.com\\`)" \\\n--label "traefik.http.routers.whoami-secure.tls=true" \\\n--label "traefik.http.routers.whoami-secure.tls.certresolver=letsencrypt" \\\n--label "traefik.http.routers.whoami-secure.middlewares=secured@docker" \\\n--label "traefik.http.routers.whoami-secure.middlewares=compress@docker" \\\n--rm traefik/whoami\n```\n\n### docker-compose\n\n```bash\nversion: "3.3"\n\nservices:\n  whoami:\n    image: "traefik/whoami"\n    container_name: "simple-service"\n    networks:\n      - backplane\n    labels:\n      - "traefik.enable=true"\n      - "traefik.http.routers.whoami.entrypoints=http"\n      - "traefik.http.routers.whoami.rule=Host(`whoami.mydomain.com`)"\n      - "traefik.http.routers.whoami.middlewares=compress@docker"\n      - "traefik.http.routers.whoami.middlewares=https-redirect@docker"\n      - "traefik.http.routers.whoami-secure.entrypoints=https"\n      - "traefik.http.routers.whoami-secure.rule=Host(`whoami.mydomain.com`)"\n      - "traefik.http.routers.whoami-secure.tls=true"\n      - "traefik.http.routers.whoami-secure.tls.certresolver=letsencrypt"\n      - "traefik.http.routers.whoami-secure.middlewares=secured@docker"\n      - "traefik.http.routers.whoami-secure.middlewares=compress@docker"\n      - "traefik.docker.network=backplane"\n\nnetworks:\n  backplane:\n    name: backplane\n    external: true\n```\n\n## Use the Runner\n\n### Update your ssh config\n\nAdd the following to `~/.ssh/config`. This allows you to reach the runner under `backplane` without further configuration.\n\n```bash\nHost backplane\n    HostName 127.0.0.1\n    User backplane\n    Port 2222\n```\n\n### Update your git remote\n\nAssuming your repository is called `myapp`, this is how you add the **backplane** runner to your git remotes:\n\n```bash\ngit remote add origin "git@backplane:myapp"\n```\n\n## Development\n\n### Dependencies\n\n```bash\npip install poetry\npoetry shell\npoetry install\nnpm i -g standard-version\n```\n\n### Build\n\n```bash\npoetry build\n```\n\n### Publish\n\n```bash\npoetry publish\n```',
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
