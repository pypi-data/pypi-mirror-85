"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import sys
import argparse


def version(basename):
  vfile=os.path.join((os.path.dirname(os.path.relpath(__file__))), '..', 'VERSION')
  if not os.path.exists(vfile):
    return "{} version: unknown".format(basename)
  fh = open(vfile, 'r')
  version = fh.readline().strip()
  fh.close()
  return "{} version: {}".format(basename, version)

def parse(basename):
  ap = argparse.ArgumentParser(
    add_help=False, epilog="{} <command> -h lists command specific options".format(basename))
  ap._positionals.title = 'commands'  # Not very clean, but whatddya want to do?
  ap.add_argument('--version', action='store_true', help='Show version and exit')
  ap.add_argument('-v', '--verbose', action='count', default=0)
  ap.add_argument('--apikey', type=str, default=None)

  db = argparse.ArgumentParser(add_help=False)
  db.add_argument('-db', '--database', type=str, default=None, metavar='<path>',
                  help="Path for local database")

  outfmt = argparse.ArgumentParser(add_help=False)
  outfmt.add_argument('-x', '--xml', default=False, action='store_true', help='Output XML')

  taxa = argparse.ArgumentParser(add_help=False)
  taxa.add_argument('-t', '--taxids', type=str, nargs='*', default=None, metavar='<taxid>',
                    help='Comma / space separated taxids')
  taxa.add_argument('-n', '--names', type=str, nargs='*', default=None, metavar='<name>',
                    help='Comma separated names: \'Homo sapiens\', \'Influenza B virus \
                         (B/Acre/121609/2012)\'')

  remote = argparse.ArgumentParser(add_help=False)
  remote.add_argument('-r', '--remote', action='store_true', default=False,
                      help='Use Entrez server')

  email = argparse.ArgumentParser(add_help=False)
  email.add_argument('-e', '--email', type=str, default=None, metavar='<email>',
                     help='Email, required for remote queries')

  subparsers = ap.add_subparsers(dest='command')
  mapper = subparsers.add_parser('map', help='Map taxid to names and vice-versa',
                                 parents=[taxa, db, remote, email, outfmt])
  mapper.add_argument('-a', '--accessions', type=str, nargs='*', default=None,
                       metavar='<accs>', help='Map accessions to taxa')
  mapper.add_argument('-edb', '--entrezdb', type=str, metavar='<entrezdb>', default='nucleotide',
                      help='Entrez database for accessions. Default: nucleotide')

  resolve = subparsers.add_parser('resolve', help='Resolve lineage',
                                  parents=[taxa, db, remote, email, outfmt])
  resolve.add_argument('-m', '--mapping', default=False, action='store_true',
                       help='Resolve accessions mapping from map via STDIN')

  importer = subparsers.add_parser('import', help='import taxa into SQLite database', parents=[db])
  importer.set_defaults(email=None, xml=None)
  #importer.add_argument('-f', '--filter', default=None, type=str, metavar='<attribute>',
                        #help='Set attribute to print to STDOUT after import: accs, taxid, lin')

  collector = subparsers.add_parser('collect', help='Collect taxa information from Entrez',
                                    parents=[taxa, email, outfmt]).set_defaults(database=None)

  subtree = subparsers.add_parser('subtree', help='Extract subtree from given taxa or lineages',
                                  parents=[taxa, db, outfmt])
  subtree.set_defaults(email=None)
  subtree.add_argument('--rank', default=None, help='extract this rank')
  subtree.add_argument('--lrank', default=None, help='Extract from lower rank, further from root')
  subtree.add_argument('--hrank', default=None, help='Extract to higher rank, closer to root')

  group = subparsers.add_parser('group', help='Organize taxa groups in local database',
                                parents=[taxa, db])
  group.set_defaults(email=None, xml=None)
  group.add_argument('--add', type=str, metavar='<groupname>', help='Add to <groupname>')
  group.add_argument('--rm', type=str, metavar='<groupname>', help='Remove from <groupname>. \
                      Without given taxid or names remove group.')
  group.add_argument('--list', action='store_true', help='List groups')
  group.add_argument('--get', type=str, nargs='*', default=None, metavar='<groupname>',
                     help='Get taxids for groups')

  if len(sys.argv) == 1:
    ap.print_help()
    sys.exit(0)
  args = ap.parse_args()
  if args.version:
    print(version(basename))
    sys.exit(0)
  return args
