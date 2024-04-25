import tempfile

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Content, Guideline, ReviewItem
from core.serializers import GuidelineSerializer, ReviewItemSerializer


class GuidelineViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

        self.client = APIClient()
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpassword'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.guideline1 = Guideline.objects.create(
            title='Guideline 1', description='Description 1'
        )
        self.guideline2 = Guideline.objects.create(
            title='Guideline 2', description='Description 2'
        )

    def test_list_guidelines(self):
        response = self.client.get(reverse('guideline-list'))
        guidelines = Guideline.objects.all()
        serializer = GuidelineSerializer(guidelines, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_guideline(self):
        response = self.client.get(
            reverse('guideline-detail', args=[self.guideline1.id])
        )
        guideline = Guideline.objects.get(id=self.guideline1.id)
        serializer = GuidelineSerializer(guideline)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_guideline(self):
        data = {'title': 'New Guideline', 'description': 'New Description'}
        response = self.client.post(reverse('guideline-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Guideline.objects.filter(title='New Guideline').exists())

    def test_update_guideline(self):
        data = {'title': 'Updated Guideline', 'description': 'Updated Description'}
        response = self.client.put(
            reverse('guideline-detail', args=[self.guideline1.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.guideline1.refresh_from_db()
        self.assertEqual(self.guideline1.title, 'Updated Guideline')
        self.assertEqual(self.guideline1.description, 'Updated Description')

    def test_partial_update_guideline(self):
        data = {'description': 'Updated Description'}
        response = self.client.patch(
            reverse('guideline-detail', args=[self.guideline1.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.guideline1.refresh_from_db()
        self.assertEqual(self.guideline1.description, 'Updated Description')

    def test_delete_guideline_not_allowed(self):
        response = self.client.delete(
            reverse('guideline-detail', args=[self.guideline1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ContentListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.content1 = Content.objects.create(
            title='Content 1', file='content1.txt', author=self.user
        )
        self.content2 = Content.objects.create(
            title='Content 2', file='content2.txt', author=self.user
        )

    def test_get_content_list(self):
        url = reverse('content-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_content_list_unauthenticated(self):
        self.client.logout()

        url = reverse('content-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ContentUploadViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.guideline1 = Guideline.objects.create(
            title='Guideline 1', description='Description 1'
        )
        self.guideline2 = Guideline.objects.create(
            title='Guideline 2', description='Description 2'
        )

    def test_upload_content_success(self):
        url = reverse('content-upload')

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"Test file content")
            temp_file.seek(0)

            data = {'title': 'Test Content', 'file': temp_file}
            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Content.objects.filter(title='Test Content').exists())

        content = Content.objects.get(title='Test Content')
        self.assertEqual(
            ReviewItem.objects.filter(content=content).count(),
            Guideline.objects.count(),
        )

    def test_upload_content_with_same_title(self):
        Content.objects.create(
            title='Test Content', file='testfile.txt', author=self.user
        )

        url = reverse('content-upload')

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"Test file content")
            temp_file.seek(0)

            data = {'title': 'Test Content', 'file': temp_file}
            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data['error'],
            'Content with the same title already exists. Please choose a unique title or update existing content.',
        )

    def test_upload_content_invalid_data(self):
        url = reverse('content-upload')

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"Test file content")
            temp_file.seek(0)

            data = {'file': temp_file}
            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_content_with_non_allowed_extension(self):
        url = reverse('content-upload')

        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_file:
            temp_file.write(b"Test file content")
            temp_file.seek(0)

            data = {'title': 'Test Content', 'file': temp_file}
            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['file'][0],
            'Invalid file type. Only images, Word documents, TXT, and PDF files are allowed.',
        )

        self.assertFalse(Content.objects.filter(title='Test Content').exists())


class ContentDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.content1 = Content.objects.create(
            title='Content 1', file='content1.txt', author=self.user
        )
        self.content2 = Content.objects.create(
            title='Content 2', file='content2.txt', author=self.user
        )

    def test_get_content_detail(self):
        url = reverse('content-detail', kwargs={'pk': self.content1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_content_detail(self):
        url = reverse('content-detail', kwargs={'pk': self.content1.pk})
        data = {'title': 'Updated Content 1'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.content1.refresh_from_db()
        self.assertEqual(self.content1.title, 'Updated Content 1')

    def test_patch_content_detail_unauthorized(self):
        other_user = User.objects.create_user(
            username='otheruser', password='testpassword'
        )
        self.client.force_authenticate(user=other_user)

        url = reverse('content-detail', kwargs={'pk': self.content1.pk})
        data = {'title': 'Attempted Unauthorized Update'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'You can only update content you own.')


class ContentReviewStatusViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.content = Content.objects.create(
            title='Test Content', file='testfile.txt', author=self.user
        )
        self.guideline1 = Guideline.objects.create(
            title='Guideline 1', description='Description 1'
        )
        self.guideline2 = Guideline.objects.create(
            title='Guideline 2', description='Description 2'
        )
        self.review_item1 = ReviewItem.objects.create(
            content=self.content,
            guideline=self.guideline1,
            status=ReviewItem.StatusChoices.PASSED,
        )
        self.review_item2 = ReviewItem.objects.create(
            content=self.content,
            guideline=self.guideline2,
            status=ReviewItem.StatusChoices.PENDING,
        )

    def test_get_review_status(self):
        url = reverse('content-review-status', kwargs={'content_id': self.content.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ReviewItemSerializer(
            [self.review_item1, self.review_item2], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_get_review_status_nonexistent_content(self):
        url = reverse('content-review-status', kwargs={'content_id': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContentReviewUpdateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.content = Content.objects.create(
            title='Test Content', file='testfile.txt', author=self.user
        )
        self.guideline1 = Guideline.objects.create(
            title='Guideline 1', description='Description 1'
        )
        self.guideline2 = Guideline.objects.create(
            title='Guideline 2', description='Description 2'
        )
        self.review_item1 = ReviewItem.objects.create(
            content=self.content,
            guideline=self.guideline1,
            status=ReviewItem.StatusChoices.PENDING,
        )
        self.review_item2 = ReviewItem.objects.create(
            content=self.content,
            guideline=self.guideline2,
            status=ReviewItem.StatusChoices.PENDING,
        )

    def test_update_review_item_success(self):
        url = reverse(
            'content-review-update',
            kwargs={
                'content_id': self.content.pk,
                'review_item_id': self.review_item1.pk,
            },
        )
        data = {'status': 'PASS'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.review_item1.refresh_from_db()
        self.assertEqual(self.review_item1.status, ReviewItem.StatusChoices.PASSED)
        self.assertEqual(self.review_item1.reviewer, self.user)
        self.assertIsNotNone(self.review_item1.reviewed_at)

    def test_update_review_item_nonexistent_content(self):
        url = reverse(
            'content-review-update',
            kwargs={'content_id': 999, 'review_item_id': self.review_item1.pk},
        )
        data = {'status': 'PASS'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'No Content matches the given query.')

    def test_update_review_item_nonexistent_review_item(self):
        url = reverse(
            'content-review-update',
            kwargs={'content_id': self.content.pk, 'review_item_id': 999},
        )
        data = {'status': 'PASS'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['error'], 'No Review item matches the given query.'
        )

    def test_update_review_item_invalid_data(self):
        url = reverse(
            'content-review-update',
            kwargs={
                'content_id': self.content.pk,
                'review_item_id': self.review_item1.pk,
            },
        )
        data = {'status': 'INVALID_STATUS'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)
