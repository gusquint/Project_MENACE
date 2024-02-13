from project import Board,get_options_dic,get_weights_dic,save_options_dic,save_weights_dic,list_to_str,game


def test_init():
    board=Board()
    assert board.list==[" "," "," "," "," "," "," "," "," "]
    board1=Board([1,2,3,4,5,6,7,8,9])
    assert board1.list==[1,2,3,4,5,6,7,8,9]


def test_update():
    board=Board()
    board.update([1,2,3,4,5,6,7,8,9])
    assert board.list==[1,2,3,4,5,6,7,8,9]
    board1=Board()
    board1.update("123456789")
    assert board.list==[1,2,3,4,5,6,7,8,9]


def test_win():
    board=Board(["X","X","X"," "," "," "," "," "," "])
    assert board.win()==True
    board1=Board([" "," "," "," "," "," "," "," "," "])
    assert board1.win()==None


def test_reset():
    board=Board([1,2,3,4,5,6,7,8,9])
    board.reset()
    assert board.list==[" "," "," "," "," "," "," "," "," "]


def test_rotate_90():
    board=Board([1,2,3,4,5,6,7,8,9])
    board.rotate_90()
    assert board.list==[7,4,1,8,5,2,9,6,3]


def test_flip_h():
    board=Board([1,2,3,4,5,6,7,8,9])
    board.flip_h()
    assert board.list==[3,2,1,6,5,4,9,8,7]


def test_copy():
    board=Board([1,2,3,4,5,6,7,8,9])
    board1=board.copy()
    assert board1.list==[1,2,3,4,5,6,7,8,9]


def test_string():
    board=Board(["1","2","3","4","5","6","7","8","9"])
    assert board.string()=="123456789"


def test_get_options_dic():
    assert get_options_dic("not_existing_file.csv")=={}


def test_get_weights_dic():
    assert get_weights_dic("not_existing_file.csv")=={}


def test_save_options_dic():
    save_options_dic({},"test_file.csv")
    assert get_options_dic("test_file.csv")=={}


def test_save_weights_dic():
    save_weights_dic({},"test_file.csv")
    assert get_weights_dic("test_file.csv")=={}


def test_list_to_str():
    assert list_to_str(["1","2","3"])=="123"


def game():
    assert game({},{},"machine",0)==""