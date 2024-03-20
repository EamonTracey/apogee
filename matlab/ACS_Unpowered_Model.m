%% ACS_Unpowered_Model.m
% PID Forward Loop Model

% Author: William Teasley
% Date: 4 August 2023
% Completed Individually

% Clear memory
clear

% Clear Command Window
clc

%% Set Parameters
tmin = 0; % Start time
tmax = 50; % End time
dt = 0.01; % Step
t = tmin:dt:tmax;
% tau = 0.001; % time delay

%% Constants
g = 9.81; % m/s**2
% cd = 0.3; % drag coefficient of rocket with flaps closed
rho = 1.204; % kg/m**3
area = 0.018241; % m**2 : not actually constant
m = 22.6796; % kg; mass after burnout, so constant
Kp = 0.0000003;

%% Initialize Vectors
y = zeros(1, length(t));
v = zeros(1, length(t));
a = zeros(1, length(t));
apogee_target = 1524*ones(1, length(t)); % meters; = 5000 feet
apogee_projected = zeros(1, length(t));
terminal_velocity = zeros(1, length(t));
cd = 0.448*ones(1, length(t));
e = zeros(1, length(t));

%% Inish Condishes
y(1) = 150; % meters; 500 feet
v(1) = 343; % m/s; value comes from pitot tube hopefully
a(1) = -1*g;
e(1) = apogee_target(69) - y(1);

%% Calculates Cd using Euler's Method
for j = 1:length(t)-1
    y(j+1) = y(j) + dt*v(j);
    v(j+1) = v(j) + dt*a(j);
    a(j+1) = (-1*g) - (cd(j)*rho*area*(v(j)^2))/(2*m);
end




%% Plot
figure(1)
plot(t, apogee_projected, 'b-', t, apogee_target, 'k-', 'LineWidth', 1.2);
legend('Projetced Apogee', 'Target Apogee', 'Location','southeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('y(t), m')
title('ACS-less Flight')
% axis([tmin tmax 0 1.5])

figure(2)
plot(t, y, 'b-', t, apogee_target, 'k-', 'LineWidth', 1.2);
legend('Height', 'Target Apogee', 'Location','southeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('y(t), m')
title('ACS-less Flight')

figure(3)
plot(t, v, 'r--', t, a, 'g-', 'LineWidth', 1.2);
legend('Velocity', 'Acceleration', 'Location','northeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('v(t), m/s, a(t), m/s^2')
title('ACS-less Flight')

figure(4)
plot(t, cd, 'g-', 'LineWidth', 1.2);
legend('Cd', 'Location','northeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('Cd')
title('ACS-less Flight')

figure(5)
plot(t, e, 'r--', 'LineWidth', 1.2);
legend('Error', 'Location','northeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('Error, m')
title('ACS-less Flight')