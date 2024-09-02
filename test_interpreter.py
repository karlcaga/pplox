from pplox.parser import Parser 
from pplox.scanner import Scanner
from pplox.interpreter import Interpreter, to_string
from pplox.interpreter_error import InterpreterError
import pytest

def evaluate(source, capsys):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    Interpreter().interpret(parser.parse())
    captured = capsys.readouterr()
    return captured.out[:-1]

def test_print(capsys):
    evaluate('print "hello world";', capsys) == "hello world" 

def evaluate_as_print_and_capture_output(source, capsys):
    scanner = Scanner("print " + source + ";")
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    Interpreter().interpret(parser.parse())
    captured = capsys.readouterr()
    return captured.out[:-1]

def test_true_false_nil(capsys):
    assert evaluate_as_print_and_capture_output('true', capsys) == "true"
    assert evaluate_as_print_and_capture_output('false', capsys) == "false"
    assert evaluate_as_print_and_capture_output('nil', capsys) == "nil"

def test_string(capsys):
    assert evaluate_as_print_and_capture_output('"hello world"', capsys) == "hello world"

def test_numbers(capsys):
    assert evaluate_as_print_and_capture_output("10", capsys) == "10"
    assert evaluate_as_print_and_capture_output("9.480", capsys) == "9.48"
    assert evaluate_as_print_and_capture_output("2.30", capsys) == "2.3"

def test_grouping(capsys):
    assert evaluate_as_print_and_capture_output('("hello world!")', capsys) == 'hello world!'
    assert evaluate_as_print_and_capture_output("(true)", capsys) == "true"
    assert evaluate_as_print_and_capture_output("((false))", capsys) == "false"
    assert evaluate_as_print_and_capture_output("(123.40)", capsys) == "123.4"

def test_truthy(capsys):
    assert evaluate_as_print_and_capture_output("-73", capsys) == "-73"
    assert evaluate_as_print_and_capture_output("!true", capsys) == "false"
    assert evaluate_as_print_and_capture_output("!10.40", capsys) == "false"
    assert evaluate_as_print_and_capture_output("!((false))", capsys) == "true"

def test_multiplication_division(capsys):
    assert evaluate_as_print_and_capture_output("8 * 8", capsys) == "64"
    assert evaluate_as_print_and_capture_output("80 / 10", capsys) == "8" 

def test_minus_plus(capsys):
    assert evaluate_as_print_and_capture_output("20 + 74 - (-(14 - 33))", capsys) == "75"

def test_concat(capsys):
    assert evaluate_as_print_and_capture_output('"Hello" + " world"', capsys) == "Hello world"
    assert evaluate_as_print_and_capture_output('"42" + "42"', capsys) == "4242"

def test_greater_less(capsys):
    assert evaluate_as_print_and_capture_output("123 >= 123", capsys) == "true"
    assert evaluate_as_print_and_capture_output("124 > 123", capsys) == "true"
    assert evaluate_as_print_and_capture_output("12837 < 1283", capsys) == "false"
    assert evaluate_as_print_and_capture_output("321 <= 321", capsys) == "true"

def test_equality(capsys):
    assert evaluate_as_print_and_capture_output('"foo" != "bar"', capsys) == "true"
    assert evaluate_as_print_and_capture_output('"hello" == "world"', capsys) == "false"
    assert evaluate_as_print_and_capture_output('"foo" == "foo"', capsys) == "true"

def test_negation_error_handling(capsys):
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('-"foo"', capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('-("foo" + "bar")', capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('-true', capsys)

def test_operand_type_error(capsys):
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('"foo" * 42', capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output("true / 2", capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('("foo" * "bar")', capsys)

def test_plus_type_error(capsys):
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('"foo" + true', capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('42 - true', capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('true + false', capsys)

def test_relational_type_error(capsys):
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('"foo" < false', capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('("foo" + "bar") < 42', capsys)
    with pytest.raises(InterpreterError):
        evaluate_as_print_and_capture_output('false > true', capsys)
