import pytest

# def move_element(index:int,data:list[tuple[int,int]],visited:set[tuple[int,int]]) -> int:
#     L = len(data)
#     while data[index] in visited:
#         index = (index+1)%L
#     item = data.pop(index)
#     new_index = (index+item[1])%L
#     new_index+=(item[1]>0)*(new_index<index)-(item[1]<0)*(new_index>index)
#     data.insert(new_index,item)
#     visited.add(item)
#     return index

# @pytest.mark.parametrize("before,after",
#     [[1,1,0,1,1],[1,1,0,1,1]])
# def test_move_item(before,after):
#     index = move_element(before)
    
#     assert 