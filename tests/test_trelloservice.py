# module imports
from trellocli import SUCCESS
from trellocli.trelloservice import TrelloService
from trellocli.models import *

# dependencies imports

# misc imports

def test_get_access_token(mocker):
    """Test to check success retrieval of user's access token"""
    mock_res = GetOAuthTokenResponse(
        token="test",
        token_secret="test",
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.get_user_oauth_token",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.get_user_oauth_token()

    assert res.status_code == SUCCESS

def test_get_all_boards(mocker):
    """Test to check success retrieval of all trello boards"""
    mock_res = GetAllBoardsResponse(
        res=[],
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.get_all_boards",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.get_all_boards()

    assert res.status_code == SUCCESS

def test_get_board(mocker):
    """Test to check success retrieval of trello board"""
    mock_res = GetBoardResponse(
        res=None,
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.get_board",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.get_board(board_id="test")

    assert res.status_code == SUCCESS

def test_get_all_lists(mocker):
    """Test to check success retrieval of all lists from trello board"""
    mock_res = GetAllListsResponse(
        res=[],
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.get_all_lists",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.get_all_lists(board=None)

    assert res.status_code == SUCCESS

def test_get_list(mocker):
    """Test to check success retrieval of a list from trello board"""
    mock_res = GetListResponse(
        res=None,
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.get_list",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.get_list(board=None, list_id="")

    assert res.status_code == SUCCESS

def test_get_all_labels(mocker):
    """Test to check success retrieval of all labels from trello board"""
    mock_res = GetAllLabelsResponse(
        res=[],
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.get_all_labels",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.get_all_labels(board=None)

    assert res.status_code == SUCCESS

def test_get_label(mocker):
    """Test to check success retrieval of a label from trello board"""
    mock_res = GetLabelResponse(
        res=None,
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.get_label",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.get_label(board=None, label_id="")

    assert res.status_code == SUCCESS

def test_add_card(mocker):
    """Test to check success addition of a new card to trello board"""
    mock_res = AddCardResponse(
        res=None,
        status_code=SUCCESS
    )
    mocker.patch(
        "trellocli.trelloservice.TrelloService.add_card",
        return_value=mock_res
    )
    trellojob = TrelloService()
    res = trellojob.add_card(col=None,name="")

    assert res.status_code == SUCCESS
