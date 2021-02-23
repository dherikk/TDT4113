import main as m

def test_Stack():
    stack = m.Stack()
    stacklist = [i for i in range(15)]
    for e in stacklist:
        stack.push(e)
    assert stack.isEmpty() == False
    for i in reversed(range(15)):
        last = stack.pop()
        assert last == i
    assert stack.isEmpty() == True

def test_Queue():
    queue = m.Queue()
    queuelist = [i for i in range(15)]
    for e in queuelist:
        queue.push(e)
    assert queue.isEmpty() == False
    for i in range(15):
        last = queue.pop()
        assert last == i
    assert queue.isEmpty() == True

def test_RPN():
    calc = m.Calculator()
    calc.output_queue.push(7)
    calc.output_queue.push(calc.functions['EXP'])
    assert round(calc.calculate_rpn(), 6) == round(m.np.exp(7), 6)
    
def test_calculate_to_RPN():
    calc = m.Calculator()
    calc.calculate_to_rpn([
        calc.functions['EXP'],
        '(',
        2,
        calc.operators['MULTIPLY'],
        3,
        calc.operators['ADD'],
        1,
        ')'
        ])

    temp_l = calc.output_queue._items
    global temp_l2
    temp_l2 = [
        m.nu.Number,
        m.nu.Number,
        m.Operator,
        m.nu.Number,
        m.Operator,
        m.Function
    ]
    for i in temp_l:
        assert isinstance(i, temp_l2[temp_l.index(i)])

def test_text_parse():
    calc = m.Calculator()
    temp_l3 = calc.text_parse("2 2 add 2 multiply sin")
    for i in temp_l3:
        assert isinstance(i, temp_l2[temp_l3.index(i)])

def test_all():
    calc = m.Calculator()
    test = "((15 DIVIDE (7 SUBTRACT (1 ADD 1))) MULTIPLY 3) SUBTRACT (2 ADD (1 ADD 1))"
    test2 = "15 ADD 700 ADD 7"
    var1 = calc.calculate_expression(test)
    var2 = calc.calculate_expression(test2)
    assert int(var1) == 5
    assert int(var2) == 722



def main():
    test_Stack()
    test_Queue()
    test_RPN()
    test_calculate_to_RPN()
    test_text_parse()
    test_all()

if __name__ == '__main__':
    main()
