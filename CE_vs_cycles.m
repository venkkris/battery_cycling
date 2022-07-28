%% Clean up
clc;
close all;
clear all;

color = 'b';
filename = 'pretty_plots/coulombic_efficiency.png';
values = fscanf(fopen('main_out/coulombic_efficiencies.txt','r'),'%f');

close all;
figure()
plot(values,'-','Color', color, 'LineWidth', 3, 'MarkerSize', 15, 'HandleVisibility', 'off');
hold on
box on
plot([0,length(values)],[100,100], '--', 'Color', 'k', 'LineWidth', 3, 'HandleVisibility', 'off');
title('Coulombic efficiency vs Cycles');
xlabel('Cycles');
ylabel('Coulombic efficiency (%)');
yticks(round(min(values)-2):3:round(max(values)+2));
xlim([0,length(values)+1]);
ylim([min(values)-2, max(values)+2]);

set(gcf, 'Color', 'w');
set(gca, 'FontName', 'Times New Roman', 'FontSize', 20, ... 
    'Linewidth' , 2, 'Fontweight', 'bold');
saveas(gcf, filename)
