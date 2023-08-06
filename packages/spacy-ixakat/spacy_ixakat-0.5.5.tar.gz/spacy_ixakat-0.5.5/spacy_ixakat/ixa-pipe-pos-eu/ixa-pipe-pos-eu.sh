#!/bin/sh
export IXA_PREFIX=`dirname "$(readlink -f "$0")"`;
export PATH=${IXA_PREFIX}/bin:${PATH};
export LD_LIBRARY_PATH=${IXA_PREFIX}/lib:${IXA_PREFIX}/lib/swipl-5.10.5/lib/x86_64-linux:${LD_LIBRARY_PATH};
cd $IXA_PREFIX;
ixa-pipe-pos-eu
