%% ACS Numeric Model
% PID Forward Loop Model

% Author: William Teasley
% Date: 4 August 2023
% Completed Individually

clc; clear; close all;

%% Set Parameters
tmin = 0; % Start time
tmax = 50; % End time
dt = 0.02; % Average time between data points
t = tmin:dt:tmax;

%% Constants
g = 32.17405; % ft/s^2
rho = 0.002247; % slug/ft**3
mass = 1.1902231; % slugs; mass after burnout, so constant
apogee_target = 5200; % ft
max_servo_deployment = 35/0.33 ; % Maximum servo rotation, deg/s
max_servo_angle = 35;
min_servo_angle = 0;

%% Modes
mode = 1; % 1 = control ON | 2 = control OFF

%% PID Parameters
K = 0.01;
Kp = 50;
Ki = 8;
Kd = 0;

%% Control loop model
for k = 1:1000
    %% Inish Condishes
    y = 1.6515e+03; %  altitude after burnout from March 2
    % y(1) = 828.864; % altitude at burnout, ft from Open Rocket
    v = 588.2806; % velocity after burnout from March 2
    % v(1) = 650.242; % velocity after burnout, ft/s from Open Rocket
    a = -48.0080; % acceleration after burnout, ft/s^2 from March 2
    % a(1) = -61.326; % ft/s^2 from Open Rocket
    D = calculate_drag(v, 0);
    servo_angle = 0;
    apogee_projected = calculate_apogee(D, y, v, mass);
    e = apogee_target - y;
    Prop = e;
    Der = 0; 
    Int = 0; 
    j = 1;
    
    while v(j) >= -10
        y(j+1) = y(j) + dt*v(j) + randi([-1 1]);
        v(j+1) = v(j) + dt*a(j);
    
        D(j+1) = calculate_drag(v(j+1), servo_angle(j));
        % D(j+1) = calculate_drag(v(j+1), 35); % Flight at full flap actuation
        % after burnout
        % D(j+1) = calculate_drag(v(j+1), 0); % Flight with no flap actuation
        % after burnout
        a(j+1) = -1*g - D(j)/mass;
        apogee_projected(j+1) = calculate_apogee(D(j), y(j+1), v(j+1), mass);
    
        e(j+1) = apogee_projected(j) - apogee_target;
    
        switch mode
            case 1
                % Control equations
                Prop(j+1) = e(j+1);
                Der(j+1) = (e(j+1)-e(j))/dt;
                Int(j+1) = Int(j) + ((e(j+1) + e(j))*dt/2);
            
                servo_angle(j+1) = dt*K*(Kd*Der(j) + Kp*Prop(j) + Ki*Int(j)) + servo_angle(j);
            case 2
                servo_angle(j+1) = 0;
        end
        
    
        if y(j+1) > apogee_target
            servo_angle(j+1) = 35;
        end
    
        %% Delay model
        %   Servo cannot actuate faster than 35 deg in 0.33 s
        %   --> which means max slope of servo angle plot is 106.06 deg/s
        servo_change(j+1) = (servo_angle(j+1) - servo_angle(j))/dt ; 
        if servo_change(j+1) >= max_servo_deployment
            servo_angle(j+1) = servo_angle(j) + max_servo_deployment*dt ;
        elseif servo_change(j+1) <= -1*max_servo_deployment
            servo_angle(j+1) = servo_angle(j) - max_servo_deployment*dt ;
        end
    
        if servo_angle(j+1) >= max_servo_angle || servo_angle(j+1) <= min_servo_angle
            servo_angle(j+1) = servo_angle(j);
        end
    
        j = j + 1;
    end

    apogees(k) = max(y);
end

servo_slope = zeros(1, length(servo_angle));
for i = 1:length(servo_angle)-1
    servo_slope(i+1) = (servo_angle(i+1) - servo_angle(i))/dt ; 
end

apogees_avg = mean(apogees);
apogees_max = max(apogees);
apogees_min = min(apogees);
apogees_std = std(apogees);
apogees_range = range(apogees);


t = t(1:j);
[apogee, t_apogee] = max(y);
disp("Target Apogee: " + apogee_target(1) + " ft")
disp("Actual predicted apogee: " + apogee + " ft")
disp("Average apogee: " + apogees_avg + " ft")
disp("Range: " + apogees_range + " ft")
disp("Standard Deviation: " + apogees_std + " ft")

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
plot(t, apogee_projected, 'b-', 'LineWidth',linewidth,'Color',color6);
hold on
yline(apogee_target, 'k-', 'LineWidth', 1.2);
xline(t(t_apogee))
grid on
legend('Projetced Apogee', 'Target Apogee', 'FontSize', fontSize, 'Location', 'northeast'); % Legend
xlabel('t, s') % Add axis labels
ylabel('y(t), m')
title('ACS Flight')
f1.Position = [100,100,800,500]; 
% axis([0 30 4800 apogee_projected(1)*3.281])

f2=figure(2);
plot(t, y, 'b-', 'LineWidth', 1.2);
hold on
yline(apogee_target, 'k-', 'LineWidth', 1.2);
xline(t(t_apogee))
grid on
legend('Height', 'Target Apogee', 'Location','southeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('y(t), m')
title('ACS Flight')
f2.Position = [100,100,800,500]; % this is based on your screen and preference

f3=figure(3);
plot(t, v, 'r--', t, a, 'g-', 'LineWidth', 1.2);
grid on
legend('Velocity', 'Acceleration', 'Location','northeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('v(t), m/s, a(t), m/s^2')
title('ACS Flight')
f3.Position = [100,100,800,500]; % this is based on your screen and preference

f4=figure(4);
plot(t, servo_angle, 'g-', 'LineWidth', 1.2);
grid on
legend('Servo Angle', 'Location','northeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('Servo Angle')
title('ACS Flight')
f4.Position = [100,100,800,500]; % this is based on your screen and preference

f5=figure(5);
plot(t, -1* e, 'r--', 'LineWidth', 1.2);
grid on
legend('Error', 'Location','northeast') % Legend
xlabel('t, s') % Add axis labels
ylabel('Error, m')
title('ACS Flight')
f5.Position = [100,100,800,500]; % this is based on your screen and preference

f6=figure(6);
plot(t, D, '-', 'LineWidth',linewidth,'Color',color6);
grid on
legend('Drag', 'FontSize', fontSize, 'Location', 'southeast'); % Legend
xlabel('t, s') % Add axis labels
ylabel('D(t), Lbf')
title('ACS Flight')
f6.Position = [100,100,800,500]; 

% close all

f7=figure(7);
plot(apogees, '^', 'LineWidth',linewidth,'Color',color2);
hold on 
yline(apogee_target, 'k-', 'LineWidth', 1.2);
yline(apogees_avg, 'LineWidth',linewidth,'Color',color1);
grid on
legend('Apogee', 'Target Apogee', 'Average Apogee',  'FontSize', fontSize, 'Location', 'southeast'); % Legend
xlabel('Test Run') % Add axis labels
ylabel('Apogee, ft')
title('ACS Flight')
f7.Position = [100,100,800,500]; 

