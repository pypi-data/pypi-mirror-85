from moco_wrapper.util.response import JsonResponse, ListingResponse

import string
import random

from .. import IntegrationTest

class TestUnit(IntegrationTest):
    def get_unit(self):
        with self.recorder.use_cassette("TestUnit.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit



    def test_getlist(self):
        with self.recorder.use_cassette("TestUnit.test_getlist"):
            unit_getlist = self.moco.Unit.getlist()

            assert unit_getlist.response.status_code == 200

            assert isinstance(unit_getlist, ListingResponse)

            assert unit_getlist.current_page == 1
            assert unit_getlist.is_last is not None
            assert unit_getlist.next_page is not None
            assert unit_getlist.total is not None
            assert unit_getlist.page_size is not None

    def test_get(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUnit.test_get"):
            unit_get = self.moco.Unit.get(unit.id)

            assert unit_get.response.status_code == 200

            assert isinstance(unit_get, JsonResponse)

            assert unit_get.data.name is not None
            assert unit_get.data.users is not None

    def test_get_unit_with_users(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUnit.test_get_unit_with_users"):
            #create a radom user and assign them to our unit
            user_create = self.moco.User.create(
                "unit",
                "test",
                "{}@mycompany.com".format(self.id_generator()),
                self.id_generator(),
                unit.id
            )

            unit_get = self.moco.Unit.get(unit.id)

            assert user_create.response.status_code == 200
            assert unit_get.response.status_code == 200

            assert isinstance(user_create, JsonResponse)
            assert isinstance(unit_get, JsonResponse)

            assert user_create.data.id in [x.id for x in unit_get.data.users]
