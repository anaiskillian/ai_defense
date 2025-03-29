import React, { useState } from 'react';
import { Box, Typography, IconButton, Dialog, Paper } from '@mui/material';
import OpenInFullIcon from '@mui/icons-material/OpenInFull';
import CloseIcon from '@mui/icons-material/Close';

const VideoFeed = ({ droneId, threatLevel }) => {
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <>
      <Paper
        elevation={0}
        sx={{
          height: '100%',
          backgroundColor: 'rgba(20, 20, 20, 0.95)',
          border: '1px solid rgba(30, 64, 175, 0.1)',
          borderRadius: '12px',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Header with threat level and expand button */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            p: 2,
          }}
        >
          <Typography
            variant="h6"
            sx={{
              color: threatLevel === 'HIGH' ? '#ef4444' : 
                     threatLevel === 'MEDIUM' ? '#f59e0b' : '#22c55e',
            }}
          >
            {threatLevel}
          </Typography>
          <IconButton 
            onClick={handleOpen}
            sx={{ 
              color: '#1E40AF',
              '&:hover': {
                backgroundColor: 'rgba(30, 64, 175, 0.1)',
              }
            }}
          >
            <OpenInFullIcon />
          </IconButton>
        </Box>

        {/* Video placeholder */}
        <Box
          sx={{
            flex: 1,
            backgroundColor: '#0A0A0A',
            m: 2,
            mt: 0,
            borderRadius: '8px',
            position: 'relative',
            width: '100%',
            '&::before': {
              content: '""',
              display: 'block',
              paddingTop: '56.25%', // 9/16 = 0.5625 = 56.25%
            },
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.5)' }}>
              Live Feed - Drone {droneId}
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Expanded view dialog */}
      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        PaperProps={{
          sx: {
            backgroundColor: '#0A0A0A',
            backgroundImage: 'none',
          }
        }}
      >
        <Box sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h4">
              Drone {droneId} - Detailed Analysis
            </Typography>
            <IconButton
              onClick={handleClose}
              sx={{ color: '#FFFFFF' }}
            >
              <CloseIcon />
            </IconButton>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 3 }}>
            {/* Video feed */}
            <Box
              sx={{
                flex: 2,
                backgroundColor: '#141414',
                borderRadius: '12px',
                height: '70vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.5)' }}>
                Live Feed - Drone {droneId}
              </Typography>
            </Box>

            {/* Analysis panel */}
            <Paper
              elevation={0}
              sx={{
                flex: 1,
                p: 3,
                backgroundColor: 'rgba(20, 20, 20, 0.95)',
                borderRadius: '12px',
                border: '1px solid rgba(30, 64, 175, 0.1)',
              }}
            >
              <Typography variant="h6" gutterBottom>
                Threat Analysis
              </Typography>
              <Typography
                variant="h5"
                gutterBottom
                sx={{
                  color: threatLevel === 'HIGH' ? '#ef4444' : 
                         threatLevel === 'MEDIUM' ? '#f59e0b' : '#22c55e',
                  mb: 3,
                }}
              >
                {threatLevel} THREAT LEVEL
              </Typography>
              <Typography variant="body1" paragraph>
                Sonar Data: [Simulated sonar readings]
              </Typography>
              <Typography variant="body1" paragraph>
                Camera Analysis: [Object detection results]
              </Typography>
              <Typography variant="body1">
                LLM Assessment: [Threat analysis details]
              </Typography>
            </Paper>
          </Box>
        </Box>
      </Dialog>
    </>
  );
};

export default VideoFeed;
