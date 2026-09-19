import copy
import json
import tempfile
import unittest
from pathlib import Path

from export import SECTIONS, build, select, validate


def fixture():
    data = {key: [] for key in SECTIONS}
    data["records"] = [{"id": "rest-1", "localDay": "2026-01-01", "kind": "rest",
                        "note": '<script>alert("test")</script>',
                        "dailySegments": [{"day": "2026-01-01", "seconds": 60},
                                          {"day": "2026-01-02", "seconds": 120}]}]
    data["health"] = [{"day": "2026-01-02", "value": 0}]
    data["books"] = [{"title": "Synthetic book", "lastOpenedAt": None}]
    return {"schemaVersion": "1.0", "generatedAt": "2026-01-02T12:00:00Z", "readOnly": True,
            "completeForQuery": True, "truncated": False,
            "query": {"fromDay": None, "toDay": None, "deviceId": None,
                      "timeZone": "Asia/Shanghai", "sections": list(SECTIONS)},
            "data": data, "returnedCounts": {key: len(rows) for key, rows in data.items()},
            "coverage": {}, "semantics": {}, "limitations": ["Missing data is unknown, not zero."],
            "summaries": {"manualDaily": [{"day": "2026-01-01", "restSeconds": 60},
                                            {"day": "2026-01-02", "restSeconds": 120}],
                          "appUsageDailyByDevice": []}, "links": {}, "mirror": {}}


class ExportTests(unittest.TestCase):
    def test_cross_midnight_selection_keeps_full_record_and_daily_total(self):
        source = fixture()
        day = select(source, day="2026-01-02")
        self.assertEqual(day["data"]["records"], source["data"]["records"])
        self.assertEqual(day["summaries"]["manualDaily"], [{"day": "2026-01-02", "restSeconds": 120}])
        self.assertEqual(day["data"]["books"], source["data"]["books"])
        self.assertIsNone(source["query"]["fromDay"])

    def test_static_export_escapes_content_and_preserves_complete_data(self):
        source = fixture()
        with tempfile.TemporaryDirectory() as directory:
            build(source, {"properties": {"summaries": {}}}, directory)
            root = Path(directory)
            output = json.loads((root / "data.json").read_text())
            self.assertEqual(output["data"], source["data"])
            self.assertFalse(output["mirror"]["queryParametersSupported"])
            page = (root / "records.html").read_text()
            self.assertNotIn("<script>", page)
            self.assertIn("&lt;script&gt;", page)
            self.assertTrue((root / "days/2026-01-01.html").exists())
            self.assertTrue((root / "days/2026-01-02.json").exists())
            self.assertFalse((root / "days/2026-01-03.json").exists())
            self.assertIn("NOT supported", (root / "llms.txt").read_text())

    def test_bad_or_partial_source_is_rejected(self):
        for key, value in [("truncated", True), ("completeForQuery", False), ("schemaVersion", "2.0")]:
            bad = fixture()
            bad[key] = value
            with self.assertRaises(ValueError):
                validate(bad)
        bad = fixture()
        bad["returnedCounts"]["health"] = 9
        with self.assertRaises(ValueError):
            validate(bad)

    def test_category_does_not_include_other_data_or_summaries(self):
        result = select(fixture(), section="health")
        self.assertEqual(list(result["data"]), ["health"])
        self.assertEqual(result["summaries"], {})


if __name__ == "__main__":
    unittest.main()
