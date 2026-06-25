from unittest.mock import patch, MagicMock

# Testing crud.py
@patch("crud.supabase")
def test_insert_restaurant(mock_supabase):
    table = MagicMock()
    table.select.return_value.eq.return_value.execute.return_value.data = []
    table.insert.return_value.execute.return_value.data = [{"id": 2, "name": "Joe's Pizza"}]
    mock_supabase.table.return_value = table
 
    from crud import insert_restaurant
    result = insert_restaurant("place_456", "Joe's Pizza", "123 Main St", 2, 4.5)
    assert result["name"] == "Joe's Pizza"
    
# Testing the search and budget filter
@patch("search.insert_restaurant")
@patch("search.requests.post")
def test_search_by_budget(mock_post, mock_insert):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "places": [
            {"id": "abc", "displayName": {"text": "JohnPizza"}, "formattedAddress": "155 W 51st St", "priceLevel": "PRICE_LEVEL_VERY_EXPENSIVE", "rating": 4.8},
            {"id": "def", "displayName": {"text": "JoePizza"}, "formattedAddress": "7 Carmine St", "priceLevel": "PRICE_LEVEL_INEXPENSIVE", "rating": 4.0}
        ]
    }
    
    from search import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        response = c.get("/search?query=pizza&budget=1")
    assert b"JohnPizza" not in response.data
    assert b"JoePizza" in response.data
