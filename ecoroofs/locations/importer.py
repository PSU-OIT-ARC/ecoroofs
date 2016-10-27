import csv
import re
import time
from decimal import Decimal

from sys import stderr

from arcutils.colorize import printer

from ..neighborhoods.models import Neighborhood
from .models import *  # noqa


# Map of CSV field names => model field names.
FIELD_NAME_MAP = {
    'Project': 'name',
    'Address': '',
    'Address (Obscured)': '',
    'Address_Clean': '',
    'Watershed': '',
    'Building Use': '',
    'Solar over Ecoroof': 'solar_over_ecoroof',
    'Type': '',
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

    def print(self, *args, **kwargs):
        if not self.quiet:
            if self.dry_run:
                args = ('[DRY RUN]',) + args
            printer.print(*args, **kwargs)

    def warn(self, *args, **kwargs):
        args = ('WARNING:',) + args
        kwargs['color'] = 'warning'
        self.print(*args, **kwargs)

    def run(self):
        if Neighborhood.objects.count() == 0:
            self.warn('WARNING: Neighborhoods have not been imported.', file=stderr)
        if self.overwrite:
            self.do_overwrite()
        elif Location.objects.count():
            self.warn('Importing locations without removing existing records.', file=stderr)
            self.warn('This will likely FAIL due to duplicate key violations.', file=stderr)
            time.sleep(5)
        data = self.read_data()
        self.column_to_table(data, BuildingUse)
        self.column_to_table(data, Contractor)
        self.column_to_table(data, Watershed)
        self.insert_locations(data)

    def do_overwrite(self):
        models_to_delete = (
            Location,
            BuildingUse,
            Contractor,
            Watershed,
        )
        for model in models_to_delete:
            self.print('Removing existing {model._meta.verbose_name_plural}...'.format(**locals()))
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
        building_uses = {r.name: r for r in BuildingUse.objects.all()}
        contractors = {r.name: r for r in Contractor.objects.all()}
        watersheds = {r.name: r for r in Watershed.objects.all()}

        # Used to keep track of names already used so we can ensure each
        # location has a unique name and slug.
        names = set()

        for row in data:
            name = row['name']

            if name is None:
                self.warn('Project name not set for location: {row}; skipping'.format_map(locals()))
                continue

            name = self.normalize_name(name)

            i = 1
            base_name = name
            while name in names:
                name = '{base_name} {i}'.format_map(locals())
                i += 1

            names.add(name)

            irrigated = self.as_bool(row['irrigated'], null=True)
            solar_over_ecoroof = self.as_bool(row['solar_over_ecoroof'], null=True)

            number_of_roofs = row['number_of_roofs']
            if number_of_roofs is None:
                self.warn(
                    'Number of roofs not set for location "{name}" Using default value'
                    .format_map(locals()))
                field = Location._meta.get_field('number_of_roofs')
                number_of_roofs = field.get_default()
            else:
                number_of_roofs = int(number_of_roofs)

            square_footage = row['square_footage']
            if square_footage is None:
                self.warn('Square footage not set for location "{name}"'.format_map(locals()))
            else:
                square_footage, *rest = square_footage.split(None, 1)
                if rest:
                    self.warn(
                        'Extraneous data in square footage for location "{name}": {rest[0]}'
                        .format_map(locals()))
                square_footage = int(square_footage)

            year_built = row['year_built']
            if year_built is None:
                self.warn(
                    'Year Built not set for location "{name}"'
                    .format_map(locals()))
            else:
                year_built = int(year_built)

            depth_min = row['depth_min']
            if depth_min is None:
                self.warn(
                    'Depth Min is not set for location "{name}"'
                    .format_map(locals()))
            else:
                depth_min = Decimal(depth_min)

            depth_max = row['depth_max']
            if depth_max is None:
                self.warn(
                    'Depth Max is not set for location "{name}"'
                    .format_map(locals()))
            else:
                depth_max = Decimal(depth_max)

            building_use = self.choice(row, 'building_use', building_uses)
            contractor = self.choice(row, 'contractor', contractors, null=True)
            watershed = self.choice(row, 'watershed', watersheds, null=True)

            # Actual coordinates
            coordinates = {'x': row['longitude'], 'y': row['latitude']}
            point = 'POINT({x} {y})'.format_map(coordinates)
            if coordinates['x'] is None or coordinates['y'] is None:
                self.warn(
                    'Coordinates not set for location "{name}": {point}; skipping'
                    .format_map(locals()))
                continue

            # Obscured coordinates
            coordinates = {'x': row['longitude_obscured'], 'y': row['latitude_obscured']}
            point_obscured = 'POINT({x} {y})'.format_map(coordinates)
            if coordinates['x'] is None or coordinates['y'] is None:
                self.warn(
                    'Obscured coordinates not set for location "{name}": {point_obscured}; skipping'
                    .format_map(locals()))
                continue

            location = Location(
                name=name,
                point=point,
                point_obscured=point_obscured,
                irrigated=irrigated,
                number_of_roofs=number_of_roofs,
                solar_over_ecoroof=solar_over_ecoroof,
                square_footage=square_footage,
                year_built=year_built,
                depth_min=depth_min,
                depth_max=depth_max,
                building_use=building_use,
                contractor=contractor,
                watershed=watershed,
            )
            location.set_neighborhood_automatically()
            locations.append(location)

        num_locations = len(locations)
        self.print('Creating', num_locations, 'locations...', end='')
        if self.real_run:
            Location.objects.bulk_create(locations)
        self.print('Done')

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

        self.print('Extracting', model_name, 'values...')
        values = {row[from_field_name] for row in data}
        values = {value for value in values if value is not None}
        values = {self.normalize_name(value) for value in values}
        num_values = len(values)
        self.print('Found', num_values, 'distinct, non-empty', model_name, 'values:')
        for value in sorted(values):
            self.print('    "{}"'.format(value))
        self.print('Done extracting', model_name, 'values')

        records = [model(**{to_field_name: value}) for value in values if value]
        num_records = len(records)
        self.print('Inserting', num_records, model_name, 'records...', end='')
        if self.real_run:
            model.objects.bulk_create(records)
        self.print('Done')
