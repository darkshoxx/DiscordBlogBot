from unittest.mock import AsyncMock, patch
import aiohttp
import pytest
from DiscordBlogBot.main import (
    fetch_latest_wp_blog_post, fetch_latest_non_wp_blog_post
)

# Test parameters, see docstring of test_fetch_latest_wp_blog_post
TEST_CASES_WP = [
    (
        {'author': 'TheCoolAuthor', 'url': 'https://wordpress-site-1.com'},
        12450468503,
        'ExcitingBlogPost',
        '2022-01-01T12:00:00',
        'https://example.com/WHOA',
    ),
    (
        {'author': 'TheMellowAuthor', 'url': 'https://wordpress-site-2.com'},
        4566045674069456,
        'CalmBlogPost',
        '2022-02-02T14:30:00',
        'https://example.com/SHHHHH',
    ),
]

TEST_CASES_NON_WP = [
    (
        {
            'author': 'TheCoolOne',
            'url': 'https://non-wordpress-site-1.com',
            'update_route': '/latest-blog'
        },
        '/blog/slug/hottest-newest',
        'https://non-wordpress-site-1.com/blog/slug/hottest-newest',
    ),
    (
        {
            'author': 'TheMellowOne',
            'url': 'https://non-wordpress-site-2.com',
            'update_route': '/latest-blog'
        },
        '/blog/slug/nothing-new',
        'https://non-wordpress-site-2.com/blog/slug/nothing-new',
    ),
]

@pytest.mark.parametrize("blog_dict, post_slug, link", TEST_CASES_NON_WP)
@pytest.mark.asyncio
async def test_fetch_latest_non_wp_blog_post(blog_dict, post_slug, link):
    """
    Tests fetch_latest_non_wp_blog_post
    """
    # use context manager to mock the "get" function of the ClientSession
    with patch.object(aiohttp.ClientSession, 'get') as mock_get:
        # mock the client session response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = (
            'something_that_will_be_filtered_out_by_regex ' + post_slug
        )

        # make sure the defined return value is returned by mock_get function
        mock_get.return_value.__aenter__.return_value = mock_response

        # time to pretend to call the blog
        lastest_route, print_string = await fetch_latest_non_wp_blog_post(
            aiohttp.ClientSession(),
            blog_dict
        )

    # test assertions
    assert blog_dict['url'] + lastest_route == link
    assert print_string == "HEY, LISTEN! \nNew Blog post from " + \
        f"{blog_dict['author']}! \n Link:{blog_dict['url'] + lastest_route}"

    mock_response.raise_for_status.assert_called_once()

@pytest.mark.parametrize("blog_dict, post_id, title, date, link", TEST_CASES_WP)
@pytest.mark.asyncio
async def test_fetch_latest_wp_blog_post(blog_dict, post_id, title, date, link):
    """
    Test the fetch_latest_wp_blog_post function.

    It mocks the aiohttp.ClientSession.get method to simulate the behavior of
    fetching the latest blog post from a WordPress site.

    Parameters:
    - blog_dict: A dictionary containing blog information.
    - post_id: Expected post ID.
    - title: Expected post title.
    - date: Expected post date.
    - link: Expected post link.

    Assertions:
    - Checks if the function returns the correct post_id and post_print_string.
    - Checks if the aiohttp.ClientSession.get method is called once
        with the correct arguments.
    - Checks if the response's raise_for_status method is called once.
    """
    # Use patch.object to mock aiohttp.ClientSession.get method
    with patch.object(aiohttp.ClientSession, 'get') as mock_get:
        # Mock the response from the session.get method
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = [
            {
                'id': post_id,
                'title': {'rendered': title},
                'date': date,
                'link': link,
            }
        ]

        # Configure the mock session to return the mock response
        mock_get.return_value.__aenter__.return_value = mock_response

        # Call the async function under test
        returned_post_id, post_print_string = await fetch_latest_wp_blog_post(
            aiohttp.ClientSession(),
            blog_dict
        )

    # Assertions
    assert returned_post_id == post_id
    assert post_print_string == "HEY, LISTEN! \nNew Blog post from" + \
        f" {blog_dict['author']}! Released on {date}!\nTitle: {title} " + \
        f"\nLink:{link}"

    # Additional assertions or checks if needed
    mock_get.assert_called_once_with(
        blog_dict['url'] + '/posts',
        params={'per_page': 1, 'orderby': 'date'}
    )
    mock_response.raise_for_status.assert_called_once()
