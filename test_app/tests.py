from rest_framework.test import APITestCase
import json

from test_app.models import Note, Content, Tag


class BaseTestCase(APITestCase):
    prefix = '/api'

    def setUp(self):
        pass

    @classmethod
    def setUpTestData(cls):
        pass


class CreateUpdateTestCase(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tag_1 = Tag.objects.create(
            id=2,
            name='name_1',
        )

        cls.tag_2 = Tag.objects.create(
            id=3,
            name='name_2',
        )

        cls.note_4 = Note.objects.create(
            id=4,
            title='title_4',
            content=Content.objects.create(
                id=4,
                text='text_4',
            ),
        )

    # def test_delete_note(self):
    #     response = self.client.delete(f'{self.prefix}/notes/4')
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(Note.objects.count(), 0)
    #     self.assertEquals(Content.objects.count(), 0)
    #     data = json.loads(response.content)
    #     self.assertEquals(data, {
    #         "id": 4
    #     })


    def test_delete_note(self):
        response = self.client.delete(f'{self.prefix}/notes?id=4')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Note.objects.count(), 0)
        self.assertEquals(Content.objects.count(), 0)
        data = json.loads(response.content)
        self.assertEquals(data, {
            "id": 4
        })

    def test_post_note(self):
        response = self.client.post(
            f'{self.prefix}/notes',
            data=json.dumps({
                "title": "title_1",
                "content": "text_1",
                "tags_ids": [
                    2,
                    3
                ]
            }),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEquals(data, {
            "id": 1,
            "title": "title_1",
            "content": "text_1",
            "tags": [
                {
                    "id": 2,
                    "name": "name_1"
                },
                {
                    "id": 3,
                    "name": "name_2"
                }
            ]
        })

    def test_post_tag(self):
        response = self.client.post(
            f'{self.prefix}/tags',
            data=json.dumps({
                "name": "name_3",
            }),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEquals(data, {
            "id": 1,
            "name": "name_3"
        })


class GetTestCase(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tag_1 = Tag.objects.create(
            id = 2,
            name='name_1',
        )

        cls.content_1 = Content.objects.create(
            id=1,
            text='text_1',
        )

        cls.content_2 = Content.objects.create(
            id=2,
            text='text_2',
        )

        cls.note_1 = Note.objects.create(
            title='title_1',
            content=cls.content_1,
        )

        cls.note_1.tags.add(cls.tag_1)

        cls.note_2 = Note.objects.create(
            title='title_2',
            content=cls.content_2,
        )

    def test_get_notes(self):
        response = self.client.get(f'{self.prefix}/notes')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data, [
            {
                "id": 2,
                "title": "title_1",
                "content": "text_1",
                "tags": [
                    {
                        "id": 2,
                        "name": "name_1"
                    }
                ]
            },
            {
                "id": 3,
                "title": "title_2",
                "content": "text_2",
                "tags": [],
            }
        ])

    # def test_get_notes_id(self):
    #     response = self.client.get(f'{self.prefix}/notes/2')
    #     self.assertEquals(response.status_code, 200)
    #     data = json.loads(response.content)
    #     self.assertEquals(data, {
    #         "id": 2,
    #         "title": "title_1",
    #         "content": "text_1",
    #         "tags": [
    #             {
    #                 "id": 2,
    #                 "name": "name_1"
    #             }
    #         ]
    #     })

    def test_get_notes_id(self):
        response = self.client.get(f'{self.prefix}/notes?id=2')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data, {
            "id": 2,
            "title": "title_1",
            "content": "text_1",
            "tags": [
                {
                    "id": 2,
                    "name": "name_1"
                }
            ]
        })

    # def test_get_notes_id_not_found(self):
    #     response = self.client.get(f'{self.prefix}/notes/4')
    #     self.assertEquals(response.status_code, 404)
    #     data = json.loads(response.content)
    #     self.assertEquals(data, {
    #         "detail": "Not found."
    #     })

    def test_get_notes_id_not_found(self):
        response = self.client.get(f'{self.prefix}/notes?id=40')
        self.assertEquals(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEquals(data, {
            "detail": "Not found."
        })

    def test_get_notes_search(self):
        response = self.client.get(f'{self.prefix}/notes?query=text_2')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data, [
            {
                "id": 3,
                "title": "title_2",
                "content": "text_2",
                "tags": [
                ]
            },
        ])

    def test_get_tags(self):
        response = self.client.get(f'{self.prefix}/tags')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data, [
            {
                "id": 2,
                "name": "name_1"
            }
        ])

