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
 'read-version[toml]>=0.3.1,<0.4.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['backplane = backplane.main:app']}

setup_kwargs = {
    'name': 'backplane',
    'version': '0.4.1',
    'description': 'a dead-simple backplane for Dockerized applications',
    'long_description': '<div>\n  <img align="left" src="logo.png" width="175" alt="logo" />\n  <h1 align="left">backplane</h1>\n</div>\n\n**[Website](https://backplane.sh)** \xe2\x80\x94 **[Documentation](https://backplane.sh/docs)** \xe2\x80\x94 **[Source Code](https://github.com/wearep3r/backplane)**\n\nA dead-simple backplane for your Docker Compose services with free SSL and Git-based continuous delivery. No more friction between development and production environments.\n\n[!["Version"](https://img.shields.io/github/v/tag/wearep3r/backplane?label=version)](https://github.com/wearep3r/backplane)\n[!["p3r. Slack"](https://img.shields.io/badge/slack-@wearep3r/general-purple.svg?logo=slack&label=Slack)](https://join.slack.com/t/wearep3r/shared_invite/zt-d9ao21f9-pb70o46~82P~gxDTNy_JWw)\n\n---\n\n## Get started\n\n> \xf0\x9f\x9a\x80 Check out our [Examples](examples) section for quick-start templates for [Wordpress](examples/wordpress), [Sonarqube](examples/sonarqube) and more\n\n```bash\npip install backplane\nbackplane init\nbackplane up\n```\n\nYou can now visit the dashboards of Traefik and Portainer in your browser:\n\n- [Traefik Dashboard](http://traefik.127-0-0-1.nip.io)\n- [Portainer Dashboard](http://portainer.127-0-0-1.nip.io)\n\n## Configure your containers\n\nExposing one of your services through **backplane** is easy:\n\n- add it to the `backplane` Docker network \n- add a label `backplane.enabled` with value `true`\n\n**backplane** will automatically pick up the services\'s name (e.g. `whoami`) and exposes it as a subdomain of your **backplane domain** (defaults to `127-0-0-1.nip.io`).\n\n> **NOTE**: this assumes that your service is accessible on port 80 inside the container. If that is NOT the case, see [Advanced configuration](#-advanced-configuration)\n\n### docker-compose\n\n```yaml\nversion: "3.3"\n\nservices:\n  whoami:\n    image: "traefik/whoami"\n    container_name: "whoami"\n    networks:\n      - backplane\n    labels:\n      - "backplane.enabled=true"\n\nnetworks:\n  backplane:\n    name: backplane\n    external: true\n```\n\nYour container will be exposed as [http://whoami.127-0-0-1.nip.io](http://whoami.127-0-0-1.nip.io).\n\n## Use in production\n\n**backplane** can be used on public cloud hosts, too. Simply change `--environment` to `production` and add a mail address for LetsEncrypt. An optional `--domain` can be set on installation (defaults to `$SERVER_IP.nip.io`, e.g. `193-43-54-23.nip.io`).\n\n```bash\nbackplane install --environment production --mail letsencrypt@mydomain.com [--domain mydomain.com]\nbackplane start\n```\n\nThis enables the following additional features:\n\n- access your backplane services as subdomains of `mydomain.com`\n- automatic SSL for your containers through LetsEncrypt (HTTP-Validation)\n- automatic HTTP to HTTPS redirect\n- sane security defaults\n\n```yaml\nversion: "3.3"\n\nservices:\n  whoami:\n    image: "traefik/whoami"\n    container_name: "whoami"\n    networks:\n      - backplane\n    labels:\n      - "backplane.enabled=true"\n\nnetworks:\n  backplane:\n    name: backplane\n    external: true\n```\n\nYour container will be exposed as [https://whoami.mydomain.com](https://whoami.mydomain.com).\n\n## Deploy to backplane\n\n`git push` your code to the built-in **runner** for dead-simple auto-deployment of your Docker Compose Service. The runner deploys whatever you define in the repository\'s `docker-compose.yml` file and can load additional environment variables from a `.env` file.\n\n### Update your ssh config\n\nAdd the following to your local `~/.ssh/config` file. This allows you to reach the runner under `backplane` without further configuration.\n\n```bash\nHost backplane\n    HostName 127.0.0.1\n    User backplane\n    Port 2222\n```\n\n> **NOTE**: replace "HostName" with your server\'s IP if you\'re running in production\n\n### Update your git remote\n\nAssuming your repository is called `whoami`, this is how you add the **backplane runner** to your git remotes:\n\n```bash\ngit remote add origin "git@backplane:whoami"\n```\n\n### Deploy to your server\n\n```bash\ngit commit -am "feat: figured out who I am"\ngit push backplane master\n```\n\nThat\'s it! **backplane** will build and deploy your application and expose it automatically.\n\n## What is backplane\n\n**backplane** consists of 3 main services:\n\n- [Traefik](#), a very popular, cloud-native reverse-proxy\n- [Portainer](#), a very popular management interface for Docker\n- [backplane Runner](#), a simple Continuous Delivery server\n\nIt aims to provide simple access to core prerequisites of modern app development:\n\n- Endpoint exposure\n- Container management\n- Deployment workflows\n\nTo develop and run modern web-based applications you need a few core ingredients, like a reverse-proxy handling request routing, a way to manage containers and a way to deploy your code. **backplane** offers this for local development as well as on production nodes in a seemless way.\n\nThe runner makes it easy to bypass long CI pipelines and deploy your application to a remote backplane host with ease. \n\n**backplane** is mainly aimed at small to medium sized development teams or solo-developers that don\'t require complex infrastructure. Use it for rapid prototyping or simple deployment scenarios where the full weight of modern CI/CD offerings just isn\'t bearable.\n\nYou can migrate from local development to production with a simple `git push` when using **backplane** on both ends. Think of it as a micro-PaaS that you can use locally.\n\n## Advanced configuration\n\n**backplane** is only a thin wrapper around Traefik. If you require more complex routing scenarios or have more complex service setups (e.g. multiple domains per container), simply use Traefik\'s label-based configuration.\n\n[Read more](https://doc.traefik.io/traefik/) in the docs.\n\n### Expose containers with non-standard ports\n\n**backplane** expects your services to listen to port 80 inside their containers. If that is not the case, you need to tell the backplane about it. Add the following additional labels to tell backplane your service is accessible on port 9000:\n\n```yaml\nlabels:\n  - backplane.enabled=true\n  - "traefik.http.routers.custom.service=custom-http"\n  - "traefik.http.services.custom-http.loadbalancer.server.port=9000"\n```\n\n## Examples\n\nIn the [examples](examples) directory you\'ll find examples showing how to integrate backplane with your existing services\n\nChange to any of the example folders and run `docker-compose up`. The example\'s `README` will hold additional information on how to use it.\n\n## Development\n\n### Dependencies\n\n```bash\npip install poetry\npoetry shell\npoetry install\n```\n\n### Build\n\n```bash\npoetry build\n```\n\n### Generate release\n\n```bash\nsemantic-release version\n```\n\n### Publish release\n\n```bash\nsemantic-release publish\n```',
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
