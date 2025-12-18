#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=
"""
File       : processor.py
Author     : Valentin Kuznetsov <vkuznet AT gmail dot com>
Description: Processor module

Define a generic `Processor` object.
"""

# System modules
import argparse
import logging
from sys import modules
from time import time

class PipelineItem():
    """An object that can be supplied as one of the items
    in `Pipeline.items`.
    """
    def __init__(self):
        """Constructor of PipelineItem class."""
        self.__name__ = self.__class__.__name__
        self.logger = logging.getLogger(self.__name__)
        self.logger.propagate = False

    @staticmethod
    def get_default_nxentry(nxobject):
        """Given a `nexusformat.nexus.NXroot` or 
        `nexusformat.nexus.NXentry` object, return the default or
        first `nexusformat.nexus.NXentry` match.

        :param nxobject: Input data.
        :type nxobject: nexusformat.nexus.NXroot,
            nexusformat.nexus.NXentry
        :raises ValueError: If unable to retrieve a
            `nexusformat.nexus.NXentry` object.
        :return: The input data if a `nexusformat.nexus.NXentry`
            object or the default or first `nexusformat.nexus.NXentry`
            object if a `nexusformat.nexus.NXroot` object.
        :rtype: nexusformat.nexus.NXentry
        """
        # Third party modules
        from nexusformat.nexus import (
            NXentry,
            NXroot,
        )

        if isinstance(nxobject, NXroot):
            if 'default' in nxobject.attrs:
                nxentry = nxobject[nxobject.default]
            else:
                nxentries = [
                    v for v in nxobject.values() if isinstance(v, NXentry)]
                if not nxentries:
                    raise ValueError(f'Unable to retrieve a NXentry object')
                elif len(nxentries) != 1:
                    self.logger.warning(
                        f'Found multiple NXentries, returning the first')
                nxentry = nxentries[0]
        elif isinstance(nxobject, NXentry):
            nxentry = nxobject
        else:
            raise ValueError(f'Invalid parameter nxobject ({nxobject})')
        return nxentry

    @staticmethod
    def unwrap_pipelinedata(data):
        """Given a list of PipelineData objects, return a list of
        their `data` values.

        :param data: Input data to read, write, or process that needs
            to be unwrapped from PipelineData before use.
        :type data: list[PipelineData]
        :return: The `'data'` values of the items in the input data.
        :rtype: list[object]
        """
        unwrapped_data = []
        if isinstance(data, list):
            for d in data:
                if isinstance(d, PipelineData):
                    unwrapped_data.append(d['data'])
                else:
                    unwrapped_data.append(d)
        else:
            unwrapped_data = [data]
        return unwrapped_data

    def get_config(
            self, data=None, config=None, schema='', remove=True, **kwargs):
        """Look through `data` for an item whose value for the first
        `'schema'` key matches `schema`. Convert the value for that
        item's `'data'` key into the configuration's Pydantic model
        identified by `schema` and return it. If no item is found and
        config is specified, validate it against the configuration's
        Pydantic model identified by `schema` and return it.

        :param data: Input data from a previous `PipelineItem`.
        :type data: list[PipelineData], optional
        :param schema: Name of the `BaseModel` class to match in
            `data` & return.
        :type schema: str
        :param config: Initialization parameters for an instance of
            the Pydantic model identified by `schema`, required if
            data is unspecified, invalid or does not contain an item
            that matches the schema.
        :type config: dict, optional
        :param remove: If there is a matching entry in `data`, remove
           it from the list, defaults to `True`.
        :type remove: bool, optional
        :raises ValueError: If there's no match for `schema` in `data`.
        :return: The first matching configuration model.
        :rtype: BaseModel
        """
        self.logger.debug(f'Getting {schema} configuration')
        t0 = time()

        matching_config = False
        if data is not None:
            try:
                for i, d in enumerate(data):
                    if d.get('schema') == schema:
                        matching_config = d.get('data')
                        if remove:
                            data.pop(i)
                        break
            except:
                pass

        if not matching_config:
            if isinstance(config, dict):
                matching_config = config
            else:
                raise ValueError(
                    f'Unable to find a configuration for schema `{schema}`')

        mod_name, cls_name = schema.rsplit('.', 1)
        module = __import__(f'{mod_name}', fromlist=cls_name)
        matching_config.update(kwargs)
        model_config = getattr(module, cls_name)(**matching_config)

        self.logger.debug(
            f'Got {schema} configuration in {time()-t0:.3f} seconds')

        return model_config

    def get_data(self, data, name=None, schema=None, remove=True):
        """Look through `data` for an item whose `'data'` value is
        a nexusformat.nexus.NXobject object or matches a given name or
        schema. Pick the item for which
        the `'name'` key matches `name` if set or the `'schema'` key
        matches `schema` if set, pick the last match for a 
        nexusformat.nexus.NXobject object otherwise.
        Return the data object.

        :param data: Input data from a previous `PipelineItem`.
        :type data: list[PipelineData].
        :param name: Name of the data item to match in `data` & return.
        :type name: str
        :param schema: Name of the `BaseModel` class to match in
            `data` & return.
        :type schema: str
        :param remove: If there is a matching entry in `data`, remove
            it from the list, defaults to `True`.
        :type remove: bool, optional
        :raises ValueError: If there's no match for `name` or 'schema`
            in `data`, or if there is no object of type
            nexusformat.nexus.NXobject.
        :return: The last matching data item.
        :rtype: obj
        """
        # Third party modules
        from nexusformat.nexus import NXobject

        result = None
        t0 = time()
        if name is None and schema is None:
            for i, d in reversed(list(enumerate(data))):
                if isinstance(d.get('data'), NXobject):
                    result = d.get('data')
                    if remove:
                        data.pop(i)
                    break
            else:
                raise ValueError(f'No NXobject data item found')
        elif name is not None:
            self.logger.debug(f'Getting data item named "{name}"')
            for i, d in reversed(list(enumerate(data))):
                if d.get('name') == name:
                    result = d.get('data')
                    if remove:
                        data.pop(i)
                    break
            else:
                raise ValueError(f'No match for data item named "{name}"')
        elif schema is not None:
            self.logger.debug(f'Getting data item with schema "{schema}"')
            for i, d in reversed(list(enumerate(data))):
                if d.get('schema') == schema:
                    result = d.get('data')
                    if remove:
                        data.pop(i)
                    break
            else:
                raise ValueError(
                    f'No match for data item with schema "{schema}"')
        self.logger.debug(
           f'Obtained pipeline data in {time()-t0:.3f} seconds')

        return result

    def execute(self, data, schema=None, **kwargs):
        """Run the appropriate method of the object and return the
        result.

        :param schema: The name of a schema associated with the data
            that will be returned.
        :type schema: str
        :param kwargs: A dictionary of any positional and keyword
            arguments to supply to the read, process, or write method.
        :type kwargs: dict
        :return: The wrapped result of running read, process, or write.
        :rtype: list[PipelineData]
        """
        if hasattr(self, 'read'):
            method_name = 'read'
            inputdir = kwargs.get('inputdir')
            if 'filename' in kwargs:
                filename = kwargs['filename']
                newfilename = os.path.normpath(os.path.realpath(
                    os.path.join(inputdir, filename)))
                if (not os.path.isfile(newfilename)
                        and not os.path.dirname(filename)):
                    outputdir = kwargs.get('outputdir')
                    self.logger.warning(
                        f'Unable to find {filename} in {inputdir}, '
                        f' looking in {outputdir}')
                    newfilename = os.path.normpath(os.path.realpath(
                        os.path.join(outputdir, filename)))
                kwargs['filename'] = newfilename
        elif hasattr(self, 'process'):
            method_name = 'process'
        elif hasattr(self, 'write'):
            method_name = 'write'
            outputdir = kwargs.get('outputdir')
            if outputdir is not None and 'filename' in kwargs:
                kwargs['filename'] = os.path.normpath(os.path.realpath(
                    os.path.join(outputdir, kwargs['filename'])))
        else:
            self.logger.error('No implementation of read, process, or write')
            return None

        method = getattr(self, method_name)
        allowed_args = inspect.getfullargspec(method).args \
                       + inspect.getfullargspec(method).kwonlyargs
        args = {}
        for k, v in kwargs.items():
            if k in allowed_args:
                args[k] = v
        if 'data' in allowed_args:
            args['data'] = data

        t0 = time()
        self.logger.debug(
            f'Executing "{method_name}" with schema "{schema}" and {args}')
        self.logger.info(f'Executing "{method_name}"')
        ddata = method(**args)
        self.logger.info(
            f'Finished "{method_name}" in {time()-t0:.0f} seconds\n')

        name = kwargs.get('name', self.__name__)
        if method_name == 'read':
            data.append(PipelineData(name=name, data=ddata, schema=schema))
            return data
        elif method_name == 'process':
            if isinstance(ddata, tuple):
                data.extend([d if isinstance(d, PipelineData)
                         else PipelineData(name=name, data=d, schema=schema)
                         for d in ddata])
            else:
                data.append(PipelineData(name=name, data=ddata, schema=schema))
        return data


class Processor(PipelineItem):
    """Generic data processor.

    The job of any `Processor` in a `Pipeline` is to receive data
    returned by the previous `PipelineItem`, process it in some way,
    and return the result for the next `PipelineItem` to use as input.
    """
    def process(self, data):
        """Extract the contents of the input data, add a string to it,
        and return the amended value.

        :param data: Input data.
        :return: Processed data.
        """
        # If needed, extract data from a returned value of Reader.read
        if isinstance(data, list):
            if all(isinstance(d, dict) for d in data):
                data = data[0]['data']
        if data is None:
            return []
        # The process operation is a simple string concatenation
        data += 'process part\n'
        # Return data back to pipeline
        return data


class OptionParser():
    """User based option parser."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument(
            '--data', action='store',
            dest='data', default='', help='Input data')
        self.parser.add_argument(
            '--processor', action='store',
            dest='processor', default='Processor', help='Processor class name')
        self.parser.add_argument(
            '--log-level', choices=logging._nameToLevel.keys(),
            dest='log_level', default='INFO', help='logging level')


def main(opt_parser=OptionParser):
    """Main function."""
    optmgr = opt_parser()
    opts = optmgr.parser.parse_args()
    cls_name = opts.processor
    try:
        processor_cls = getattr(modules[__name__], cls_name)
    except AttributeError:
        print(f'Unsupported processor {cls_name}')
        raise

    processor = processor_cls()
    processor.logger.setLevel(getattr(logging, opts.log_level))
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter(
        '{name:20}: {message}', style='{'))
    processor.logger.addHandler(log_handler)
    data = processor.process(opts.data)


if __name__ == '__main__':
    main()
