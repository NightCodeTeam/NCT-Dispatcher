from app.core.requests_makers import HttpMaker, HttpMakerAsync



def test_maker_single():
    maker = HttpMaker()
    assert HttpMaker() is maker
    maker_async = HttpMakerAsync()
    assert HttpMakerAsync() is maker_async
    assert maker is not maker_async

"""
def test_maker_sync():
    maker = HttpMaker('https://not-exist-ololo-example.max', make_cache=False)

    mock = Mock()
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {
        "ok": True,
    }

    with patch('requests.get', return_value=mock) as mock_get:
        assert maker._make('https://example.com', 'GET').json == {'ok': True}
"""