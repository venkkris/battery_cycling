%% Clean up
clc;
close all;
clear all;


% cycle_num = [1, 50, 100, 150, 200];
cycle_num = [1, 5, 10, 15, 20];
filename = 'selected_profiles.png';
vlim = [1.5, 4.6];

legend_str = {'Cycle '+string(cycle_num(1)), 'Cycle '+string(cycle_num(2)), 'Cycle '+string(cycle_num(3)), 'Cycle '+string(cycle_num(4)), 'Cycle '+string(cycle_num(5))};

color1 = sscanf('53a4ec','%2x%2x%2x',[1 3])/255;
color2 = sscanf('187dd8','%2x%2x%2x',[1 3])/255;
color3 = sscanf('1360a6','%2x%2x%2x',[1 3])/255;
color4 = sscanf('0f497d','%2x%2x%2x',[1 3])/255;
color5 = sscanf('092d4d','%2x%2x%2x',[1 3])/255;

close all;
figure()
hold on

values1 = readmatrix('cycles/charge_'+string(cycle_num(1))+'.csv');
values2 = readmatrix('cycles/charge_'+string(cycle_num(2))+'.csv');
values3 = readmatrix('cycles/charge_'+string(cycle_num(3))+'.csv');
values4 = readmatrix('cycles/charge_'+string(cycle_num(4))+'.csv');
values5 = readmatrix('cycles/charge_'+string(cycle_num(5))+'.csv');

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

values1 = readmatrix('cycles/discharge_'+string(cycle_num(1))+'.csv');
values2 = readmatrix('cycles/discharge_'+string(cycle_num(2))+'.csv');
values3 = readmatrix('cycles/discharge_'+string(cycle_num(3))+'.csv');
values4 = readmatrix('cycles/discharge_'+string(cycle_num(4))+'.csv');
values5 = readmatrix('cycles/discharge_'+string(cycle_num(5))+'.csv');

p(6) = plot(values1(:,1), values1(:,2),'-','Color', color1, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(7) = plot(values2(:,1), values2(:,2),'-','Color', color2, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(8) = plot(values3(:,1), values3(:,2),'-','Color', color3, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(9) = plot(values4(:,1), values4(:,2),'-','Color', color4, ...
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
p(10) = plot(values5(:,1), values5(:,2),'-','Color', color5, ...    
    'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');


box on
legend(p, legend_str)
legend('Box','off', 'Location','east')
title('Charge/discharge profiles');
xlabel('Capacity (mAh)');
ylabel('Voltage (V)');

%xticks(0:0.5:3);
yticks(vlim(1):0.5:vlim(2));
% xlim([0,3]);
ylim(vlim);

set(gcf, 'Color', 'w');
set(gca, 'FontName', 'Times New Roman', 'FontSize', 20, ... 
    'Linewidth' , 2, 'Fontweight', 'bold');

saveas(gcf, filename)
