import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
} from '@mui/material';
import VideoFeed from './VideoFeed';

const Dashboard = () => {
  // Simulated drone data
  const drones = [
    { id: 1, threatLevel: 'HIGH' },
    { id: 2, threatLevel: 'LOW' },
    { id: 3, threatLevel: 'MEDIUM' },
  ];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        width: '100vw',
        backgroundColor: '#0A0A0A',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Typography 
        variant="h4" 
        component="h1" 
        sx={{ 
          p: 3,
          pb: 2,
        }}
      >
        Threat Analysis Dashboard
      </Typography>

      <Box
        sx={{
          flex: 1,
          display: 'flex',
          p: 3,
          pt: 0,
        }}
      >
        <Box
          sx={{
            display: 'flex',
            width: '100%',
            backgroundColor: 'rgba(20, 20, 20, 0.95)',
            borderRadius: '16px',
            border: '1px solid rgba(30, 64, 175, 0.1)',
            p: 3,
          }}
        >
          <Grid 
            container 
            spacing={3}
            sx={{
              width: '100%',
              margin: 0,
              flexWrap: 'nowrap',
            }}
          >
            {drones.map((drone) => (
              <Grid 
                item
                key={drone.id}
                sx={{
                  flex: 1,
                  minWidth: 0, // Allows the flex item to shrink below its minimum content size
                }}
              >
                <VideoFeed
                  droneId={drone.id}
                  threatLevel={drone.threatLevel}
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
