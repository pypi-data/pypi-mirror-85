# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_django']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1,<4.0', 'strawberry-graphql>=0.41,<0.42']

setup_kwargs = {
    'name': 'strawberry-graphql-django',
    'version': '0.0.4',
    'description': 'Strawberry GraphQL Django extension',
    'long_description': '# Strawberry GraphQL Django extension\n\nThis library provides helpers to generate fields, mutations and resolvers for Django models.\n\n## Sample project files\n\nmodels.py:\n```python\nfrom django.db import models\n\nclass User(models.Model):\n    name = models.CharField(max_length=50)\n    age = models.IntegerField()\n    groups = models.ManyToManyField(\'Group\', related_name=\'users\')\n\nclass Group(models.Model):\n    name = models.CharField(max_length=50)\n```\n\nschema.py:\n```python\nimport strawberry\nfrom strawberry_django import ModelResolver, ModelPermissions\nfrom .models import User, Group\n\nclass UserResolver(ModelResolver):\n    model = User\n    @strawberry.field\n    def age_in_months(info, root) -> int:\n        return root.age * 16\n\nclass GroupResolver(ModelResolver):\n    model = Group\n    fields = [\'name\', \'users\']\n    # only users who have permissions for group models can access and modify\n    permissions_classess = [ModelPermissions]\n    def get_queryset(self):\n        qs = super().get_queryset()\n        if not self.request.user.is_superuser:\n            qs = qs.none()\n        return qs\n\n@strawberry.type\nclass Query(UserResolver.query(), GroupResolver.query()):\n    pass\n\n@strawberry.type\nclass Mutation(UserResolver.mutation(), GroupResolver.mutation()):\n    pass\n\nschema = strawberry.Schema(query=Query, mutation=Mutation)\n```\n\nurls.py:\n```python\nfrom strawberry.django.views import GraphQLView\nfrom .schema import schema\n\nurlpatterns = [\n    path(\'graphql\', GraphQLView.as_view(schema=schema)),\n]\n```\n\nAdd models and schema. Create database. Start development server.\n```shell\npip install strawberry-graphql-django\nmanage.py makemigrations\nmanage.py migrate\nmanage.py runserver\n```\n\n## Mutations and Queries\n\nOpen http://localhost:8000/graphql and start testing.\n\nCreate new user.\n```\nmutation {\n  createUser(data: {name: "my user", age: 20}) {\n    id\n  }\n}\n```\n\nMake first queries.\n```\nquery {\n  user(id: 1) {\n    name\n    age\n    groups {\n        name\n    }\n  }\n  users(filters: ["name__contains=my", "!age__gt=60"]) {\n    id\n    name\n    age_in_months\n  }\n}\n```\n\nUpdate user data.\n```\nmutation {\n  updateUsers(data: {name: "new name"}, filters: ["id=1"]) {\n    id\n    name\n  }\n}\n```\n\nFinally delete user.\n```\nmutation {\n  deleteUsers(filter: ["id=1"]) {\n    id\n  }\n}\n```\n\n## Contribution\n\nI would be more than happy to get pull requests, improvement ideas or any feedback.\n',
    'author': 'Lauri Hintsala',
    'author_email': 'lauri.hintsala@verkkopaja.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/la4de/strawberry-graphql-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
