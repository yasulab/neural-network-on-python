#!/bin/sh
echo ""
echo "*********************"
echo "***     START     ***"
echo "*********************"
echo ""
cd ../ver-0
echo "*********************"
echo "* binary perceptron *"
echo "*********************"
time sh ../ver-0/easy-test.sh > /dev/null
echo ""
echo "**********************"
echo "* Multi-V perceptron *"
echo "**********************"
echo ""
cd ../ver-1
time sh ../ver-1/easy-test.sh > /dev/null
echo ""
echo "***********************"
echo "* backprop perceptron *"
echo "***********************"
echo ""
cd ../ver-2
time sh ../ver-2/easy-test.sh > /dev/null
echo ""
echo "*************************"
echo "* Nearest Neighbor Rule *"
echo "*************************"
echo ""
cd ../ver-3
time sh ../ver-3/easy-test.sh > /dev/null
echo ""
echo "*********************"
echo "***      END      ***"
echo "*********************"
echo ""
cd ../stats

