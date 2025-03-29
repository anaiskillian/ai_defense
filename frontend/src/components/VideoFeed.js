import React, { useState } from 'react';
import { Box, Typography, IconButton, Dialog, Paper } from '@mui/material';
import OpenInFullIcon from '@mui/icons-material/OpenInFull';
import CloseIcon from '@mui/icons-material/Close';
import YOLOFeed from './YOLOFeed';
import LLMAssessment from './LLMAssessment';

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
          backgroundColor: '#0A0A0A',
          border: '1px solid rgba(30, 64, 175, 0.1)',
          borderRadius: '16px',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          transition: 'all 0.3s ease-in-out',
          cursor: 'pointer',
          '&:hover': {
            transform: 'scale(1.05)',
            boxShadow: '0 0 20px rgba(65, 105, 225, 0.3)',
            zIndex: 1,
          },
        }}
      >
        {/* Video placeholder with expand button overlay */}
        <Box
          sx={{
            position: 'relative',
            aspectRatio: '16/9',
            width: '100%',
            height: '100%',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              display: 'block',
              paddingTop: '56.25%', // 16:9 aspect ratio
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
              backgroundColor: '#0A0A0A',
            }}
          >
            <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.5)' }}>
              Live Feed - Drone {droneId}
            </Typography>
          </Box>
          {/* Expand button overlay */}
          <IconButton 
            onClick={handleOpen}
            sx={{ 
              position: 'absolute',
              top: 8,
              right: 8,
              color: '#1E40AF',
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              '&:hover': {
                backgroundColor: 'rgba(30, 64, 175, 0.3)',
              }
            }}
          >
            <OpenInFullIcon />
          </IconButton>
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
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h5" sx={{ 
              color: threatLevel === 'HIGH' ? '#ef4444' : 
                     threatLevel === 'MEDIUM' ? '#f59e0b' : '#22c55e',
              fontWeight: 'bold'
            }}>
              Drone {droneId} Feed
            </Typography>
            <IconButton onClick={handleClose} sx={{ color: 'white' }}>
              <CloseIcon />
            </IconButton>
          </Box>

          <Box sx={{ display: 'flex', gap: 3 }}>
            {/* Video feed */}
            <Box
              sx={{
                flex: 2,
                backgroundColor: '#141414',
                borderRadius: '16px',
                height: '70vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                overflow: 'hidden',
                position: 'relative',
                p: 1.5,
                '& > *': {
                  position: 'absolute',
                  top: '12px',
                  left: '12px',
                  right: '12px',
                  bottom: '12px',
                  width: 'calc(100% - 24px)',
                  height: 'calc(100% - 24px)',
                }
              }}
            >
              <YOLOFeed droneId={droneId} />
            </Box>

            {/* Analysis panel */}
            <LLMAssessment threatLevel={threatLevel} />
          </Box>
        </Box>
      </Dialog>
    </>
  );
};

export default VideoFeed;
