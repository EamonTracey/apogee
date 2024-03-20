%% Launch Analysis
% This code plots launch data and compares it to predicted launch
% characteristics

% Author: William Teasley
% Date: 2 March 2023
% Completed Individually

clc; clear; close all;

%% Load in data
data = readtable("fullscale_data_03_02_2024_16_26_45.csv"); % March 2nd flight data
[time, state, servoPercentage, apogeePrediction, altitudeFiltered, velocityFiltered, accelerationFiltered, temp, b, c] = truncate_flight(data);
clc

%% Constants
g = 32.17405; % ft/s^2
rho = 0.002247; % slug/ft**3
mass = 1.1902231; % slugs; mass after burnout, so constant
apogee_target = 5200; % ft
dt = 0.02; % Average time between data points

[apogee, t_apogee] = max(altitudeFiltered);
disp("Target Apogee: " + apogee_target + " ft")
disp("ACS Altimeter: " + apogee + " ft")

%% Expected apogee prediction using analytical approximation and on board velocity data
for i = 1:length(time)
    dragOnBoard(i) = calculate_drag(velocityFiltered(i), servoPercentage(i));
    analyticalPrediction(i) = calculate_apogee(dragOnBoard(i), altitudeFiltered(i), velocityFiltered(i), mass);
end

%% Flight path using analytical approximation and theoretical velocity data
[velocityTheoretical(1), bt] = max(velocityFiltered); % velocity after burnout ft/s

altitudeTheoretical(1) = altitudeFiltered(bt); % altitude at burnout feet;
accelerationTheoretical(1) = accelerationFiltered(bt); % ft/s^2
dragTheoretical(1) = calculate_drag(velocityTheoretical(1), 0);

tt = time(bt:end);

for j = 1:length(tt)-1 
    altitudeTheoretical(j+1) = altitudeTheoretical(j) + dt*velocityTheoretical(j); % + randi([-1 1])*0.5;
    velocityTheoretical(j+1) = velocityTheoretical(j) + dt*accelerationTheoretical(j);
    dragTheoretical(j+1) = calculate_drag(velocityTheoretical(j+1), 0);
    accelerationTheoretical(j+1) = -1*g - dragTheoretical(j)/mass;
    apogee_projected_theoretical(j+1) = calculate_apogee(dragTheoretical(j), altitudeTheoretical(j+1), velocityTheoretical(j+1), mass);
end

%% Style values
linewidth = 1;
pointSize = 20;
circleSize = 7.5; 
fontSize = 14;
color1 = '#A2142F'; % red 
color2 =  '#0072BD'; % blue 
color3 = '#7E2F8E'; % purple
color4 = '#77AC30' ; % green
color5 = 'k'; % black
color6 = '#D95319'; % orange

%% Plot
f1=figure(1);
plot(time, altitudeFiltered, 'LineWidth',linewidth,'Color',color1);
% plot(time(bt:end), (altitudeFiltered(bt:end)-altitudeTheoretical'), 'LineWidth',linewidth,'Color',color1);
hold on
plot(tt, altitudeTheoretical, 'LineWidth',linewidth,'Color',color2);
yline(apogee_target, 'k-', 'LineWidth', 1.2);
xline(time(t_apogee))
xline(time(b), 'Color',color5)
xline(time(bt), 'Color',color6)
xline(time(c), '--','Color',color6)
grid on
legend('Measured Altitude', 'Theoretical Altitude', 'Target Apogee', 'Apogee Detection', 'Burnout Detection', 'Actual Burnout', 'Flap Deployment', 'FontSize', fontSize, 'Location', 'southeast'); % Legend
xlabel('t, s') % Add axis labels
ylabel('y(t), ft')
title('ACS Flight')
f1.Position = [100,100,800,500]; 
% axis([0 30 4800 apogee_projected(1)*3.281])

f2=figure(2);
plot(time, apogeePrediction, '-', 'LineWidth',linewidth,'Color',color4);
hold on
plot(time, analyticalPrediction, '-', 'LineWidth',linewidth,'Color',color6);
plot(tt, apogee_projected_theoretical, '-', 'LineWidth',linewidth,'Color',color5);
yline(apogee_target, 'k-', 'LineWidth', 1.2);
yline(apogee, 'Color',color3)
xline(time(t_apogee))
xline(time(b), 'Color',color5)
xline(time(bt), 'Color',color6)
xline(time(c), '--','Color',color6)
grid on
legend('On-Board Predicted Apogee', "William's predicted Apogee using flight data", 'Theoretical apogee prediction using analyitcal methods', 'Target Apogee', 'Measured Apogee', 'Apogee Detection', 'Burnout Detection', 'Actual Burnout', 'Flap Deployment', 'Location','southeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('y(t), ft')
title('ACS Flight')
f2.Position = [100,100,800,500]; % this is based on your screen and preference

f3=figure(3);
plot(time, velocityFiltered, '-', 'LineWidth',linewidth,'Color',color1);
hold on
plot(time, accelerationFiltered, '-', 'LineWidth',linewidth,'Color',color2);
plot(tt, velocityTheoretical, '-', 'LineWidth',linewidth,'Color',color3);
plot(tt, accelerationTheoretical, '-', 'LineWidth',linewidth,'Color',color4);
xline(time(b), 'Color',color5)
xline(time(bt), 'Color',color6)
xline(time(c), '--','Color',color6)
grid on
legend('Measured Velocity', 'Measured Acceleration', 'Theoretical Velocity', 'Theoretical Acceleration', 'Burnout Detection', 'Actual Burnout', 'Flap Deployment', 'Location','northeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('v(t), ft/s, a(t), ft/s^2')
title('ACS Flight')
f3.Position = [100,100,800,500]; % this is based on your screen and preference


% 
% f4=figure(4);
% plot(time, servo_angle, 'g-', 'LineWidth', 1.2);
% grid on
% legend('Servo Angle', 'Location','northeast') % Legend
% xlabel('t, s') % Add axis labels
% ylabel('Servo Angle')
% title('ACS Flight')
% f4.Position = [100,100,800,500]; % this is based on your screen and preference
% 
% f5=figure(5);
% plot(time, -1* e, 'r--', 'LineWidth', 1.2);
% grid on
% legend('Error', 'Location','northeast') % Legend
% xlabel('t, s') % Add axis labels
% ylabel('Error, m')
% title('ACS Flight')
% f5.Position = [100,100,800,500]; % this is based on your screen and preference
% 
% f6=figure(6);
% plot(time, D, '-', 'LineWidth',linewidth,'Color',color6);
% grid on
% legend('Drag', 'FontSize', fontSize, 'Location', 'southeast'); % Legend
% xlabel('t, s') % Add axis labels
% ylabel('D(t), Lbf')
% title('ACS Flight')
% f6.Position = [100,100,800,500]; 