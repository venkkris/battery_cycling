%% Clean up
clc;
close all;
clear all;

color = 'r';
filename = 'pretty_plots/coulombic_efficiency.png';
values = fscanf(fopen('main_out/coulombic_efficiencies.txt','r'),'%f');

close all;
figure()
plot(values,'-o','Color', color, 'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
hold on
box on
title('Coulombic efficiency vs Cycles');
xlabel('Cycles');
ylabel('Coulombic efficiency (%)');
% xticks(0:2:18);
% yticks(0:0.5:3);
% xlim([0,17]);

set(gcf, 'Color', 'w');
set(gca, 'FontName', 'Times New Roman', 'FontSize', 20, ... 
    'Linewidth' , 2, 'Fontweight', 'bold');
saveas(gcf, filename)
