#!/bin/bash

# aldatu ondorengo 2 aldagai hauen balioak

# change the values of the next 2 variables (path to this directory
# and resources directory)
rootDir=/kokapena_katalogo_honena/ixa-pipe-dep-eu
baliabideak=$rootDir/dep-eu-resources-v2.0.0


java -jar $rootDir/ixa-pipe-dep-eu-2.0.0-exec.jar -b $baliabideak


# "-c conll_irt_fitx" parametroa gehi dezakezu deian CONLL formatuan ere jasotzeko irteera; adibidez: 
# java -jar $rootDir/target/ixa-pipe-dep-eu-1.0.0-exec.jar -b $baliabideak -c $rootDir/dependentziak.conll

# you can add "-c conll_out_file" parameter in order to get the output also in CONLL format; for example:
# java -jar $rootDir/target/ixa-pipe-dep-eu-1.0.0-exec.jar -b $baliabideak -c $rootDir/dependencies.conll
