import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def create_ruian_types():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'ruian_types'}
        logging.info("getting vocabulary show")
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'ruian_types'}
        logging.info("trying to create vocab");
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (
                u'AD', u'BPA', u'CO', u'KR', u'KU', u'MC', u'MP', u'OB', u'OK',
                u'OP', u'PA', u'PO', u'PU', u'RS', u'SO', u'SP', u'ST', u'UL',
                u'VC', u'VO', u'ZJ'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)


def ruian_types():
    logging.info("ruiantypes")
    create_ruian_types()
    try:
        tag_list = toolkit.get_action('tag_list')
        ruian_types = tag_list(data_dict={'vocabulary_id': 'ruian_types'})
        return ruian_types
    except toolkit.ObjectNotFound:
        return None


class CkanExtCzNkod(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config_):
        print("CkanExtCzNkod.update_config")
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config_, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config_, 'public')

    def _modify_package_schema(self, schema):
        schema.update({
            'publisher_name': [toolkit.get_validator('ignore_missing'),
                               toolkit.get_converter('convert_to_extras')],
            'publisher_uri': [toolkit.get_validator('ignore_missing'),
                              toolkit.get_converter('convert_to_extras')],
            'frequency': [toolkit.get_validator('ignore_missing'),
                          toolkit.get_converter('convert_to_extras')],
            'ruian_code': [toolkit.get_validator('ignore_missing'),
                           toolkit.get_converter('convert_to_extras')],
            'ruian_type': [toolkit.get_validator('ignore_missing'),
                           toolkit.get_converter('convert_to_extras')],
            'spatial_uri': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'theme': [toolkit.get_validator('ignore_missing'),
                      toolkit.get_converter('convert_to_extras')],
            'temporal_start': [toolkit.get_validator('ignore_missing'),
                               toolkit.get_converter('convert_to_extras')],
            'temporal_end': [toolkit.get_validator('ignore_missing'),
                             toolkit.get_converter('convert_to_extras')],
            'real_issued': [toolkit.get_validator('ignore_missing'),
                               toolkit.get_converter('convert_to_extras')],
            'real_modified': [toolkit.get_validator('ignore_missing'),
                               toolkit.get_converter('convert_to_extras')],
            'nkod_link': [toolkit.get_validator('ignore_missing'),
                       toolkit.get_converter('convert_to_extras')],
            'schema': [toolkit.get_validator('ignore_missing'),
                       toolkit.get_converter('convert_to_extras')],
            'license_link': [toolkit.get_validator('ignore_missing'),
                             toolkit.get_converter('convert_to_extras')]
        })

        schema['resources'].update({
            'license_link': [toolkit.get_validator('ignore_missing')],
            'describedBy': [toolkit.get_validator('ignore_missing')],
            'describedByType': [toolkit.get_validator('ignore_missing')],
            'temporal_start': [toolkit.get_validator('ignore_missing')],
            'temporal_end': [toolkit.get_validator('ignore_missing')],
            'spatial_uri': [toolkit.get_validator('ignore_missing')],
            'ruian_type': [toolkit.get_validator('ignore_missing')],
            'ruian_code': [toolkit.get_validator('ignore_missing')]
        })

        return schema

    def create_package_schema(self):
        print("CkanExtCzNkod.create_package_schema")
        # let's grab the default schema in our plugin
        schema = super(CkanExtCzNkod, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        print("CkanExtCzNkod.update_package_schema")
        schema = super(CkanExtCzNkod, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        print("CkanExtCzNkod.show_package_schema")
        schema = super(CkanExtCzNkod, self).show_package_schema()
        schema['tags']['__extras'].append(
            toolkit.get_converter('free_tags_only'))
        schema.update({
            'publisher_name': [toolkit.get_converter('convert_from_extras'),
                               toolkit.get_validator('ignore_missing')],
            'publisher_uri': [toolkit.get_converter('convert_from_extras'),
                              toolkit.get_validator('ignore_missing')],
            'frequency': [toolkit.get_converter('convert_from_extras'),
                          toolkit.get_validator('ignore_missing')],
            'ruian_code': [toolkit.get_converter('convert_from_extras'),
                           toolkit.get_validator('ignore_missing')],
            'ruian_type': [toolkit.get_converter('convert_from_extras'),
                           toolkit.get_validator('ignore_missing')],
            'spatial_uri': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'theme': [toolkit.get_converter('convert_from_extras'),
                      toolkit.get_validator('ignore_missing')],
            'temporal_start': [toolkit.get_converter('convert_from_extras'),
                               toolkit.get_validator('ignore_missing')],
            'license_link': [toolkit.get_converter('convert_from_extras'),
                             toolkit.get_validator('ignore_missing')],
            'schema': [toolkit.get_converter('convert_from_extras'),
                       toolkit.get_validator('ignore_missing')],
            'real_issued': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'real_modified': [toolkit.get_converter('convert_from_extras'),
                              toolkit.get_validator('ignore_missing')],
            'nkod_link': [toolkit.get_converter('convert_from_extras'),
                          toolkit.get_validator('ignore_missing')],
            'temporal_end': [toolkit.get_converter('convert_from_extras'),
                             toolkit.get_validator('ignore_missing')]
        })

        schema['resources'].update({
            'license_link': [toolkit.get_validator('ignore_missing')],
            'describedBy': [toolkit.get_validator('ignore_missing')],
            'describedByType': [toolkit.get_validator('ignore_missing')],
            'spatial_uri': [toolkit.get_validator('ignore_missing')],
            'ruian_type': [toolkit.get_validator('ignore_missing')],
            'ruian_code': [toolkit.get_validator('ignore_missing')],
            'temporal_start': [toolkit.get_validator('ignore_missing')],
            'temporal_end': [toolkit.get_validator('ignore_missing')]
        })

        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def get_helpers(self):
        return {'ruian_types': ruian_types}
