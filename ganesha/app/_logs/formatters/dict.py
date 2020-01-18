import datetime
import logging
import traceback


def _run_enrichment_method(enrichment_method):
    try:
        return enrichment_method()
    except Exception as e:
        return {'error': str(e)}


class DictFormatter(logging.Formatter):
    def __init__(self, app_name, enrichment_methods=None, **kwargs):
        super().__init__(**kwargs)

        self.app_name = app_name
        self.enrichment_methods = enrichment_methods

    def format(self, record):
        message_json = dict()

        self.add_exception_info(record, message_json)

        message_json['time'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        message_json['args'] = dict()
        self.add_custom_message(record, message_json)
        self.add_enrichment(message_json)

        message_json['logger'] = self.app_name
        message_json['level'] = record.levelname
        message_json['log_trace'] = record.pathname
        if not any(message_json['args']):
            message_json.pop('args')

        return message_json

    def add_enrichment(self, message_json):
        if not self.enrichment_methods:
            return

        for field, enrichment_method in self.enrichment_methods.items():
            enrichment_value = _run_enrichment_method(enrichment_method)

            if enrichment_value is not None:
                message_json['args'][field] = enrichment_value

    @staticmethod
    def add_exception_info(record, message_json):
        if bool(record.exc_info) and any(record.exc_info):
            message_json['error_class_name'] = record.exc_info[1].__class__.__name__
            message_json['error_message'] = str(record.exc_info[1])
            message_json['backtrace'] = '\n'.join(traceback.format_exception(*record.exc_info))

    @staticmethod
    def add_custom_message(record, message_json):
        if isinstance(record.msg, dict):
            message_json['msg'] = '{} {}'.format(record.msg.get('message', ''),
                                                 record.msg.get('msg', '')).strip()

            # remove messages from args
            args = {k: record.msg[k] for k in record.msg if k not in ['message', 'msg']}
            message_json['args'].update(args)
        else:
            message_json['msg'] = str(record.msg)