# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

from justice import Justice
from . import JusticeTestCase


class JusticeStatisticTestCase(JusticeTestCase):

    @classmethod
    def setUpClass(cls):
        super(JusticeStatisticTestCase, cls).setUpClass()
        cls.user_id = "e3a07e0906794541954480740c1fb184"
        cls.second_user_id = "ddf8601399334f308fe43f7ea914bdf6"
        cls.bulk_user = [cls.user_id, cls.second_user_id]

        # StatCode for stat config test
        # CREATE
        cls.to_create_stat_code = "augmentsdktestcreate"
        # UPDATE
        cls.to_update_stat_code = "augmentsdktestupdate"
        update_config = cls.create_sample_config(cls, cls.to_update_stat_code)
        cls.justice.statistic.create_stat_config(update_config)
        # DELETE
        cls.to_delete_stat_code = "augmentsdktestdelete"
        delete_config = cls.create_sample_config(cls, cls.to_delete_stat_code)
        cls.justice.statistic.create_stat_config(delete_config)

        # StatCode for user statitem test
        # NOTE: StatCode below cannot be deleted from config, as it status
        #       changed to TIED after it interacted with user
        # CREATE
        cls.user_create_stat_code = "useraugmentsdktest1"
        # UPDATE
        cls.user_update_stat_code = "useraugmentsdktest2"
        cls.justice.statistic.create_user_statitem(
            cls.user_id, cls.user_update_stat_code)
        # DELETE
        cls.user_delete_stat_code = "useraugmentsdktest3"
        cls.justice.statistic.create_user_statitem(
            cls.user_id, cls.user_delete_stat_code)

        # StatCode bulk ops
        cls.create_bulk_code = ["useraugmentsdktest4", "useraugmentsdktest5"]
        cls.update_bulk_code = ["useraugmentsdktest6", "useraugmentsdktest7"]
        for code in cls.update_bulk_code:
            cls.justice.statistic.create_user_statitem(cls.user_id, code)
            cls.justice.statistic.create_user_statitem(
                cls.second_user_id, code)

    @classmethod
    def tearDownClass(cls):
        # cleanup stat config test
        cls.justice.statistic.delete_stat_config(cls.to_create_stat_code)
        cls.justice.statistic.delete_stat_config(cls.to_update_stat_code)

        # cleanup user statitem test
        cls.justice.statistic.delete_user_statitem(
            cls.user_id, cls.user_create_stat_code)
        cls.justice.statistic.delete_user_statitem(
            cls.user_id, cls.user_update_stat_code)

        # cleanup bulk ops
        for code in cls.create_bulk_code:
            cls.justice.statistic.delete_user_statitem(cls.user_id, code)
        for code in cls.update_bulk_code:
            cls.justice.statistic.delete_user_statitem(cls.user_id, code)
            cls.justice.statistic.delete_user_statitem(
                cls.second_user_id, code)

        super(JusticeStatisticTestCase, cls).tearDownClass()

    def create_sample_config(self, stat_code):
        return {
            "defaultValue": 0,
            "description": "string",
            "incrementOnly": True,
            "maximum": 100,
            "minimum": 0,
            "name": "augment-sdk-sample-test",
            "setAsGlobal": True,
            "setBy": "SERVER",
            "statCode": stat_code,
            "tags": [
                "SDKSampleTag"
            ]
        }

    def test_get_global_stats(self):
        resp = self.justice.statistic.get_global_stats()
        result = resp.json()['data']

        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(result), 0)

    def test_search_statcode(self):
        resp = self.justice.statistic.search_statcode('elo')
        result = resp.json()['data']

        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(result), 0)

    def test_get_stat_config(self):
        resp = self.justice.statistic.get_stat_config('elo')
        result = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(result['name'], "ELO")
        self.assertEqual(result['defaultValue'], 0)

    def test_create_stat_config(self):
        sample = self.create_sample_config(self.to_create_stat_code)
        resp = self.justice.statistic.create_stat_config(sample)

        self.assertEqual(resp.status_code, 201)

    # TODO: add test for each updated fields?
    def test_update_stat_config(self):
        # null update, nothing changed
        resp = self.justice.statistic.update_stat_config(
            self.to_update_stat_code)

        self.assertEqual(resp.status_code, 200)

    def test_delete_stat_config(self):
        resp = self.justice.statistic.delete_stat_config(
            self.to_delete_stat_code)

        self.assertEqual(resp.status_code, 204)

    def test_get_user_stats(self):
        resp = self.justice.statistic.get_user_stats(self.user_id)
        result = resp.json()['data']

        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(result), 0)

    def test_create_user_statitem(self):
        resp = self.justice.statistic.create_user_statitem(
            self.user_id, self.user_create_stat_code)

        self.assertEqual(resp.status_code, 201)

    def test_update_user_statitem(self):
        value = 7
        resp = self.justice.statistic.update_user_statitem_value(
            self.user_id, self.user_update_stat_code, value)
        result = resp.json()['currentValue']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(result, value)

    def test_delete_user_statitem(self):
        resp = self.justice.statistic.delete_user_statitem(
            self.user_id, self.user_delete_stat_code)

        self.assertEqual(resp.status_code, 204)

    def test_put_update_multiple_bulk(self):
        bulk = []
        for code in self.update_bulk_code:
            for user in self.bulk_user:
                bulk.append({
                    "inc": 1,
                    "statCode": code,
                    "userId": user
                })
        resp = self.justice.statistic.put_update_multiple_bulk(bulk)

        self.assertEqual(resp.status_code, 200)

    def test_patch_update_multiple_bulk(self):
        bulk = []
        for code in self.update_bulk_code:
            for user in self.bulk_user:
                bulk.append({
                    "inc": 1,
                    "statCode": code,
                    "userId": user
                })
        resp = self.justice.statistic.patch_update_multiple_bulk(bulk)

        self.assertEqual(resp.status_code, 200)

    def test_create_single_bulk(self):
        resp = self.justice.statistic.create_single_bulk(
            self.user_id, self.create_bulk_code)

        self.assertEqual(resp.status_code, 200)

    def test_put_update_single_bulk(self):
        bulk = [{"inc": 1, "statCode": code} for code in self.update_bulk_code]
        resp = self.justice.statistic.put_update_single_bulk(
            self.user_id, bulk)

        self.assertEqual(resp.status_code, 200)

    def test_patch_update_single_bulk(self):
        bulk = [{"inc": 1, "statCode": code} for code in self.update_bulk_code]
        resp = self.justice.statistic.patch_update_single_bulk(
            self.user_id, bulk)

        self.assertEqual(resp.status_code, 200)
