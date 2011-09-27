from datautil.date import *

import datetime

class TestPythonStringOrdering(object):
    # It is impossible to find a string format such that +ve and -ve numbers
    # sort correctly as strings:
    # if (in string ordering) X < Y => -X < -Y (False!)
    def test_ordering(self):
        assert '0' < '1'
        assert '-10' < '10'
        assert '-' < '@'
        assert '-' < '0'
        assert '-100' < '-X10'
        assert '10' < '1000'
        assert '02000' < '10000'
        assert ' 2000' < '10000'

    def test_bad_ordering(self):
        assert ' ' < '0'
        assert ' ' < '-'
        assert not '-' < '+'
        assert '-100' > '-10'
        assert not '-100' < '-010'
        assert not '-100' < '- 10'
        assert not '-100' < ' -10'
        assert '10000' < '2000'
        assert not '-10' < ' 1'
        

class TestFlexiDate(object):
    def test_init(self):
        fd = FlexiDate()
        assert fd.year == '', fd
        assert fd.month == '', fd

        fd = FlexiDate(2000, 1,1)
        assert fd.month == '01', fd
        assert fd.day== '01', fd

    def test_str(self):
        fd = FlexiDate(2000, 1, 23)
        assert str(fd) == '2000-01-23', '"%s"' % fd
        fd = FlexiDate(-2000, 1, 23)
        assert str(fd) == '-2000-01-23'
        fd = FlexiDate(2000)
        assert str(fd) == '2000'
        fd = FlexiDate(1760, qualifier='fl.')
        assert str(fd) == '1760 [fl.]', fd

        fd = FlexiDate(qualifier='anything')
        assert str(fd) == ' [anything]'


    def test_from_str(self):
        def dotest(fd):
            out = FlexiDate.from_str(str(fd))
            assert str(out) == str(fd)

        fd = FlexiDate(2000, 1, 23)
        dotest(fd)
        fd = FlexiDate(1760, qualifier='fl.')
        dotest(fd)
        fd = FlexiDate(-1760, 1, 3, qualifier='fl.')
        dotest(fd)
    
    def test_as_float(self):
        fd = FlexiDate(2000)
        assert fd.as_float() == float(2000), fd.as_float()
        fd = FlexiDate(1760, 1, 2)
        exp = 1760 + 1/12.0 + 2/365.0
        assert fd.as_float() == exp, fd.as_float()
        fd = FlexiDate(-1000)
        assert fd.as_float() == float(-1000)

    def test_as_datetime(self):
        fd = FlexiDate(2000)
        out = fd.as_datetime()
        assert out == datetime.datetime(2000, 1, 1), out
        fd = FlexiDate(1760, 1, 2)
        out = fd.as_datetime()
        assert out == datetime.datetime(1760,1,2), out


class TestDateParsers(object):
    def test_using_datetime(self):
        parser = PythonDateParser()

        d1 = datetime.date(2000, 1, 23)
        fd = parser.parse(d1)
        assert fd.year == '2000'

        d1 = datetime.datetime(2000, 1, 23)
        fd = parser.parse(d1)
        # assert str(fd) == '2000-01-23T00:00:00', fd
        assert str(fd) == '2000-01-23', fd

    def test_using_dateutil(self):
        parser = DateutilDateParser()

        in1 = '2001-02'
        fd = parser.parse(in1)
        assert str(fd) == in1, fd

        in1 = 'March 1762'
        fd = parser.parse(in1)
        assert str(fd) == '1762-03'

        in1 = 'March 1762'
        fd = parser.parse(in1)
        assert str(fd) == '1762-03'

        in1 = '1768 AD'
        fd = parser.parse(in1)
        assert str(fd) == '1768', fd

        in1 = '1768 A.D.'
        fd = parser.parse(in1)
        assert str(fd) == '1768', fd

        in1 = '-1850'
        fd = parser.parse(in1)
        assert str(fd) == '-1850', fd

        in1 = '1762 BC'
        fd = parser.parse(in1)
        assert str(fd) == '-1762', fd

        in1 = '4 BC'
        fd = parser.parse(in1)
        assert str(fd) == '-0004', fd

        in1 = '4 B.C.'
        fd = parser.parse(in1)
        assert str(fd) == '-0004', fd

        in1 = 'Wed, 06 Jan 2010 09:30:00 GMT'
        fd = parser.parse(in1)
        assert str(fd) == '2010-01-06', fd

        in1 = 'Tue, 07 Dec 2010 10:00:00 GMT'
        fd = parser.parse(in1)
        assert str(fd) == '2010-12-07', fd

    def test_parse(self):
        d1 = datetime.datetime(2000, 1, 23)
        fd = parse(d1)
        assert fd.year == '2000'

        fd = parse('March 1762')
        assert str(fd) == '1762-03'

        fd = parse(1966)
        assert str(fd) == '1966'

        fd = parse('22/07/2010')
        assert fd.month == '07', fd.month

    def test_parse_ambiguous_day_month(self):
        fd = parse('05/07/2010')
        assert fd.month == '07', fd.month
        assert fd.day == '05', fd.month

    def test_parse_with_none(self):
        d1 = parse(None)
        assert d1 is None
    
    def test_parse_wildcards(self):
        fd = parse('198?')
        assert fd.year == '', fd.year # expect this to not parse
        # TODO but we should have a float if possible
#        assert fd.as_float() == u'1980', fd.as_float()

    def test_parse_with_qualifiers(self):
        fd = parse('1985?')
        assert fd.year == u'1985', fd
        assert fd.qualifier == u'Uncertainty : 1985?', fd.qualifier

        fd = parse('c.1780')
        assert fd.year == u'1780', fd
        assert fd.qualifier == u"Note 'circa' : c.1780", fd

        fd = parse('c. 1780')
        assert fd.year == u'1780', fd
        assert fd.qualifier.startswith(u"Note 'circa'"), fd

    def test_ambiguous(self):
        # TODO: have to be careful here ...
        fd = parse('1068/1069')

    def test_small_years(self):
        in1 = '23'
        fd = parse(in1)
        assert str(fd) == '0023', fd
        assert fd.as_float() == 23, fd.as_float()

    def test_small_years_with_zeros(self):
        in1 = '0023'
        fd = parse(in1)
        assert str(fd) == '0023', fd
        assert fd.as_float() == 23, fd.as_float()

    def test_years_with_alpha_prefix(self):
        in1 = "p1980"
        fd = parse(in1)
        assert str(fd) == "1980", fd
        
