from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.models import Count
from accounts.models import CustomUser
from characteristics.models import CalculatedCharacteristic, SupportedCharacteristic
from goals.serializers import GoalSerializer
from goals.tests.test_goal_endpoints import User
# from django.contrib.auth.models import User
from measures.models import CalculatedMeasure, SupportedMeasure

from metrics.models import CollectedMetric, SupportedMetric
from organizations.management.commands.utils import get_random_goal_data
from organizations.models import Organization, Product, Repository
from sqc.models import SQC
from subcharacteristics.models import CalculatedSubCharacteristic, SupportedSubCharacteristic
from utils import get_random_datetime, get_random_path, get_random_qualifier, get_random_value
from django.utils import timezone

import datetime as dt


class Command(BaseCommand):

    def _get_admin(self):
        get_user_model().objects.filter(email='admin@admin.com')

    def create_a_goal(self, product: Product, user: User):
        pre_config = product.pre_configs.first()
        data = get_random_goal_data(pre_config)
        serializer = GoalSerializer(data=data)
    
        class MockView:
            @staticmethod
            def get_product():
                return product
    
        serializer.context['view'] = MockView
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product, created_by=user)


    def create_fake_sqc_data(self, repository):
        qs = SQC.objects.filter(repository=repository)

        MIN_NUMBER = 50

        if qs.count() >= MIN_NUMBER:
            return

        SQC.objects.bulk_create([
            SQC(value=get_random_value('PERCENT'),
                repository=repository,
                )
            for _ in range(MIN_NUMBER - qs.count())
        ])


    def create_fake_organizations(self):
        organizations = [
            Organization(
                name='fga-eps-mds',
                description=((
                    "Organização que agrupa os "
                    "projetos de EPS e MDS da FGA."
                )),
            # remove this line: members=self._get_admin(),
            ),
        ]

        for organization in organizations:
            if Organization.objects.filter(name=organization.name).exists():
                continue
            organization.save()
            # Assign members after saving the instance.
            organization.members.set([self._get_admin()])

    def create_fake_products(self):
        organizations = Organization.objects.all()

        organizations = {
            organization.name: organization
            for organization in organizations
        }

        products = [
            Product(
                name='MeasureSoftGram',
                description=(
                    "Este projeto que visa a construção de um "
                    "sistema de análise quantitativa da qualidade "
                    "de um sistema de software."
                ),
                organization=organizations['fga-eps-mds'],
            ),
            # Product(
            #     name='Acacia',
            #     description=(
            #         "Este projeto que visa a construção de um "
            #         "sistema de colaboração de colheita de "
            #         "árvores frutíferas em ambiente urbano."
            #     ),
            #     organization=organizations['fga-eps-mds'],
            # ),
        ]

        for product in products:
            if Product.objects.filter(
                name=product.name,
                organization=product.organization,
            ).exists():
                continue
            product.save()

    def create_fake_repositories(self):
        products = Product.objects.all()

        products = {
            product.name: product
            for product in products
        }

        repositories = [
            # Repository(
            #     name='2019.2-Acacia',
            #     description=(
            #         "Repositório do backend do projeto Acacia."
            #     ),
            #     product=products['Acacia'],
            # ),
            # Repository(
            #     name='2019.2-Acacia-Frontend',
            #     description=(
            #         "Repositório do frontend do projeto Acacia."
            #     ),
            #     product=products['Acacia'],
            # ),
            # Repository(
            #     name='2019.2-Acacia-Frontend',
            #     description=(
            #         "Repositório do frontend do projeto Acacia."
            #     ),
            #     product=products['Acacia'],
            # ),
            # Repository(
            #     name='2020.1-BCE',
            #     description=(
            #         "Repositório do projeto BCE UnB."
            #     ),
            #     product=products['BCE UnB'],
            # ),
            # Repository(
            #     name='2021.1_G01_Animalesco_BackEnd',
            #     description=(
            #         "Repositório do backend do projeto Animalesco."
            #     ),
            #     product=products['Animalesco'],
            # ),
            # Repository(
            #     name='2021.1_G01_Animalesco_FrontEnd',
            #     description=(
            #         "Repositório do frontend "
            #         "do projeto Animalesco."
            #     ),
            #     product=products['Animalesco'],
            # ),
            Repository(
                name='2022-1-MeasureSoftGram-Service',
                description=(
                    "Repositório do backend do projeto "
                    "MeasureSoftGram."
                ),
                product=products['MeasureSoftGram'],
            ),
            Repository(
                name='2022-1-MeasureSoftGram-Core',
                description=(
                    "Repositório da API do modelo matemático "
                    "do projeto MeasureSoftGram"
                ),
                product=products['MeasureSoftGram'],
            ),
            Repository(
                name='2022-1-MeasureSoftGram-Front',
                description=(
                    "Repositório do frontend da projeto "
                    "MeasureSoftGram"
                ),
                product=products['MeasureSoftGram'],
            ),
            Repository(
                name='2022-1-MeasureSoftGram-CLI',
                description=(
                    "Repositório do CLI da projeto "
                    "MeasureSoftGram"
                ),
                product=products['MeasureSoftGram'],
            ),
        ]

        for repository in repositories:
            if Repository.objects.filter(
                name=repository.name,
                product=repository.product,
            ).exists():
                continue
            repository.save()

    def create_fake_calculated_characteristics(self, repository):
        qs = SupportedCharacteristic.objects.annotate(
            qty=Count('calculated_characteristics'),
        )

        def calculated_entity_factory(entity, created_at):
            return CalculatedCharacteristic(
                characteristic=entity,
                value=get_random_value('PERCENT'),
                created_at=created_at,
                repository=repository,
            )

        def get_entity_qty(entity):
            return entity.calculated_characteristics.filter(
                repository=repository,
            ).count()

        self.create_fake_calculated_entity(
            qs,
            calculated_entity_factory,
            CalculatedCharacteristic,
            get_entity_qty,
        )

    def create_fake_calculated_subcharacteristics(self, repository):
        qs = SupportedSubCharacteristic.objects.annotate(
            qty=Count('calculated_subcharacteristics'),
        )

        def calculated_entity_factory(entity, created_at):
            return CalculatedSubCharacteristic(
                subcharacteristic=entity,
                value=get_random_value('PERCENT'),
                created_at=created_at,
                repository=repository,
            )

        def get_entity_qty(entity):
            return entity.calculated_subcharacteristics.filter(
                repository=repository,
            ).count()

        self.create_fake_calculated_entity(
            qs,
            calculated_entity_factory,
            CalculatedSubCharacteristic,
            get_entity_qty,
        )

    def create_fake_calculated_measures(self, repository):

        qs = SupportedMeasure.objects.all()

        def calculated_entity_factory(entity, created_at):
            return CalculatedMeasure(
                measure=entity,
                value=get_random_value('PERCENT'),
                created_at=created_at,
                repository=repository,
            )

        def get_entity_qty(entity):
            return entity.calculated_measures.filter(
                repository=repository,
            ).count()

        self.create_fake_calculated_entity(
            qs,
            calculated_entity_factory,
            CalculatedMeasure,
            get_entity_qty,
        )

    def create_fake_collected_metrics(self, repository):
        qs = SupportedMetric.objects.all()

        def calculated_entity_factory(entity, created_at):
            metric_type = entity.metric_type
            value = get_random_value(metric_type)

            return CollectedMetric(
                metric=entity,
                path=get_random_path(),
                qualifier=get_random_qualifier(),
                value=value,
                created_at=created_at,
                repository=repository,
            )

        def get_entity_qty(entity):
            return entity.collected_metrics.filter(
                repository=repository,
            ).count()

        self.create_fake_calculated_entity(
            qs,
            calculated_entity_factory,
            CollectedMetric,
            get_entity_qty,
        )

    def create_fake_calculated_entity(
        self,
        qs,
        calculated_entity_factory,
        bulk_create_klass,
        get_entity_qty,
    ):

        end_date = timezone.now()
        start_date = end_date - dt.timedelta(days=90)

        MIN_NUMBER_OF_CALCULATED_ENTITIES = 50
        MIN_NUMBER = MIN_NUMBER_OF_CALCULATED_ENTITIES

        fake_calculated_entities = []

        for entity in qs:
            qty = get_entity_qty(entity)

            if qty < MIN_NUMBER:
                for _ in range(MIN_NUMBER - qty):
                    created_at = get_random_datetime(start_date, end_date)
                    fake_calculated_entities.append(
                        calculated_entity_factory(entity, created_at),
                    )

        bulk_create_klass.objects.bulk_create(fake_calculated_entities)

    # def handle(self, *args, **options):

    #     self.create_fake_organizations()
    #     self.create_fake_products()
    #     self.create_fake_repositories()

    #     repositories = Repository.objects.all()

    #     for repository in repositories:
    #         self.create_fake_collected_metrics(repository)
    #         self.create_fake_calculated_measures(repository)
    #         self.create_fake_calculated_subcharacteristics(repository)
    #         self.create_fake_calculated_characteristics(repository)
    #         self.create_fake_sqc_data(repository)

    #     products = Product.objects.all()

    #     for product in products:
    #         self.create_a_goal(product)
    def handle(self, *args, **options):
    
        self.create_fake_organizations()
        self.create_fake_products()
        self.create_fake_repositories()
    
        repositories = Repository.objects.all()
    
        for repository in repositories:
            self.create_fake_collected_metrics(repository)
            self.create_fake_calculated_measures(repository)
            self.create_fake_calculated_subcharacteristics(repository)
            self.create_fake_calculated_characteristics(repository)
            self.create_fake_sqc_data(repository)
    
        products = Product.objects.all()
    
        # Get the first user in the database
        user = CustomUser.objects.first()
    
        for product in products:
            self.create_a_goal(product, user)
