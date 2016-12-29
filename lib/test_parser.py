from lib.ExcelParser import DataParser, Comparator
import pprint
import argparse

from operator import itemgetter

parser = argparse.ArgumentParser(description='This is a demo script by nixCraft.')
parser.add_argument('-s','--source', help='Source file name',required=True)
parser.add_argument('--sstart',help='Source start row', required=True)
parser.add_argument('--snumber',help='Source number col', required=True)
parser.add_argument('--sprice',help='Source price col', required=True)

parser.add_argument('-c','--compare',help='Compare file name', required=True)
parser.add_argument('--cstart',help='Compare start row', required=True)
parser.add_argument('--cnumber',help='Compare number col', required=True)
parser.add_argument('--cprice',help='Compare price col', required=True)

args = parser.parse_args()

parser = DataParser()
source_file = open(args.source, 'rb');
source_data = parser.parse_file(excelContent=source_file.read(),
                                start_row=int(args.sstart),
                                number_col=int(args.snumber),
                                price_col=int(args.sprice))
source_file.close()

compare_file = open(args.compare, 'rb');
compare_data = parser.parse_file(excelContent=compare_file.read(),
                                 start_row=int(args.cstart),
                                 number_col=int(args.cnumber),
                                 price_col=int(args.cprice))
compare_file.close()

comparator = Comparator()

result = comparator.compare_data(source=source_data,
                                 compare=compare_data)

result = sorted(result, key=itemgetter(3,2))

count = 1
for item in result:
    item.insert(0, str(count))
    l = tuple(item)
    print("%s: %s ряд: %s № %s - %s" % l)
    count += 1
