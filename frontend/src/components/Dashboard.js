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
    { id: 4, threatLevel: 'LOW' },
    { id: 5, threatLevel: 'MEDIUM' },
    { id: 6, threatLevel: 'HIGH' },
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
        variant="h3" 
        component="h1" 
        sx={{ 
          p: 3,
          pb: 5,
          fontWeight: 'bold',
          textAlign: 'center',
          background: 'linear-gradient(45deg, #4169E1 0%, #6495ED 30%, #87CEEB 60%, #B0E0E6 90%)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          color: 'transparent',
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
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: 3,
            }}
          >
            {drones.map((drone) => (
              <Grid 
                item
                key={drone.id}
                sx={{
                  minWidth: 0,
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Box sx={{ width: '98%' }}>
                  <VideoFeed
                    droneId={drone.id}
                    threatLevel={drone.threatLevel}
                  />
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
