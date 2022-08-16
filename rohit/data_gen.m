clc;
clear all;

BFG_1 = xlsread("LC709203F_5.csv");
BFG_2 = xlsread("MAX17043_5.csv");

BFG_arbin = xlsread('BFG_take_2_Channel_2_Wb_1.CSV');

BFG_ar_cur = BFG_arbin(:,7);
BFG_ar_vol = BFG_arbin((244:end),8);

BFG_1_vol = BFG_1((335:end),1);
BFG_2_vol = BFG_2((337:end),1);


h =figure;
plot(BFG_1_vol,LineWidth=1.5);
hold on;
plot(BFG_2_vol,LineWidth=1.5);
legend('BFG_1 (Adafruit)','BFG_2 (Maximum Integrated)','Arbin');
plot(BFG_ar_vol,LineWidth=1.5);
title('Voltage Comparison');
