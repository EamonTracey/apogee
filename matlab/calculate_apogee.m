function [projected_apogee, velocity_terminal] = calculate_apogee(drag, current_altitude, velocity, mass)
%   Inputs:
%       drag = approximated drag force from calculate_drag (lbf)
%       current_altitude = reported altitude from Kalman filter in (ft)
%       velocity = vertical velocity (ft/s)
%       mass = mass of vehicle from Luke (slugs)
%
%   Outputs:
%       projected_apogee = predicted apogee assuming flap angle remains
%           constant (ft)
%       velocity_terminal = terminal velocity based on drag. Not critical just cool
%           to know (ft/s)

    g = 32.17405; % ft/s^2

    % If drag funky, prob low enough to neglect drag forces
    if drag <= 0
        % velocity_terminal = 0;
        projected_apogee = (velocity^2)/(2*g) + current_altitude;
    else
        velocity_terminal = velocity.*sqrt(abs(mass.*g./(drag)));
        projected_apogee = ((velocity_terminal.^2)./(2*g)).*log((velocity.^2 + velocity_terminal.^2)./velocity_terminal.^2) + current_altitude;
    end
end
