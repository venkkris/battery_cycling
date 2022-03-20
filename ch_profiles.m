%% Clean up
clc;
close all;
clear all;



color1 = sscanf('53a4ec','%2x%2x%2x',[1 3])/255;
color2 = sscanf('187dd8','%2x%2x%2x',[1 3])/255;
color3 = sscanf('1360a6','%2x%2x%2x',[1 3])/255;
color4 = sscanf('0f497d','%2x%2x%2x',[1 3])/255;
color5 = sscanf('092d4d','%2x%2x%2x',[1 3])/255;

filename = 'charge_profiles.png';
values1 = readmatrix('charge_1.csv');
values2 = readmatrix('charge_2.csv');
values3 = readmatrix('charge_3.csv');
values4 = readmatrix('charge_4.csv');
values5 = readmatrix('charge_5.csv');


close all;
figure()
hold on
p(1) = plot(values1(:,1), values1(:,2),'-','Color', color1, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(2) = plot(values2(:,1), values2(:,2),'-','Color', color2, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(3) = plot(values3(:,1), values3(:,2),'-','Color', color3, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(4) = plot(values4(:,1), values4(:,2),'-','Color', color4, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(5) = plot(values5(:,1), values5(:,2),'-','Color', color5, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');

box on
legend(p, {'Cycle 1','Cycle 2','Cycle 3','Cycle 4','Cycle 5'})
legend('Box','off', 'Location','east')
title('Charge profiles');
xlabel('Capacity (mAh)');
ylabel('Voltage (V)');

xticks(0:0.5:3);
yticks(1.5:0.5:4.8);
xlim([0,3]);
ylim([1.5,4.8]);

set(gcf, 'Color', 'w');
set(gca, 'FontName', 'Times New Roman', 'FontSize', 20, ... 
    'Linewidth' , 2, 'Fontweight', 'bold');

saveas(gcf, filename)
