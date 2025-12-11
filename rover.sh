[Unit]
Description=Rover Autonomous Navigation System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/rover
ExecStart=/home/pi/rover/start_rover.sh

# Restart robot automatically if script crashes
Restart=always
RestartSec=5

# Logging
StandardOutput=append:/home/pi/rover/rover.log
StandardError=append:/home/pi/rover/rover_error.log

[Install]
WantedBy=multi-user.target
