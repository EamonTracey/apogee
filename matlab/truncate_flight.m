function [time, state, servoPercentage, apogeePrediction, altitudeFiltered, velocityFiltered, accelerationFiltered, temp, b, c] = truncate_flight(data)
%   Inputs:
%       data = matrix of launch data      
%
%   Outputs:
%       state = launch state (ground, launch, burnout, overshoot, apogee)

%% Convert data matrix to variables
    time = data.Time;
    state = data.State;
    servoPercentage = data.ServoPercentage;
    apogeePrediction = data.ApogeePrediction;
    altitudeFiltered = data.AltitudeFiltered;
    velocityFiltered = data.VelocityFiltered;
    accelerationFiltered = data.AccelerationFiltered;
    temp = data.Temperature;

%% Find start and end of relevant flight data
    a = 0;
    b = 0;
    c = 0;
    d = 0;
    truth1 = true;
    truth2 = true;
    truth3 = true;
    truth4 = true;

    while truth1
        a = a+1;
        if state(a) == "State.LAUNCHED"
            truth1 = false;
        end
    end

    while truth2
        b = b+1;
        if state(b) == "State.BURNOUT"
            truth2 = false;
        end
    end

    while truth3
        c = c+1;
        if state(c) == "State.OVERSHOOT"
            truth3 = false;
        end
    end
    
    while truth4
        d = d+1;
        if state(d) == "State.APOGEE"
            truth4 = false;
        end
    end

    b = b-a;
    c = c-a;
%% Truncate data
    time = time(a:d);
    state = state(a:d);
    apogeePrediction = apogeePrediction(a:d);
    servoPercentage = servoPercentage(a:d);
    altitudeFiltered = altitudeFiltered(a:d);
    velocityFiltered = velocityFiltered(a:d);
    accelerationFiltered = accelerationFiltered(a:d);
    temp = temp(a:d);
end