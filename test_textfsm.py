import pytest
from textfsmlab import choose_device

def test_R0():
    output = choose_device("R0")
    assert output.get('Gig 0/0') == "Connect to Gig 0/0 of S0"

def test_R1():
    output = choose_device("R1")
    assert output.get('Gig 0/0') == "Connect to Gig 0/1 of S0"
    assert output.get('Gig 0/1') == "Connect to PC"
    assert output.get('Gig 0/2') == "Connect to Gig 0/1 of R2"

def test_R2():
    output = choose_device("R2")
    assert output.get('Gig 0/0') == "Connect to Gig 0/2 of S0"
    assert output.get('Gig 0/1') == "Connect to Gig 0/2 of R1"
    assert output.get('Gig 0/2') == "Connect to Gig 0/1 of S1"
    assert output.get('Gig 0/3') == "Connect to WAN"

def test_S0():
    output = choose_device("S0")
    assert output.get('Gig 0/0') == "Connect to Gig 0/0 of R0"
    assert output.get('Gig 0/1') == "Connect to Gig 0/0 of R1"
    assert output.get('Gig 0/2') == "Connect to Gig 0/0 of R2"
    assert output.get('Gig 0/3') == "Connect to Gig 0/0 of S1"

def test_S1():
    output = choose_device("S1")
    assert output.get('Gig 0/0') == "Connect to Gig 0/3 of S0"
    assert output.get('Gig 0/1') == "Connect to Gig 0/2 of R2"
    assert output.get('Gig 1/1') == "Connect to PC"

if __name__ == "__main__":
    test_R0()
    test_R1()
    test_R2()
    test_S0()
    test_S1()