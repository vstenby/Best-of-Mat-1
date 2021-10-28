def check_tag(tag):
    '''
    Checks the syntax of tags.
    '''
    
    assert len(tag) == 7, f'Error with {tag}: tag should have length 7.'
    assert tag[0] in ['E', 'F'], f'Error with {tag}: the first character of the tag should either be E (Efterår) or F (Forår)'
    try:
        year = int(tag[1:2])
        assert year >= 0, f'{tag} is an invalid tag.'
    except:
        raise ValueError(f'Error with {tag}: tag[1:2] should be numbers specifying the year.')
    
     #This will exclude GEs, but we'll cross that bridge when we get to it...
    assert tag[3] in ['A', 'B', 'C'], f'Error with {tag}: tag[3] should specify the skema, either A, B or C.'
    assert tag[4] == 'L', f'{tag} is an invalid tag.'

    try: 
        lecture_number = int(tag[5:7])
        assert lecture_number >= 1
    except:
        raise ValueError(f'Error with {tag}: tag[5:7] should be numbers specifying the lecture. First lecture number is 01.')

    return