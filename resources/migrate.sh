SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

export $(grep -v '^#' $SCRIPTPATH/../.env | xargs)
python3 $SCRIPTPATH/../app/manage.py migrate
