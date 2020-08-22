climb() {	
n=$1
if [[ $n -le 0 ]]; then
	n=1
fi
var=	
echo $n
for ((i=1; i<= $n; i++)); do
 var=$var../
done
cd $var
}
