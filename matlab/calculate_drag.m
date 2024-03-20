function [drag, mach_number] = calculate_drag(velocity, flap_angle)
%   Inputs:
%       velocity = vertical velocity (ft/s)
%       flap_angle = Assume flap angle equals servo actuation percentage.
%           This is not perfectly accurate but a decent approximation.
%       temp = 
%
%   Outputs:
%       drag = approximated drag force from CFD (lbf)
%       mach_number = mach number based on velocity. Not critical just cool
%           to know
% 
%   This is a rough calculation of mach number given velocity.
%   Improvement: calculate based on temperature.
    mach_number = velocity / sqrt(1.4*1716.46*514.67) ;
% 
%   This equation is based on interpolated CFD results.
    drag =  (-20.74 ... 
            + 4.351 * flap_angle ...
            + 131.1 * mach_number ...
            - 0.1112 * flap_angle.^2 ...
            - 19.77 * flap_angle.*mach_number ...
            + 146 * mach_number.^2 ...
            + 0.5031 * flap_angle.^2 .* mach_number...
            + 31.64 * flap_angle .* mach_number.^2 ...
            + 117.8 * mach_number.^3 ) * 0.224809; 

    if drag <= 0
        drag = 0;
    end
end