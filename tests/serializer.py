import unittest
import slumber
import slumber.serialize

ordered_dict_defined = True
try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        ordered_dict_defined = False


class ResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
            "foo": "bar",
        }
        if ordered_dict_defined:
            self.data1 = OrderedDict((
                ("foo", "bar"),
                ("foo2", "bar"),
                ("foo1", "bar"),
            ))

    def prepare_json_serializer(self):
        s = slumber.serialize.Serializer()

        serializer = None
        for content_type in [
            "application/json",
            "application/x-javascript",
            "text/javascript",
            "text/x-javascript",
            "text/x-json",
        ]:
            serializer = s.get_serializer(content_type=content_type)
            self.assertEqual(type(serializer), slumber.serialize.JsonSerializer,
                             "content_type %s should produce a JsonSerializer")
        return serializer

    def test_json_get_serializer(self):
        serializer = self.prepare_json_serializer()

        result = serializer.dumps(self.data)
        self.assertEqual(result, '{"foo": "bar"}')
        self.assertEqual(self.data, serializer.loads(result))

    def test_json_get_serializer_ordereddict(self):
        if not ordered_dict_defined:  # skip this test if OrderedDict is not loaded
            return

        serializer = self.prepare_json_serializer()

        result = serializer.dumps(self.data1)
        self.assertEqual(result, '{"foo": "bar", "foo2": "bar", "foo1": "bar"}')
        self.assertEqual(self.data1, serializer.loads(result))

    def test_yaml_get_serializer(self):
        s = slumber.serialize.Serializer()

        serializer = None
        for content_type in [
            "text/yaml",
        ]:
            serializer = s.get_serializer(content_type=content_type)
            self.assertEqual(type(serializer), slumber.serialize.YamlSerializer,
                             "content_type %s should produce a YamlSerializer")

        result = serializer.dumps(self.data)
        self.assertEqual(result, "{foo: bar}\n")
        self.assertEqual(self.data, serializer.loads(result))
