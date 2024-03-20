%% ACS_2023_Huntsville_Data

% Plots various things recorded during Huntsville 2023 flight

% Author: William Teasley
% Date: 12 August 2023
% Completed Individually

clc; clear; close all;

% Loads in data
load("ACS_2023_Huntsville_Data.mat")
load("ACS_2023_Huntsville_Scoring_Data.mat")
load("ACS_2023_Huntsville_Recovery_Data.mat")


%% Read in variables
state = State;
index = 0;

for i = 1:length(state)
    if (state(i) == "BURNOUT" || state(i) == "OVERSHOOT") && Time(i) <= 5700
        index = index+1;
        y(index)= Altitude(i)*3.281;
        t(index) = Time(i);
        projected_Apogee(index) = Projected_Apogee(i)*3.281;
        servo_Angle(index) = Servo_Angle(i);
        bmp_Altitude(index) = BMP_Altitude(i)*3.281;
        error_Apogee(index) = Error_Apogee(i)*3.281;
        altitude_Kalman(index) = Kalman_Altitude(i)*3.281;
        velocity_Kalman(index) = Kalman_Velocity(i)*3.281;
        acceleration_Kalman(index) = Kalman_Acceleration(i)*3.281;        
    end
end

apogee = max(y);
apogee_Kalman = max(altitude_Kalman);
apogee_target = 4600;

% my_drag = calculate_drag(velocity_Kalman, servo_Angle);
% my_apogee_prediction = calculate_apogee(my_drag, altitude_Kalman, velocity_Kalman, 1.2); 

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

figure(1)
plot(t, y, 'LineWidth',linewidth,'Color',color1);
hold on
plot(t, altitude_Kalman, 'LineWidth',linewidth,'Color',color2);
yline(apogee_target,'LineWidth',linewidth, 'Color',color3)
legend("Altitude", "Kalman Altitude", "Target Apogee")
grid on 

figure(2)
plot(t, projected_Apogee, 'LineWidth',linewidth,'Color',color2);
hold on
yline(apogee, 'LineWidth', linewidth, 'Color',color5)
yline(apogee_target, 'LineWidth',linewidth,'Color',color3)
% plot(t, my_apogee_prediction, 'LineWidth',linewidth,'Color',color4);
legend("Projected Apogee", "Apogee", "Target Apogee", 'My apogee prediction')
grid on 

figure(3)
plot(t, servo_Angle, 'LineWidth',linewidth,'Color',color6);
grid on 

figure(4)
plot(t, velocity_Kalman, 'LineWidth',linewidth,'Color',color3);
hold on 
plot(t, acceleration_Kalman, 'LineWidth',linewidth,'Color',color4);
grid on 

% figure(3)
% plot(t, error_Apogee, 'LineWidth',linewidth,'Color',color3);
% legend("Error")



disp("ACS Accelerometer Approximation: " + apogee + " ft")
disp("ACS Kalman Altitude: " + apogee_Kalman + " ft")
disp("ACS Altimeter: " + max(bmp_Altitude) + " ft")
disp("PED Altimeter: " + max(PED_Altitude) + " ft")
disp("NED Green Altimeter: " + max(NEDG_Altitude) + " ft")
disp("NED Blue Altimeter: " + max(NEDB_Altitude) + " ft")
disp("FED Altimeter: " + max(FED_Altitude) + " ft")
disp("Scoring Altimeter: " + max(AltitudeBaroFtAGL) + " ft")

