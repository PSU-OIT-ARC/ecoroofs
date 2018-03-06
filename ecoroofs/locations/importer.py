import csv
import re
import time
from decimal import Decimal
from sys import stderr

from . import models


# Map of CSV field names => model field names.
FIELD_NAME_MAP = {
    'Project': 'name',
    'Address': 'address',
    'Address (Obscured)': 'address_obscured',
    'Address_Clean': '',
    'Watershed': '',
    'Building Use': '',
    'Solar over Ecoroof': 'solar_over_ecoroof',
    'Type': 'construction_type',
    'Year Built': 'year_built',
    'Size (sf)': 'square_footage',
    'Number': 'number_of_roofs',
    'Latitude(Non Obscured)': 'latitude',
    'Longitude (Non Obscured)': 'longitude',
    'Confidence (Non Obscured)': 'confidence',
    'Latitude': 'latitude_obscured',
    'Longitude': 'longitude_obscured',
    'Confidence': 'confidence_obscured',
    'Depth Min': 'depth_min',
    'Depth Max': 'depth_max',
    'Cost': '',
    'Composition': '',
    'Irrigation': 'irrigated',
    'Drainage': '',
    'Plants': '',
    'Maintenance': '',
    'Contractor': '',
}


class CSVDictReader(csv.DictReader):

    @property
    def fieldnames(self):
        names = super().fieldnames
        for i, name in enumerate(names):
            names[i] = FIELD_NAME_MAP.get(name) or self.clean_field_name(name)
        for name in names:
            assert name.isidentifier(), '%s must be a valid identifier' % name
        return names

    def clean_field_name(self, name):
        name = name.lower()
        name = re.sub(r'[^a-z0-9_\s]', '', name)
        name = re.sub(r'\s+', '_', name)
        return name

    def iter_rows(self):
        for row in iter(self):
            row = {k: (v.strip() or None) for (k, v) in row.items()}
            yield row


class Importer:

    """Import locations and related data from CSV file.

    Args:
        file_name: Path to CSV file

    """

    def __init__(self, file_name, overwrite=False, dry_run=False, quiet=False):
        self.file_name = file_name
        self.overwrite = overwrite
        self.dry_run = dry_run
        self.real_run = not dry_run
        self.quiet = quiet

    def do_overwrite(self):
        models_to_delete = (
            models.Location,
            models.BuildingUse,
            models.Confidence,
            models.ConstructionType,
            models.Contractor,
            models.Watershed,
        )
        for model in models_to_delete:
            print('Removing existing {model._meta.verbose_name_plural}...'.format(**locals()))
            if self.real_run:
                model.objects.all().delete()

    def read_data(self):
        with open(self.file_name) as fp:
            reader = CSVDictReader(fp)
            data = list(reader.iter_rows())
        return data

    def as_bool(self, value, true_values=('yes',), false_values=('no',), null=False):
        if value is None:
            return None
        value = value.strip().lower()
        if not value:
            return None
        if value in true_values:
            return True
        if value in false_values:
            return False
        raise ValueError('{value} not in specified true or false values'.format_map(locals()))

    def normalize_name(self, name):
        # Applies the following transformations to normalize a name:
        #
        #     - Collapse contiguous whitespace into a single space
        #     - Convert name to title case if it doesn't already appear
        #       to be title-cased.
        name = re.sub(r'\s+', ' ', name)
        name = name.title() if name[0].islower() else name
        return name

    def choice(self, row, field, choices, null=False):
        value = row[field]
        if value is None:
            if null:
                return None
            raise ValueError('Expected a value for {field} in {row}'.format_map(locals()))
        value = self.normalize_name(value)
        try:
            value = choices[value]
        except KeyError:
            raise ValueError(
                '{value} is not one of the available choices for {field}; '
                'available choices: {choices}'
                .format_map(locals()))
        return value

    def insert_locations(self, data):
        locations = []
        building_uses = {r.name: r for r in models.BuildingUse.objects.all()}
        contractors = {r.name: r for r in models.Contractor.objects.all()}
        watersheds = {r.name: r for r in models.Watershed.objects.all()}
        construction_types = {r.name: r for r in models.ConstructionType.objects.all()}
        confidences = {r.name: r for r in models.Confidence.objects.all()}

        # Used to keep track of names already used so we can ensure each
        # location has a unique name and slug.
        names = set()

        for row in data:
            name = row['name']

            if name is None:
                print('Project name not set for location: {row}; skipping'.format_map(locals()))
                continue

            name = self.normalize_name(name)

            i = 1
            base_name = name
            while name in names:
                name = '{base_name} {i}'.format_map(locals())
                i += 1

            names.add(name)

            # Addresses
            address = row['address']
            if address is None:
                print('Address is not set for location "{name}"'.format_map(locals()))
            else:
                address = self.normalize_name(address)
            address_obscured = row['address_obscured']
            if address_obscured is None:
                print(
                    'Address (Obscured) is not set for location "{name}"'
                    .format_map(locals()))
            else:
                address_obscured = self.normalize_name(address_obscured)

            # Text fields
            composition = row['composition']
            drainage = row['drainage']
            maintenance = row['maintenance']
            plants = row['plants']

            # Booleans
            irrigated = self.as_bool(row['irrigated'], null=True)
            solar_over_ecoroof = self.as_bool(row['solar_over_ecoroof'], null=True)

            # Numeric fields
            depth_min = row['depth_min']
            if depth_min is None:
                print('Depth Min is not set for location "{name}"'.format_map(locals()))
            else:
                depth_min = Decimal(depth_min)

            depth_max = row['depth_max']
            if depth_max is None:
                print('Depth Max is not set for location "{name}"'.format_map(locals()))
            else:
                depth_max = Decimal(depth_max)

            number_of_roofs = row['number_of_roofs']
            if number_of_roofs is None:
                print(
                    'Number of roofs not set for location "{name}" Using default value'
                    .format_map(locals()))
                field = models.Location._meta.get_field('number_of_roofs')
                number_of_roofs = field.get_default()
            else:
                number_of_roofs = int(number_of_roofs)

            square_footage = row['square_footage']
            if square_footage is None:
                print('Square footage not set for location "{name}"'.format_map(locals()))
            else:
                square_footage, *rest = square_footage.split(None, 1)
                if rest:
                    print(
                        'Extraneous data in square footage for location "{name}": {rest[0]}'
                        .format_map(locals()))
                square_footage = int(square_footage)

            year_built = row['year_built']
            if year_built is None:
                print(
                    'Year Built not set for location "{name}"'
                    .format_map(locals()))
            else:
                year_built = int(year_built)

            # Related fields
            building_use = self.choice(row, 'building_use', building_uses)
            confidence = self.choice(row, 'confidence', confidences, null=True)
            construction_type = self.choice(row, 'construction_type', construction_types,
                null=True)
            contractor = self.choice(row, 'contractor', contractors, null=True)
            watershed = self.choice(row, 'watershed', watersheds, null=True)

            # Actual coordinates
            coordinates = {'x': row['longitude'], 'y': row['latitude']}
            point = 'POINT({x} {y})'.format_map(coordinates)
            if coordinates['x'] is None or coordinates['y'] is None:
                print(
                    'Coordinates not set for location "{name}": {point}; skipping'
                    .format_map(locals()))
                continue

            # Obscured coordinates
            coordinates = {'x': row['longitude_obscured'], 'y': row['latitude_obscured']}
            point_obscured = 'POINT({x} {y})'.format_map(coordinates)
            if coordinates['x'] is None or coordinates['y'] is None:
                print(
                    'Obscured coordinates not set for location "{name}": {point_obscured}; skipping'
                    .format_map(locals()))
                continue

            location = models.Location(
                address=address,
                address_obscured=address_obscured,
                building_use=building_use,
                composition=composition,
                confidence=confidence,
                construction_type=construction_type,
                contractor=contractor,
                depth_min=depth_min,
                depth_max=depth_max,
                drainage=drainage,
                irrigated=irrigated,
                maintenance=maintenance,
                name=name,
                number_of_roofs=number_of_roofs,
                plants=plants,
                point=point,
                point_obscured=point_obscured,
                solar_over_ecoroof=solar_over_ecoroof,
                square_footage=square_footage,
                watershed=watershed,
                year_built=year_built,
            )
            location.set_neighborhood_automatically()
            locations.append(location)

        num_locations = len(locations)
        print('Creating', num_locations, 'locations...', end='')
        if self.real_run:
            models.Location.objects.bulk_create(locations)
        print('Done')

    def column_to_table(self, data, model, from_field_name=None, to_field_name='name'):
        """Take column values for field from data and insert into table.

        Args:
            data: A list of dicts
            model: A Django model class
            from_field_name: Field to extract values from (derived from ``model``
                if not specified)
            to_field_name: Model field name to set

        """
        model_name = model._meta.verbose_name
        if from_field_name is None:
            from_field_name = model_name.replace(' ', '_')

        print('Extracting', model_name, 'values...')
        values = {row[from_field_name] for row in data}
        values = {value for value in values if value is not None}
        values = {self.normalize_name(value) for value in values}
        num_values = len(values)
        print('Found', num_values, 'distinct, non-empty', model_name, 'values:')
        for value in sorted(values):
            print('    "{}"'.format(value))
        print('Done extracting', model_name, 'values')

        records = [model(**{to_field_name: value}) for value in values if value]
        num_records = len(records)
        print('Inserting', num_records, model_name, 'records...', end='')
        if self.real_run:
            model.objects.bulk_create(records)
        print('Done')

    def run(self):
        if self.overwrite:
            self.do_overwrite()
        elif models.Location.objects.count():
            print('Importing locations without removing existing records.', file=stderr)
            print('This will likely FAIL due to duplicate key violations.', file=stderr)
            time.sleep(5)
        data = self.read_data()
        self.column_to_table(data, models.BuildingUse)
        self.column_to_table(data, models.Confidence)
        self.column_to_table(data, models.ConstructionType)
        self.column_to_table(data, models.Contractor)
        self.column_to_table(data, models.Watershed)
        self.insert_locations(data)
