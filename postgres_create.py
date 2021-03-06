#!/usr/bin/python
import os
import optparse
import sys

docker = '/usr/bin/docker'
image = 'fredhutch/postgres:9.5'
dbvol = '/var/postgres_dbs'

def createdb(name, dbuser, passwd, owner, description, contact, memlimit):
    try:
        os.popen("mkdir -p %s/%s" % (dbvol, name))
        os.popen("%s run -d -P --name %s --restart on-failure -e POSTGRES_USER=%s \
                 -e POSTGRES_DB=%s -e POSTGRES_PASSWORD=%s -l OWNER=%s -l DESCRIPTION=\"%s\" \
                 -l DBaaS=true -l CONTACT=%s -m=%s -v %s/%s:/var/lib/postgresql/data %s 2>/dev/null" % \
                 (docker, name, dbuser, name, passwd, owner, description, contact, memlimit, dbvol, name, image))
        res = os.popen("%s ps -l --format 'table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Status}}'" % docker).read()
        if __name__ == "__main__":
            print(res)
        else:
            return(res)
    except Exception, e:
        if __name__ == "__main__":
            print("An error occured: %s" % e)
        else:
            return("An error occured: %s" % e)

def main():
    p = optparse.OptionParser(usage="usage: %prog --name=<container/dbname> --dbuser=<username> --password=<password> --owner=<owner> --description='<description>' [--memlimit=<num><m/g> (optional)]", version="%prog 1.0")
    p.add_option('-n', '--name',  action='store', type='string', dest='name', help='Set the name of the container and database')
    p.add_option('-u', '--dbuser',  action='store', type='string', dest='dbuser', help='Set the database username')
    p.add_option('-p', '--password',  action='store', type='string', dest='passwd', help='Set the dbuser\'s password')
    p.add_option('-o', '--owner',  action='store', type='string', dest='owner', help='Set the owner of the container/db')
    p.add_option('-c', '--contact',  action='store', type='string', dest='contact', help='Set database contact (email)')
    p.add_option('-d', '--description',  action='store', type='string', dest='description', help='Set the descriptoin of the container/db')
    p.add_option('-m', '--memlimit',  action='store', type='string', dest='memlimit', help='Set the maximum RAM that the containter can use. Specify "m" for MB and "g" for GB - ex: 512m, 2g (optional) - defaults to 2g if no limit provided')
    opt, args = p.parse_args()

    if len(sys.argv) < 5:
        p.error('use --help for usage information.')
    
    # if a memory limit is not provided, default to 2GB
    if not opt.memlimit:
        opt.memlimit = '2g' 

    createdb(opt.name, opt.dbuser, opt.passwd, opt.owner, opt.description, opt.contact, opt.memlimit)

if __name__ == "__main__":    
    main()
