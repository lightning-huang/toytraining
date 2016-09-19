import ConfigParser,sys,netprinter

config=ConfigParser.ConfigParser();
if len(sys.argv)<3:
	print "usage: python clear_fastrank_models.py xxx.ini output.ini"
	sys.exit(1)
	

netpath=sys.argv[1]
outpath=sys.argv[2]
config.read(netpath)


out=file(outpath,'w')
netprinter.print_tree_ensemble(config, out)
out.close()

