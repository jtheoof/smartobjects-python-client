from mnubo.ingestion import Result
from six import string_types

class ObjectsService(object):

    def __init__(self, api_manager):
        """ Initializes ObjectServices with the api manager
        """

        self.api_manager = api_manager

    def validate_object(self, object, validate_object_type=True):
        if not object:
            raise ValueError('Object body cannot be null.')

        if 'x_device_id' not in object or not object['x_device_id']:
            raise ValueError('x_device_id cannot be null or empty.')

        if validate_object_type and ('x_object_type' not in object or not object['x_object_type']):
            raise ValueError('x_object_type cannot be null or empty.')

    def create(self, object):
        """ Creates a new object for mnubo

        :param object: the object to be created
        """
        self.validate_object(object)
        self.api_manager.post('objects', object)

    def update(self, device_id, object):
        """ Updates an object from mnubo
        :param device_id:
        :param object: the object with the updated properties
            if x_device_id is present in the object and differs from the argument device_id, it will be ignored
        """
        if not device_id:
            raise ValueError("deviceId cannot be null or empty.")
        if not object:
            raise ValueError("Object body cannot be null or empty.")
        return self.api_manager.put('objects/{}'.format(device_id), object)

    def create_update(self, objects):
        """ create or update a batch of objects

        a single batch can contain up to 1000 objects.

        :param objects: list or objects to be sent to mnubo. If the object already exists, it will be
            updated with the new content, otherwise it will be created
        :return:
        """
        [self.validate_object(obj, validate_object_type=False) for obj in objects]
        r = self.api_manager.put('objects', objects)
        return [Result(**result) for result in r.json()]

    def delete(self, device_id):
        """ Deletes an object from mnubo

        :param device_id: the device_id of the object to be deleted
        """
        if not device_id:
            raise ValueError('x_device_id cannot be null or empty.')
        self.api_manager.delete('objects/{}'.format(device_id))

    def exists(self, device_id):
        """
        :param device_id (str|list): the device_id or the list of device_ids we want to check if existing
        :return:
        """

        if isinstance(device_id, string_types):
            r = self.api_manager.get('objects/exists/{0}'.format(device_id))
        elif all(isinstance(dev_id, string_types) for dev_id in device_id):
            r = self.api_manager.post('objects/exists', device_id)
        else:
            raise TypeError

        return r.json()

    def object_exists(self, device_id):
        if not device_id:
            raise ValueError('deviceId cannot be null or empty.')
        r = self.api_manager.get('objects/exists/{0}'.format(device_id))
        json = r.json()
        assert device_id in json
        return json[device_id]

    def objects_exist(self, device_ids):
        if not device_ids:
            raise ValueError('List of deviceId cannot be null or empty.')
        r = self.api_manager.post('objects/exists', device_ids)

        result = {}
        for object in r.json():
            result.update(object)
        return result
